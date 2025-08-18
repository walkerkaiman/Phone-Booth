"""
frontend/booth/vision.py
========================
High-level role:
- Captures a single frame from a webcam per user turn and extracts simple scene cues
  such as a short caption and a small set of tags (colors, objects, brightness).

Where this fits:
- Called by `main.py` once per user turn; returns a dict `{caption, tags}` to include
  in the `/v1/generate` request to the backend.

What this file typically contains (when implemented):
- Webcam acquisition using OpenCV.
- Lightweight heuristics to extract dominant colors/brightness and a short caption.

Notes for new contributors:
- Maintain strict privacy: no identity, age, or gender guesses; avoid face detection.
"""

# Placeholder marker
VISION_AVAILABLE = False


