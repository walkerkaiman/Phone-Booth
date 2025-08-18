"""
frontend/booth/audio_io.py
==========================
High-level role:
- Low-level audio input/output utilities for microphone capture and speaker playback.

Where this fits:
- Used by `main.py` to capture user speech and to play TTS audio.
- VAD (`vad.py`) operates on the captured audio stream to detect speech segments.

What this file typically contains (when implemented):
- Microphone stream management (sample rate, chunk size) via `sounddevice` or `pyaudio`.
- Output stream for PCM playback.
- Utility functions to convert between numpy arrays and byte buffers.

Notes for new contributors:
- Handle device selection and error conditions gracefully; provide clear logging.
"""

# Placeholder marker
AUDIO_IO_AVAILABLE = False


