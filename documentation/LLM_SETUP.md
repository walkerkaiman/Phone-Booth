# LLM Engine Setup Guide

This guide explains how to set up and configure the LLM engine for the Character Booth System backend.

## Overview

The backend supports multiple LLM engines:
- **EchoEngine**: Development/testing (echoes user input)
- **LlamaCppEngine**: Local inference with llama-cpp-python
- **OllamaEngine**: Remote inference via Ollama API

## Quick Start

### 1. Install Dependencies

```bash
# Install backend dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Engine

Edit `config/backend.json`:
```json
{
  "llm": {
    "engine": "llama_cpp",
    "model_path": "/path/to/your/model.gguf",
    "context_length": 2048,
    "temperature": 0.8,
    "top_p": 0.9,
    "max_tokens": 180,
    "n_gpu_layers": -1
  }
}
```

### 3. Download a Model

Download a GGUF model file and update the `model_path` in your config.

## LlamaCppEngine Setup

### Prerequisites

- Python 3.10+
- llama-cpp-python installed
- GGUF model file

### Installation

```bash
# Install llama-cpp-python
pip install llama-cpp-python

# For GPU support (CUDA)
pip install llama-cpp-python --force-reinstall --index-url https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118

# For CPU-only
pip install llama-cpp-python --force-reinstall --index-url https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cpu
```

### Model Recommendations

**Small Models (2-4GB, Fast):**
- `llama-2-7b.Q4_K_M.gguf`
- `llama-3.1-8b.Q4_K_M.gguf`
- `mistral-7b-instruct-v0.2.Q4_K_M.gguf`

**Medium Models (7-13GB, Balanced):**
- `llama-2-13b.Q4_K_M.gguf`
- `llama-3.1-70b.Q4_K_M.gguf`
- `mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf`

**Large Models (20GB+, High Quality):**
- `llama-2-70b.Q4_K_M.gguf`
- `llama-3.1-405b.Q4_K_M.gguf`

### Configuration Options

```json
{
  "llm": {
    "engine": "llama_cpp",
    "model_path": "/models/llama-3.1-8b.Q4_K_M.gguf",
    "context_length": 2048,        // Maximum context length
    "temperature": 0.8,            // 0.0-2.0, higher = more creative
    "top_p": 0.9,                  // 0.0-1.0, nucleus sampling
    "max_tokens": 180,             // Maximum tokens to generate
    "n_gpu_layers": -1,            // -1=all layers, 0=CPU only, N=first N layers
    "n_threads": null,             // CPU threads (null=auto)
    "verbose": false               // Enable llama-cpp logging
  }
}
```

### Performance Tuning

**CPU-Only Setup:**
```json
{
  "llm": {
    "engine": "llama_cpp",
    "model_path": "/models/llama-3.1-8b.Q4_K_M.gguf",
    "n_gpu_layers": 0,
    "n_threads": 8,
    "context_length": 1024
  }
}
```

**GPU Setup (NVIDIA):**
```json
{
  "llm": {
    "engine": "llama_cpp",
    "model_path": "/models/llama-3.1-8b.Q4_K_M.gguf",
    "n_gpu_layers": -1,
    "context_length": 2048
  }
}
```

**Memory-Constrained Setup:**
```json
{
  "llm": {
    "engine": "llama_cpp",
    "model_path": "/models/llama-3.1-8b.Q4_K_M.gguf",
    "context_length": 512,
    "max_tokens": 100,
    "n_gpu_layers": 10
  }
}
```

## Model Sources

### Hugging Face
```bash
# Download from Hugging Face
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
```

### Ollama
```bash
# Pull model with Ollama
ollama pull llama2:7b
# Then copy the model file from Ollama's storage
```

### Direct Downloads
- [TheBloke's GGUF Models](https://huggingface.co/TheBloke)
- [Hugging Face GGUF Models](https://huggingface.co/models?search=gguf)

## Testing Your Setup

### 1. Test Engine Factory
```bash
python test_llama_engine.py
```

### 2. Test Backend API
```bash
# Start backend
./backend/run_backend.sh

# Test health endpoint
curl http://localhost:8080/healthz

# Test generation endpoint
curl -X POST http://localhost:8080/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "user_text": "Hello, how are you?",
    "personality": "trickster"
  }'
```

## Troubleshooting

### Common Issues

**1. Model File Not Found**
```
FileNotFoundError: Model file not found: /path/to/model.gguf
```
**Solution:** Verify the model path in `config/backend.json`

**2. Import Error**
```
ImportError: llama-cpp-python is not installed
```
**Solution:** Install llama-cpp-python: `pip install llama-cpp-python`

**3. CUDA/GPU Issues**
```
RuntimeError: CUDA error
```
**Solution:** Install GPU version: `pip install llama-cpp-python --force-reinstall --index-url https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118`

**4. Out of Memory**
```
RuntimeError: CUDA out of memory
```
**Solution:** Reduce `n_gpu_layers` or use a smaller model

**5. Slow Performance**
**Solutions:**
- Use GPU acceleration (`n_gpu_layers: -1`)
- Reduce `context_length`
- Use a smaller model
- Increase `n_threads` for CPU-only

### Performance Benchmarks

**CPU Performance (Intel i7-12700K):**
- llama-2-7b.Q4_K_M: ~15-20 tokens/second
- llama-2-13b.Q4_K_M: ~8-12 tokens/second

**GPU Performance (RTX 4090):**
- llama-2-7b.Q4_K_M: ~80-120 tokens/second
- llama-2-13b.Q4_K_M: ~40-60 tokens/second

## Advanced Configuration

### Custom Prompt Formatting

The engine uses a custom prompt format. You can modify `_build_prompt()` in `llama_cpp_engine.py`:

```python
def _build_prompt(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
    # Custom prompt formatting for your model
    prompt = f"<|system|>\n{system_prompt}\n<|endoftext|>"
    
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        
        if role == "user":
            prompt += f"\n<|user|>\n{content}\n<|endoftext|>"
        elif role == "assistant":
            prompt += f"\n<|assistant|>\n{content}\n<|endoftext|>"
    
    prompt += "\n<|assistant|>\n"
    return prompt
```

### Model-Specific Tuning

**For Llama 2:**
```json
{
  "llm": {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 150
  }
}
```

**For Mistral:**
```json
{
  "llm": {
    "temperature": 0.8,
    "top_p": 0.95,
    "max_tokens": 200
  }
}
```

## Security Considerations

1. **Model Safety**: Ensure your model has appropriate safety guardrails
2. **Input Validation**: The API validates all inputs
3. **Resource Limits**: Set appropriate `max_tokens` and `context_length`
4. **Network Security**: Use HTTPS in production

## Next Steps

1. **Test with EchoEngine**: Start with `"engine": "echo"` for development
2. **Download a Model**: Get a GGUF model file
3. **Configure GPU**: Set up GPU acceleration if available
4. **Tune Parameters**: Adjust temperature, top_p, and max_tokens
5. **Monitor Performance**: Check response times and memory usage
