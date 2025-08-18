# Piper TTS Setup Guide

## Overview
This guide covers the installation and configuration of Piper TTS (Text-to-Speech) models for the Phone Booth System.

## ✅ Installation Complete

### Installed Models
- **en_US-lessac-high**: High-quality US English voice (109MB)
- **en_GB-alan-medium**: Medium-quality British English voice (60MB)

### Model Locations
```
models/
├── en_US-lessac-high.onnx          # High-quality US voice model
├── en_US-lessac-high.onnx.json     # Model configuration
├── en_GB-alan-medium.onnx          # British voice model  
└── en_GB-alan-medium.onnx.json     # Model configuration
```

## Voice Mapping
The system maps personalities to specific voices:

| Personality | Voice | Description |
|-------------|-------|-------------|
| trickster | en_US-lessac-high | High-quality US English |
| sage | en_GB-alan-medium | British English |
| muse | en_US-lessac-high | High-quality US English |
| jester | en_GB-alan-medium | British English |
| night_watch | en_US-lessac-high | High-quality US English |

## Installation Scripts

### Windows
```batch
scripts\install_piper_models.bat
```

### macOS/Linux
```bash
scripts/install_piper_models.sh
```

### Python Script
```bash
python scripts/install_piper_models.py
```

## Available Models

### List All Models
```bash
python scripts/install_piper_models.py --list
```

### Install Specific Models
```bash
python scripts/install_piper_models.py --models en_US-lessac-high en_GB-alan-medium
```

### Install All Models
```bash
python scripts/install_piper_models.py
```

## Model Details

### en_US-lessac-high
- **Size**: 109MB
- **Quality**: High
- **Language**: US English
- **Voice**: Lessac (natural, expressive)
- **Use Case**: Primary US English voice

### en_GB-alan-medium  
- **Size**: 60MB
- **Quality**: Medium
- **Language**: British English
- **Voice**: Alan (clear, professional)
- **Use Case**: British accent variety

### Additional Available Models
- **en_US-lessac-medium**: Medium-quality US English (smaller file)
- **en_US-amy-low**: Low-quality US English (fastest, smallest)

## Testing

### Test TTS System
```python
from frontend.booth.tts import TTSManager

# Create TTS manager
tts = TTSManager()

# Test US voice
audio, meta = tts.synthesize("Hello! This is a test.", "trickster")
print(f"US Voice: {meta['voice']}, Duration: {meta['duration']:.2f}s")

# Test British voice  
audio, meta = tts.synthesize("Hello! This is a test.", "sage")
print(f"British Voice: {meta['voice']}, Duration: {meta['duration']:.2f}s")
```

### Expected Output
```
✅ Found 2 Piper TTS models: en_GB-alan-medium, en_US-lessac-high
US Voice: en_US-lessac-high, Duration: 3.59s
British Voice: en_GB-alan-medium, Duration: 2.91s
```

## Web UI Integration

### Automatic Detection
The system automatically detects installed models and uses them:
- ✅ Real Piper TTS when models are available
- ✅ Graceful fallback to mock TTS if models are missing
- ✅ No configuration changes needed

### Testing in Web UI
1. Start the system: `start_system.bat`
2. Open: http://localhost:5000
3. Pick up the phone
4. Select different personalities to hear different voices
5. Type messages to test TTS quality

## Performance

### Audio Quality
- **High-quality models**: Natural, expressive speech
- **Medium-quality models**: Good balance of quality and speed
- **Low-quality models**: Fast synthesis, smaller files

### Synthesis Speed
- **Real-time capable**: Fast enough for interactive use
- **Memory efficient**: Models loaded on-demand
- **CPU optimized**: Efficient inference

## Troubleshooting

### Common Issues

#### "Piper TTS not available"
```bash
pip install piper-tts
```

#### "No models found"
```bash
python scripts/install_piper_models.py
```

#### "Model file not found"
- Check `models/` directory exists
- Verify `.onnx` and `.onnx.json` files are present
- Re-run installer if files are missing

#### "Audio synthesis failed"
- Check model file integrity
- Verify Piper TTS installation
- Check system memory availability

### Fallback Behavior
The system gracefully falls back to mock TTS if:
- Piper TTS is not installed
- Model files are missing
- Synthesis fails for any reason

## Next Steps

### Adding More Models
1. Edit `scripts/install_piper_models.py`
2. Add new model definitions to `MODELS` dictionary
3. Run installer with new model names

### Custom Voice Mapping
1. Edit `config/frontend.json`
2. Update `tts.voice_map` section
3. Restart web UI

### Performance Tuning
- Use lower-quality models for faster synthesis
- Adjust sample rate in configuration
- Optimize for specific hardware

## Resources

### Official Documentation
- [Piper TTS GitHub](https://github.com/rhasspy/piper)
- [Piper Voices Repository](https://huggingface.co/rhasspy/piper-voices)

### Model Sources
- [Hugging Face Piper Voices](https://huggingface.co/rhasspy/piper-voices)
- [Community Models](https://github.com/rhasspy/piper-voices)

### Support
- Check system logs for detailed error messages
- Verify all dependencies are installed
- Test with simple text first
