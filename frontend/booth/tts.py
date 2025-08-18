"""
frontend/booth/tts.py
====================
Text-to-speech synthesis using Piper TTS.
"""

from __future__ import annotations

import io
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .config import config


class TTSEngine:
    """Base class for TTS engines."""
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
    
    def synthesize(self, text: str, voice: str) -> Tuple[bytes, Dict[str, Any]]:
        """Synthesize text to speech."""
        raise NotImplementedError
    
    def get_available_voices(self) -> list[str]:
        """Get list of available voices."""
        raise NotImplementedError


class MockTTSEngine(TTSEngine):
    """Mock TTS engine for development and testing."""
    
    def __init__(self, sample_rate: int = 22050):
        super().__init__(sample_rate)
        self.voices = ["en_US-lessac-high", "en_GB-alan-medium", "en_US-lessac-medium"]
    
    def synthesize(self, text: str, voice: str) -> Tuple[bytes, Dict[str, Any]]:
        """Generate mock audio data."""
        # Generate some mock audio data based on text length
        duration = len(text) * 0.1  # Rough estimate: 0.1 seconds per character
        samples = int(duration * self.sample_rate)
        
        # Generate a simple sine wave tone
        import math
        import struct
        
        audio_data = b""
        frequency = 440.0  # A4 note
        amplitude = 0.3
        
        for i in range(samples):
            sample = amplitude * math.sin(2 * math.pi * frequency * i / self.sample_rate)
            # Convert to 16-bit PCM
            sample_int = int(sample * 32767)
            audio_data += struct.pack("<h", sample_int)
        
        # Add some variation based on voice
        if "high" in voice:
            frequency = 660.0  # Higher pitch
        elif "low" in voice:
            frequency = 220.0  # Lower pitch
        
        metadata = {
            "duration": duration,
            "sample_rate": self.sample_rate,
            "voice": voice,
            "text_length": len(text)
        }
        
        return audio_data, metadata
    
    def get_available_voices(self) -> list[str]:
        """Get available mock voices."""
        return self.voices


class PiperTTSEngine(TTSEngine):
    """Piper TTS engine for real text-to-speech synthesis."""
    
    def __init__(self, sample_rate: int = 22050, speed: float = 1.0):
        super().__init__(sample_rate)
        self.speed = speed
        self.models = {}
        self._load_models()
    
    def _load_models(self) -> None:
        """Load Piper TTS models."""
        try:
            import piper
            # Check for actual model files
            models_dir = Path("models")
            available_models = {}
            
            # Check for installed models
            for model_file in models_dir.glob("*.onnx"):
                model_name = model_file.stem
                config_file = model_file.with_suffix(".onnx.json")
                if config_file.exists():
                    available_models[model_name] = str(model_file)
            
            if available_models:
                self.models = available_models
                print(f"✅ Found {len(available_models)} Piper TTS models: {', '.join(available_models.keys())}")
            else:
                # Fallback to mock paths
                self.models = {
                    "en_US-lessac-high": "models/en_US-lessac-high.onnx",
                    "en_GB-alan-medium": "models/en_GB-alan-medium.onnx",
                    "en_US-lessac-medium": "models/en_US-lessac-medium.onnx"
                }
                print("Piper TTS available but no models found - will fall back to mock")
                
        except ImportError:
            print("Warning: Piper TTS not available. Install with: pip install piper-tts")
            self.models = {}
    
    def synthesize(self, text: str, voice: str) -> Tuple[bytes, Dict[str, Any]]:
        """Synthesize text to speech using Piper."""
        if not self.models:
            # Fallback to mock if Piper not available
            mock_engine = MockTTSEngine(self.sample_rate)
            return mock_engine.synthesize(text, voice)
        
        try:
            import piper
            
            # Load the model
            model_path = self.models.get(voice)
            if not model_path:
                raise ValueError(f"Voice not found: {voice}")
            
            # Load voice directly (newer Piper API)
            voice_model = piper.PiperVoice.load(model_path)
            
            # Configure synthesis
            synthesis_config = piper.SynthesisConfig()
            synthesis_config.length_scale = 1.0 / self.speed  # Inverse relationship
            
            # Synthesize - returns AudioChunk objects
            audio_chunks = voice_model.synthesize(text, synthesis_config)
            
            # Convert AudioChunk objects to bytes
            audio_data = b""
            for chunk in audio_chunks:
                audio_data += chunk.audio_int16_bytes
            
            metadata = {
                "duration": len(audio_data) / (self.sample_rate * 2),  # 16-bit audio
                "sample_rate": self.sample_rate,
                "voice": voice,
                "text_length": len(text)
            }
            
            return audio_data, metadata
            
        except Exception as e:
            print(f"Piper TTS error: {e}")
            # Fallback to mock
            mock_engine = MockTTSEngine(self.sample_rate)
            return mock_engine.synthesize(text, voice)
    
    def get_available_voices(self) -> list[str]:
        """Get available Piper voices."""
        return list(self.models.keys())


class TTSManager:
    """Manages text-to-speech synthesis."""
    
    def __init__(self):
        self.tts_config = config.tts
        self.engine = self._create_engine()
        self.voice_map = self.tts_config.get("voice_map", {})
    
    def _create_engine(self) -> TTSEngine:
        """Create the appropriate TTS engine."""
        try:
            # Try to use Piper TTS
            return PiperTTSEngine(
                sample_rate=self.tts_config.get("sample_rate", 22050),
                speed=self.tts_config.get("speed", 1.0)
            )
        except Exception as e:
            print(f"Warning: Could not initialize Piper TTS: {e}")
            print("Using mock TTS engine")
            return MockTTSEngine(
                sample_rate=self.tts_config.get("sample_rate", 22050)
            )
    
    def get_voice_for_personality(self, personality: str) -> str:
        """Get the appropriate voice for a personality."""
        return self.voice_map.get(personality, "en_US-lessac-high")
    
    def synthesize(self, text: str, personality: str) -> Tuple[bytes, Dict[str, Any]]:
        """Synthesize text to speech for a personality."""
        voice = self.get_voice_for_personality(personality)
        return self.engine.synthesize(text, voice)
    
    def get_available_voices(self) -> list[str]:
        """Get available voices."""
        return self.engine.get_available_voices()
    
    def get_amplitude_envelope(self, audio_data: bytes) -> list[float]:
        """Extract amplitude envelope from audio data for lighting control."""
        import struct
        
        # Convert bytes to samples
        samples = []
        for i in range(0, len(audio_data), 2):
            if i + 1 < len(audio_data):
                sample = struct.unpack("<h", audio_data[i:i+2])[0]
                samples.append(abs(sample) / 32767.0)  # Normalize to 0-1
        
        if not samples:
            return [0.0]
        
        # Calculate amplitude envelope
        envelope = []
        window_size = max(1, len(samples) // 100)  # 100 envelope points
        
        for i in range(0, len(samples), window_size):
            window = samples[i:i + window_size]
            amplitude = sum(window) / len(window)
            envelope.append(amplitude)
        
        return envelope


# Global TTS manager instance
tts_manager = TTSManager()


