"""
backend/app/llm/llama_cpp_engine.py
===================================
High-level role:
- Concrete LLM engine backed by `llama-cpp-python` for local inference.

Where this fits:
- Implements the interface defined in `engine.py`.
- Constructed by the backend based on `config.py` settings.

What this file typically contains (when implemented):
- A class `LlamaCppEngine(LanguageModelEngine)` that loads a GGUF model file from disk
  (e.g., `/models/llama3.1-8b.Q4_K_M.gguf`).
- A `generate(...)` method that assembles prompts/messages, invokes the model, and
  returns `(text, usage)`.

Operational notes:
- CPU/GPU offloading (via llama.cpp build flags) can be configured for performance.
- Keep prompt construction consistent with policy guardrails and persona prompts.
"""

# Placeholder symbol to mark this module
LLAMA_ENGINE_AVAILABLE = False


