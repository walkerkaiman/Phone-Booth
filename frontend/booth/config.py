"""
frontend/booth/config.py
========================
High-level role:
- Loads and provides frontend configuration: backend URL, booth id, default
  personality, audio/ASR/TTS settings, lighting driver selection, and supported modes.

Where this fits:
- Read by `main.py` during startup to configure subsystems.
- Referenced by `tts.py`, `asr.py`, and `lighting/` drivers.

What this file typically contains (when implemented):
- Loader for JSON config at `config/frontend.json` with sane defaults.
- Accessors for individual sections and validation of required fields.

Notes for new contributors:
- Keep the API stable; other modules should not need to know the file format.
"""

# Placeholder defaults mirroring the design document
DEFAULT_FRONTEND_CONFIG = {
	"backend_url": "http://backend.local:8080",
	"booth_id": "booth-12",
	"default_personality": "trickster",
	"audio": {"sample_rate": 16000},
	"asr": {"model_size": "small", "compute_type": "int8"},
	"tts": {
		"voice_map": {
			"trickster": "en_US-lessac-high",
			"sage": "en_GB-alan-medium"
		}
	},
	"lighting": {"enabled": True, "driver": "pwm", "gpio_pin": 18},
	"modes": ["chat", "riddle", "haiku", "story"],
}


