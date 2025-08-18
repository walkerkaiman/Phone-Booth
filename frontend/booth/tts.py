"""
frontend/booth/tts.py
=====================
High-level role:
- Text-to-speech synthesis using Piper (or another local TTS engine).

Where this fits:
- Called by `main.py` to synthesize the backend's text reply into PCM audio for
  immediate playback.
- Provides an amplitude envelope that downstream lighting code uses to set brightness.

What this file typically contains (when implemented):
- Voice selection mapped from the current persona via config (`voice_map`).
- A function `synthesize(text, voice_id)` returning PCM samples and sample rate.
- A helper `amplitude_envelope(samples)` returning values scaled to 0–255.

Notes for new contributors:
- Ensure synthesis is non-blocking or runs in a worker to avoid stalling the loop.
"""

# Placeholder marker
TTS_AVAILABLE = False


