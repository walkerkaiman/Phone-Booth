"""
backend/app/llm/llama_cpp_engine.py
===================================
Local LLM engine using llama-cpp-python for inference.

This engine loads a GGUF model file and provides text generation capabilities
for the Character Booth System backend.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

from .engine import LanguageModelEngine

logger = logging.getLogger(__name__)


class LlamaCppEngine(LanguageModelEngine):
    """Local LLM engine using llama-cpp-python for inference."""

    def __init__(
        self,
        model_path: str,
        context_length: int = 2048,
        temperature: float = 0.8,
        top_p: float = 0.9,
        max_tokens: int = 180,
        n_gpu_layers: int = -1,
        n_threads: Optional[int] = None,
        verbose: bool = False,
    ):
        """Initialize the LlamaCpp engine.
        
        Args:
            model_path: Path to the GGUF model file
            context_length: Maximum context length for the model
            temperature: Sampling temperature (0.0 to 2.0)
            top_p: Top-p sampling parameter (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            n_gpu_layers: Number of layers to offload to GPU (-1 for all, 0 for CPU only)
            n_threads: Number of CPU threads to use (None for auto)
            verbose: Enable verbose logging from llama-cpp
        """
        if Llama is None:
            raise ImportError(
                "llama-cpp-python is not installed. "
                "Install it with: pip install llama-cpp-python"
            )

        self.model_path = Path(model_path)
        self.context_length = context_length
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.n_gpu_layers = n_gpu_layers
        self.n_threads = n_threads
        self.verbose = verbose

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        logger.info(f"Loading LlamaCpp model from: {self.model_path}")
        logger.info(f"Context length: {context_length}, GPU layers: {n_gpu_layers}")

        # Initialize the model
        self._model = Llama(
            model_path=str(self.model_path),
            n_ctx=context_length,
            n_gpu_layers=n_gpu_layers,
            n_threads=n_threads,
            verbose=verbose,
        )

        logger.info("LlamaCpp model loaded successfully")

    def generate(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Generate text from messages using the loaded model.
        
        Args:
            system_prompt: System prompt to prepend to the conversation
            messages: List of message dicts with 'role' and 'content' keys
            max_tokens: Override default max tokens
            temperature: Override default temperature
            top_p: Override default top_p
            
        Returns:
            Tuple of (generated_text, usage_stats)
        """
        # Use provided parameters or defaults
        max_tokens = max_tokens or self.max_tokens
        temperature = temperature or self.temperature
        top_p = top_p or self.top_p

        # Build the full prompt
        prompt = self._build_prompt(system_prompt, messages)
        
        logger.debug(f"Generating with max_tokens={max_tokens}, temperature={temperature}")
        
        try:
            # Generate response
            response = self._model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop=["</s>", "<|endoftext|>", "\n\n\n"],  # Common stop tokens
                echo=False,  # Don't include input in output
            )
            
            # Extract the generated text
            generated_text = response["choices"][0]["text"].strip()
            
            # Build usage stats
            usage = {
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "total_tokens": response.get("usage", {}).get("total_tokens", 0),
            }
            
            logger.debug(f"Generated {len(generated_text)} characters")
            return generated_text, usage
            
        except Exception as e:
            logger.error(f"Error during text generation: {e}")
            # Return a fallback response
            fallback_text = "I'm having trouble thinking of a response right now. Could you try again?"
            fallback_usage = {
                "prompt_tokens": 0,
                "completion_tokens": len(fallback_text.split()),
                "total_tokens": len(fallback_text.split()),
            }
            return fallback_text, fallback_usage

    def _build_prompt(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """Build a prompt string from system prompt and messages.
        
        This formats the conversation in a way that works well with most
        Llama-based models.
        """
        # Start with system prompt
        prompt_parts = [f"<|system|>\n{system_prompt}\n<|endoftext|>"]
        
        # Add conversation messages
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "user":
                prompt_parts.append(f"<|user|>\n{content}\n<|endoftext|>")
            elif role == "assistant":
                prompt_parts.append(f"<|assistant|>\n{content}\n<|endoftext|>")
            elif role == "system":
                # Additional system messages
                prompt_parts.append(f"<|system|>\n{content}\n<|endoftext|>")
        
        # Add assistant prefix for the response
        prompt_parts.append("<|assistant|>\n")
        
        return "".join(prompt_parts)

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_path": str(self.model_path),
            "context_length": self.context_length,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "n_gpu_layers": self.n_gpu_layers,
            "n_threads": self.n_threads,
        }


def create_llama_cpp_engine(config: Dict[str, Any]) -> LlamaCppEngine:
    """Factory function to create a LlamaCppEngine from configuration.
    
    Args:
        config: Configuration dictionary with LLM settings
        
    Returns:
        Configured LlamaCppEngine instance
    """
    return LlamaCppEngine(
        model_path=config.get("model_path", "/models/llama3.1-8b.Q4_K_M.gguf"),
        context_length=config.get("context_length", 2048),
        temperature=config.get("temperature", 0.8),
        top_p=config.get("top_p", 0.9),
        max_tokens=config.get("max_tokens", 180),
        n_gpu_layers=config.get("n_gpu_layers", -1),
        n_threads=config.get("n_threads"),
        verbose=config.get("verbose", False),
    )


