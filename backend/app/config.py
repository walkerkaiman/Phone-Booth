"""
backend/app/config.py
=====================
Configuration loading and management for the backend service.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# Default configuration
DEFAULT_CONFIG = {
    "server": {
        "host": "0.0.0.0",
        "port": 8080,
        "cors_origins": ["*"]
    },
    "llm": {
        "engine": "echo",
        "model_path": "/models/llama3.1-8b.Q4_K_M.gguf",
        "context_length": 2048,
        "temperature": 0.8,
        "top_p": 0.9,
        "max_tokens": 180
    },
    "sessions": {
        "ttl_seconds": 600,
        "history_max_turns": 8,
        "store": "memory"
    },
    "logging": {
        "level": "INFO",
        "json": True
    }
}


class Config:
    """Configuration manager for the backend service."""
    
    def __init__(self, config_path: str | Path | None = None):
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Look for config in parent directory (project root)
            self.config_path = Path(__file__).parent.parent.parent / "config" / "backend.json"
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
    def server(self) -> Dict[str, Any]:
        """Server configuration."""
        return self._config["server"]
    
    @property
    def llm(self) -> Dict[str, Any]:
        """LLM configuration."""
        return self._config["llm"]
    
    @property
    def sessions(self) -> Dict[str, Any]:
        """Session configuration."""
        return self._config["sessions"]
    
    @property
    def logging(self) -> Dict[str, Any]:
        """Logging configuration."""
        return self._config["logging"]
    
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


