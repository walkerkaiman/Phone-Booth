"""
frontend/booth/lighting/mapper.py
=================================
High-level role:
- Maps audio amplitude (from TTS output) to a brightness value in the 0–255 range,
  with smoothing to avoid flicker.

Where this fits:
- Called by `main.py` while TTS audio is playing; output is sent to a `LightingDriver`.

What this file typically contains (when implemented):
- Envelope follower with configurable attack and release times.
- Scaling and clamping utilities.

Notes for new contributors:
- Keep computation lightweight to run comfortably on small single-board computers.
"""

# Placeholder marker
MAPPER_AVAILABLE = False


