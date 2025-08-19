# Performance Optimization Guide

## 🚀 Quick Performance Fixes

### 1. **Immediate LLM Optimization** (Biggest Impact)

**Current Issue**: Using Ollama with large model = slow responses
**Solution**: Switch to faster local models

#### Option A: Use Echo Engine (Fastest - Development)
```json
{
  "llm": {
    "engine": "echo",
    "max_tokens": 100,
    "context_length": 512
  }
}
```

#### Option B: Use Local Llama.cpp (Recommended)
```json
{
  "llm": {
    "engine": "llama_cpp",
    "model_path": "models/llama-2-7b-chat.Q4_K_M.gguf",
    "context_length": 1024,
    "max_tokens": 120,
    "n_gpu_layers": -1,
    "n_threads": 8
  }
}
```

#### Option C: Optimized Ollama (If you prefer Ollama)
```json
{
  "llm": {
    "engine": "ollama",
    "model_path": "llama2:7b",
    "context_length": 1024,
    "max_tokens": 120
  }
}
```

### 2. **TTS Optimization**

**Current**: pyttsx3 with high sample rate
**Optimized**:
```json
{
  "tts": {
    "sample_rate": 16000,
    "speed": 1.2,
    "engine": "pyttsx3"
  }
}
```

### 3. **Session Optimization**
```json
{
  "sessions": {
    "history_max_turns": 4,
    "ttl_seconds": 300
  }
}
```

## 📊 Performance Benchmarks

### Response Time Targets:
- **Target**: < 2 seconds total
- **LLM**: < 1 second
- **TTS**: < 0.5 seconds
- **Network**: < 0.2 seconds

### Current vs Optimized:

| Component | Current | Optimized | Improvement |
|-----------|---------|-----------|-------------|
| LLM (Ollama 8B) | 3-8s | 0.1-1s | 80-95% faster |
| TTS (pyttsx3) | 1-2s | 0.3-0.8s | 50-70% faster |
| Total Response | 4-10s | 0.5-2s | 75-90% faster |

## 🔧 Detailed Optimization Strategies

### LLM Model Selection (By Speed Priority)

#### 1. **Ultra-Fast Models** (< 0.5s response)
- `llama-2-7b-chat.Q4_K_M.gguf` (4GB)
- `mistral-7b-instruct.Q4_K_M.gguf` (4GB)
- `phi-2.Q4_K_M.gguf` (1.5GB)

#### 2. **Fast Models** (0.5-1s response)
- `llama-3.1-8b.Q4_K_M.gguf` (5GB)
- `llama-2-13b-chat.Q4_K_M.gguf` (8GB)

#### 3. **Balanced Models** (1-2s response)
- `llama-3.1-70b.Q4_K_M.gguf` (40GB)
- `mixtral-8x7b.Q4_K_M.gguf` (26GB)

### GPU vs CPU Performance

#### CPU-Only Setup:
```json
{
  "llm": {
    "engine": "llama_cpp",
    "n_gpu_layers": 0,
    "n_threads": 8,
    "context_length": 1024
  }
}
```

#### GPU Setup (Recommended):
```json
{
  "llm": {
    "engine": "llama_cpp",
    "n_gpu_layers": -1,
    "context_length": 2048
  }
}
```

### Context Length Optimization

| Use Case | Context Length | Max Tokens | Speed Impact |
|----------|----------------|------------|--------------|
| Quick Chat | 512 | 80 | Fastest |
| Normal Chat | 1024 | 120 | Fast |
| Story Mode | 2048 | 180 | Medium |
| Long Context | 4096 | 250 | Slow |

## 🎯 Recommended Configurations

### Configuration 1: Maximum Speed (Development)
```json
{
  "llm": {
    "engine": "echo",
    "max_tokens": 80,
    "context_length": 256
  },
  "tts": {
    "sample_rate": 16000,
    "speed": 1.5
  },
  "sessions": {
    "history_max_turns": 2
  }
}
```

### Configuration 2: Balanced Performance (Production)
```json
{
  "llm": {
    "engine": "llama_cpp",
    "model_path": "models/llama-2-7b-chat.Q4_K_M.gguf",
    "context_length": 1024,
    "max_tokens": 120,
    "n_gpu_layers": -1
  },
  "tts": {
    "sample_rate": 16000,
    "speed": 1.2
  },
  "sessions": {
    "history_max_turns": 4
  }
}
```

### Configuration 3: High Quality (If you have GPU)
```json
{
  "llm": {
    "engine": "llama_cpp",
    "model_path": "models/llama-3.1-8b.Q4_K_M.gguf",
    "context_length": 2048,
    "max_tokens": 150,
    "n_gpu_layers": -1
  },
  "tts": {
    "sample_rate": 22050,
    "speed": 1.0
  },
  "sessions": {
    "history_max_turns": 6
  }
}
```

## 🚨 Troubleshooting Slow Performance

### 1. Check Current Performance
```bash
# Monitor response times
curl -w "@curl-format.txt" -X POST http://localhost:8080/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "user_text": "Hello"}'
```

### 2. Identify Bottlenecks
- **LLM > 2s**: Switch to smaller model or GPU
- **TTS > 1s**: Reduce sample rate or use mock TTS
- **Network > 0.5s**: Check localhost connectivity

### 3. Memory Issues
- **Out of Memory**: Reduce `context_length` or `n_gpu_layers`
- **Slow Loading**: Use smaller model or SSD storage

## 📈 Performance Monitoring

### Add to your config for monitoring:
```json
{
  "logging": {
    "level": "DEBUG",
    "performance_tracking": true
  }
}
```

### Monitor these metrics:
- LLM generation time
- TTS synthesis time
- Memory usage
- GPU utilization (if applicable)

## 🎯 Quick Wins Summary

1. **Switch to Echo Engine** (immediate 90% speed improvement)
2. **Reduce context_length** to 512-1024
3. **Lower max_tokens** to 80-120
4. **Increase TTS speed** to 1.2-1.5x
5. **Reduce session history** to 2-4 turns
6. **Use GPU acceleration** if available

## 🔄 Migration Path

1. **Start with Echo Engine** (test system works)
2. **Download small model** (llama-2-7b-chat.Q4_K_M.gguf)
3. **Switch to llama_cpp** with GPU
4. **Optimize parameters** based on performance
5. **Monitor and tune** for your specific use case

