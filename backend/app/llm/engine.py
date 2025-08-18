"""
backend/app/llm/engine.py
=========================
High-level role:
- Declares the abstract interface for LLM engines used by the backend.
- Concrete implementations (e.g., llama.cpp, Ollama) must implement this interface.

Where this fits:
- Imported by `api.py` to obtain an engine instance based on configuration.
- Concrete engine modules live alongside this file (see `llama_cpp_engine.py`,
  `ollama_proxy.py`).

What this file typically contains (when implemented):
- An abstract class like `LanguageModelEngine` with:
  - `generate(system_prompt: str, messages: list[dict], max_tokens: int, temperature: float, top_p: float) -> tuple[str, dict]`
    returning the generated text and a usage dict with token counts.
- A small factory function to build an engine from config.

Notes for new contributors:
- Keep the interface minimal and model-agnostic so multiple backends can plug in.
- Token accounting can be approximate; ensure it is clearly documented.
"""

from __future__ import annotations

from typing import Tuple


class LanguageModelEngine:  # pylint: disable=too-few-public-methods
	"""Abstract base class for LLM engines."""

	def generate(
		self,
		system_prompt: str,
		messages: list[dict],
		max_tokens: int = 180,
		temperature: float = 0.8,
		top_p: float = 0.9,
	) -> Tuple[str, dict]:
		"""Generate text from messages and return (text, usage)."""
		raise NotImplementedError


class EchoEngine(LanguageModelEngine):
	"""A development engine that echoes the last user message with a prefix.

	Useful for wiring and testing before real LLM integration.
	"""

	def generate(self, system_prompt, messages, max_tokens=180, temperature=0.8, top_p=0.9):
		last_user = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
		text = f"[echo] {last_user}".strip()
		usage = {"prompt_tokens": 0, "completion_tokens": len(text.split()), "total_tokens": len(text.split())}
		return text, usage


