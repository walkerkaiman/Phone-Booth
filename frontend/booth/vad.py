"""
frontend/booth/vad.py
=====================
High-level role:
- Voice Activity Detection (VAD) helper using `webrtcvad` to decide when the user is
  speaking and when they have finished their utterance.

Where this fits:
- Consumes audio frames from `audio_io.py` and emits start/stop speech events.
- Used by `main.py` to delimit a single user turn for ASR.

What this file typically contains (when implemented):
- A class wrapping `webrtcvad.Vad` with tunable aggressiveness.
- Sliding-window logic to detect speech segments in real time.

Notes for new contributors:
- Carefully choose frame sizes (e.g., 20ms) and sample rate to match ASR expectations.
"""

# Placeholder marker
VAD_AVAILABLE = False


