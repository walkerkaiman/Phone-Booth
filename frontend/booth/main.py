"""
frontend/booth/main.py
======================
High-level role:
- Entry point for the phone booth client application.
- Orchestrates hardware/software components: mic capture, VAD, ASR, vision snapshot,
  network requests to backend, TTS playback, and lighting control.

Where this fits:
- Runs on each physical booth device. Communicates with the backend via HTTP.

Typical flow (when implemented):
1) On handset pickup: generate `session_id` (UUIDv4), load `frontend/config.py`,
   call `/v1/session/start`.
2) For each user turn:
   - Capture speech until VAD detects end-of-utterance.
   - Transcribe with Faster-Whisper.
   - Grab a single webcam frame and extract scene tags/caption via `vision.py`.
   - Send `/v1/generate` with `session_id`, text, and scene.
   - Receive reply text; synthesize speech with Piper via `tts.py` and play to speakers.
   - Drive lighting brightness according to TTS amplitude via `lighting/mapper.py` and
     a selected `lighting/driver_*`.
3) On handset hangup: call `/v1/session/release`, stop audio, set lighting to 0, reset.

Notes for new contributors:
- Keep I/O and blocking work off the UI/interaction loop using threads or async.
- Provide clear logs for each stage to aid debugging on embedded devices.
"""

import sys
from pathlib import Path

# Add the project root to Python path so imports work
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def run():
	"""Main entry point for the booth application."""
	print("Character Booth Frontend - Starting...")
	print("(This is a placeholder implementation)")
	print("In the real implementation, this would:")
	print("1. Load configuration")
	print("2. Initialize audio I/O, VAD, ASR, TTS, vision, and lighting")
	print("3. Start the main booth interaction loop")
	print("4. Handle handset pickup/hangup events")
	print("5. Process user speech and generate responses")
	return 0


if __name__ == "__main__":
	sys.exit(run())


