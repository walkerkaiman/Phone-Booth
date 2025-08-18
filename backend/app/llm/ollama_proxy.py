"""
backend/app/llm/ollama_proxy.py
===============================
High-level role:
- Concrete LLM engine that forwards generate requests to an external Ollama server
  via HTTP. Useful if you want to centralize models or run them on a different host.

Where this fits:
- Implements the `LanguageModelEngine` interface from `engine.py`.
- Selected by configuration (e.g., `llm.engine == "ollama"`).

What this file typically contains (when implemented):
- A class `OllamaProxyEngine(LanguageModelEngine)` that:
  - Stores the Ollama base URL and model name.
  - Serializes prompts/messages into Ollama's API format.
  - Parses the response text and (if available) usage metadata.

Notes for new contributors:
- This design keeps the backend small while delegating heavy lifting to Ollama.
- Ensure robust error handling and clear timeout behavior.
"""

# Placeholder symbol to mark this module
OLLAMA_ENGINE_AVAILABLE = False


