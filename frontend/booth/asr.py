"""
frontend/booth/asr.py
=====================
High-level role:
- Automatic Speech Recognition (ASR) using Faster-Whisper (ctranslate2 backend).

Where this fits:
- Receives a recorded audio segment for a single user utterance and outputs text.
- Called by `main.py` after VAD signals end-of-utterance.

What this file typically contains (when implemented):
- Model loading (size and compute type) based on config (e.g., `small`, `int8`).
- A function `transcribe(audio, sample_rate)` that returns the best-effort transcript.

Notes for new contributors:
- Keep latency low by loading the model once and reusing it across turns.
"""

# Placeholder marker
ASR_AVAILABLE = False


