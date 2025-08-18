"""
frontend/booth/config.py
========================
Configuration loading and management for the frontend booth application.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# Default configuration
DEFAULT_CONFIG = {
    "backend_url": "http://localhost:8080",
    "booth_id": "booth-01",
    "default_personality": "trickster",
    "audio": {
        "sample_rate": 16000,
        "channels": 1,
        "chunk_size": 1024,
        "device": None  # None = default device
    },
    "vad": {
        "threshold": 0.5,
        "min_speech_duration_ms": 250,
        "max_speech_duration_s": 30,
        "min_silence_duration_ms": 100
    },
    "asr": {
        "model_size": "small",
        "compute_type": "int8",
        "language": "en",
        "beam_size": 5
    },
    "vision": {
        "enabled": True,
        "camera_index": 0,
        "capture_interval_ms": 1000,
        "max_tags": 10
    },
    "tts": {
        "voice_map": {
            "trickster": "en_US-lessac-high",
            "sage": "en_GB-alan-medium",
            "muse": "en_US-lessac-medium",
            "jester": "en_GB-alan-low",
            "night_watch": "en_US-lessac-low"
        },
        "sample_rate": 22050,
        "speed": 1.0
    },
    "lighting": {
        "enabled": True,
        "driver": "null",  # null, pwm, or custom
        "gpio_pin": 18,
        "brightness_range": [0, 255],
        "smoothing": {
            "attack_ms": 50,
            "release_ms": 200
        }
    },
    "session": {
        "auto_reconnect": True,
        "max_retries": 3,
        "retry_delay_s": 1.0
    },
    "modes": ["chat", "riddle", "haiku", "story"]
}


class Config:
    """Configuration manager for the frontend booth application."""
    
    def __init__(self, config_path: str | Path | None = None):
        self.config_path = Path(config_path) if config_path else Path("config/frontend.json")
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file, falling back to defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                # Merge with defaults
                config = DEFAULT_CONFIG.copy()
                self._deep_merge(config, file_config)
                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
                print("Using default configuration")
                return DEFAULT_CONFIG.copy()
        else:
            print(f"Config file not found at {self.config_path}, using defaults")
            return DEFAULT_CONFIG.copy()
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Recursively merge update dict into base dict."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    @property
    def backend_url(self) -> str:
        """Backend URL for API calls."""
        return self._config["backend_url"]
    
    @property
    def booth_id(self) -> str:
        """Unique booth identifier."""
        return self._config["booth_id"]
    
    @property
    def default_personality(self) -> str:
        """Default personality to use."""
        return self._config["default_personality"]
    
    @property
    def audio(self) -> Dict[str, Any]:
        """Audio configuration."""
        return self._config["audio"]
    
    @property
    def vad(self) -> Dict[str, Any]:
        """Voice Activity Detection configuration."""
        return self._config["vad"]
    
    @property
    def asr(self) -> Dict[str, Any]:
        """Automatic Speech Recognition configuration."""
        return self._config["asr"]
    
    @property
    def vision(self) -> Dict[str, Any]:
        """Vision/camera configuration."""
        return self._config["vision"]
    
    @property
    def tts(self) -> Dict[str, Any]:
        """Text-to-Speech configuration."""
        return self._config["tts"]
    
    @property
    def lighting(self) -> Dict[str, Any]:
        """Lighting configuration."""
        return self._config["lighting"]
    
    @property
    def session(self) -> Dict[str, Any]:
        """Session management configuration."""
        return self._config["session"]
    
    @property
    def modes(self) -> list[str]:
        """Available conversation modes."""
        return self._config["modes"]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by dot-notation key."""
        keys = key.split('.')
        value = self._config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default


# Global config instance
config = Config()


