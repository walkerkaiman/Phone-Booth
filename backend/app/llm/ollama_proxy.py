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

import httpx
import logging
from typing import Dict, Any, Optional, Tuple
from .engine import LanguageModelEngine

logger = logging.getLogger(__name__)

OLLAMA_ENGINE_AVAILABLE = True


class OllamaProxyEngine(LanguageModelEngine):
    """Ollama proxy engine that forwards requests to Ollama server."""
    
    def __init__(self, model_path: str, **kwargs):
        """Initialize the Ollama proxy engine.
        
        Args:
            model_path: The model name (e.g., "llama3.1:8b")
            **kwargs: Additional configuration (base_url, timeout, etc.)
        """
        self.model_name = model_path
        self.base_url = kwargs.get("base_url", "http://localhost:11434")
        self.timeout = kwargs.get("timeout", 30.0)
        
        logger.info(f"Initialized Ollama proxy engine with model: {self.model_name}")
    
    def set_model(self, model_name: str) -> None:
        """Change the model being used for generation.
        
        Args:
            model_name: The new model name (e.g., "phi3:mini")
        """
        self.model_name = model_name
        logger.info(f"Switched Ollama model to: {self.model_name}")
    
    def get_available_models(self) -> list[str]:
        """Get list of available models from Ollama server.
        
        Returns:
            List of available model names
        """
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            logger.error(f"Failed to get available models: {e}")
            return []
    
    def generate(
        self,
        system_prompt: str,
        messages: list[dict],
        max_tokens: int = 180,
        temperature: float = 0.8,
        top_p: float = 0.9,
        model_name: str = None,  # Allow per-request model override
    ) -> Tuple[str, dict]:
        """Generate text using Ollama API.
        
        Args:
            system_prompt: The system prompt
            messages: List of message dictionaries
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            model_name: Optional model override for this request
            
        Returns:
            Tuple of (generated_text, usage_dict)
        """
        # Use provided model or fall back to instance model
        request_model = model_name or self.model_name
        
        try:
            # Build the full prompt from system prompt and messages
            prompt_parts = [system_prompt]
            for message in messages:
                role = message.get("role", "user")
                content = message.get("content", "")
                if role == "user":
                    prompt_parts.append(f"User: {content}")
                elif role == "assistant":
                    prompt_parts.append(f"Assistant: {content}")
            
            full_prompt = "\n\n".join(prompt_parts) + "\n\nAssistant:"
            
            # Prepare the request payload
            payload = {
                "model": request_model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                    "num_predict": max_tokens,
                }
            }
            
            # Make the request to Ollama
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extract the generated text
                generated_text = data.get("response", "")
                
                # Create usage dict
                usage = {
                    "prompt_tokens": data.get("prompt_eval_count", 0),
                    "completion_tokens": data.get("eval_count", 0),
                    "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
                    "total_duration": data.get("total_duration"),
                    "model": data.get("model"),
                }
                
                return generated_text, usage
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API error: {e.response.status_code} - {e.response.text}")
            raise RuntimeError(f"Ollama API error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Ollama connection error: {e}")
            raise RuntimeError(f"Ollama connection error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in Ollama proxy: {e}")
            raise RuntimeError(f"Unexpected error in Ollama proxy: {e}")


