"""
frontend/booth/asr.py
=====================
Minimal Faster-Whisper ASR wrapper with lazy model loading.

High-level role:
- Accept a single-utterance audio buffer and return a transcript string.

Notes:
- Uses configuration from `frontend/booth/config.py` to pick model size and compute type.
- Gracefully degrades if faster-whisper is not available.
"""

from __future__ import annotations

from typing import Any, Optional

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    np = None  # type: ignore

try:
    from faster_whisper import WhisperModel  # type: ignore
    _FW_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    WhisperModel = None  # type: ignore
    _FW_AVAILABLE = False

from .config import config


class ASREngine:
    """Lightweight ASR engine that loads Faster-Whisper on first use."""

    def __init__(self) -> None:
        self._model: Optional[Any] = None
        self._loaded: bool = False
        self._load_error: Optional[str] = None

    def _ensure_loaded(self) -> bool:
        if self._loaded:
            return self._model is not None
        self._loaded = True

        if not _FW_AVAILABLE:
            self._load_error = "faster-whisper not installed"
            return False

        try:
            asr_cfg = config.asr
            model_size = asr_cfg.get("model_size", "small")
            compute_type = asr_cfg.get("compute_type", "int8")
            self._model = WhisperModel(model_size, compute_type=compute_type)
            return True
        except Exception as exc:  # pragma: no cover
            self._model = None
            self._load_error = str(exc)
            return False

    def transcribe(self, audio: bytes | "np.ndarray", sample_rate: int) -> str:
        """Transcribe a single-utterance audio buffer to text.

        Accepts 16-bit PCM little-endian `bytes` or a NumPy float32 array.
        Returns best-effort transcript (empty string on failure).
        """
        if not self._ensure_loaded():
            return ""

        if self._model is None:
            return ""

        try:
            # Normalize input to float32 NumPy array in range [-1, 1]
            if np is None:
                return ""

            if isinstance(audio, (bytes, bytearray)):
                pcm = np.frombuffer(audio, dtype=np.int16)  # type: ignore
                audio_f32 = (pcm.astype(np.float32) / 32768.0)  # type: ignore
            else:
                audio_f32 = audio  # assume float32 array

            lang = config.asr.get("language")
            beam = int(config.asr.get("beam_size", 5))

            segments, info = self._model.transcribe(
                audio_f32,
                language=lang,
                beam_size=beam,
                vad_filter=True,
            )

            transcript_parts = [seg.text for seg in segments]
            return " ".join(part.strip() for part in transcript_parts).strip()
        except Exception:
            return ""


# Module-level singleton and availability flag
asr_engine = ASREngine()
ASR_AVAILABLE = _FW_AVAILABLE

