"""
backend/app/config.py
=====================
High-level role:
- Centralizes configuration for the backend service (model paths, engine selection,
  session TTL, logging options, etc.).

Where this fits:
- Read by `main.py` during app startup to configure logging and subsystems.
- Accessed by `api.py`, `llm/` engines, and `sessions/` store to get runtime settings.

What this file typically contains (when implemented):
- A `Settings` class (e.g., Pydantic BaseSettings) with fields like:
  - `llm.engine` ("llama_cpp" or "ollama")
  - `llm.model_path`, `llm.context_length`, `llm.temperature`, `llm.top_p`, `llm.max_tokens`
  - `sessions.ttl_seconds`, `sessions.history_max_turns`, `sessions.store`
  - `logging.level`, `logging.json`
- Logic to load JSON from `config/backend.json` and/or environment variables.

Notes for new contributors:
- Keep defaults sensible for development. Allow overrides via env vars.
- Provide a small helper function to load and cache settings for the app lifetime.
"""

# Placeholder example structure to show intended usage
DEFAULT_CONFIG = {
	"llm": {
		"engine": "llama_cpp",
		"model_path": "/models/llama3.1-8b.Q4_K_M.gguf",
		"context_length": 2048,
		"temperature": 0.8,
		"top_p": 0.9,
		"max_tokens": 180,
	},
	"sessions": {
		"ttl_seconds": 600,
		"history_max_turns": 8,
		"store": "memory",
	},
	"logging": {"level": "INFO", "json": True},
}


