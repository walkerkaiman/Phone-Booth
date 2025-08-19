"""
frontend/booth/tts.py
====================
Ultra-fast text-to-speech synthesis using edge-tts for real speech.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple


class EdgeTTSEngine:
    """Ultra-fast TTS engine using Microsoft Edge TTS for real speech."""
    
    def __init__(self):
        self.sample_rate = 16000
        self.voices = ["en-US-JennyNeural", "en-US-GuyNeural", "en-GB-RyanNeural"]
        
        # Personality to voice mapping
        self.personality_voices = {
            "trickster": "en-US-JennyNeural",  # Energetic, playful
            "sage": "en-GB-RyanNeural",        # Wise, contemplative
            "muse": "en-US-JennyNeural",       # Creative, inspiring
            "jester": "en-US-GuyNeural",       # Fast, humorous
            "night_watch": "en-GB-RyanNeural"  # Mysterious, deep
        }
    
    def synthesize(self, text: str, personality: str = None) -> Tuple[bytes, Dict[str, Any]]:
        """Generate real speech using edge-tts."""
        try:
            # Use personality-specific voice or default
            voice = self.personality_voices.get(personality, "en-US-JennyNeural")
            
            # Generate audio using edge-tts
            audio_data = self._synthesize_sync(text, voice)
            
            # Calculate duration (rough estimate)
            duration = len(text) * 0.06  # ~0.06 seconds per character
            
            metadata = {
                "duration": duration,
                "sample_rate": self.sample_rate,
                "voice": voice,
                "text_length": len(text),
                "engine": "edge_tts",
                "personality": personality
            }
            
            return audio_data, metadata
            
        except Exception as e:
            print(f"Edge TTS error: {e}")
            # Fallback to fast mock
            return self._fallback_synthesize(text, personality)
    
    def _synthesize_sync(self, text: str, voice: str) -> bytes:
        """Synchronous TTS synthesis using edge-tts."""
        try:
            import subprocess
            import tempfile
            import os
            
            # Create temporary file for output (WAV format)
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            try:
                # Use edge-tts command line tool with correct format
                cmd = [
                    "python", "-m", "edge_tts",
                    "--voice", voice,
                    "--text", text,
                    "--write-media", temp_filename
                ]
                
                print(f"Running edge-tts command: {' '.join(cmd)}")
                
                # Run the command
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                
                print(f"Edge TTS stdout: {result.stdout}")
                print(f"Edge TTS stderr: {result.stderr}")
                print(f"Edge TTS return code: {result.returncode}")
                
                if result.returncode == 0 and os.path.exists(temp_filename):
                    # Read the generated audio file
                    with open(temp_filename, 'rb') as f:
                        audio_data = f.read()
                    
                    print(f"Generated audio file size: {len(audio_data)} bytes")
                    return audio_data
                else:
                    print(f"Edge TTS command failed: {result.stderr}")
                    raise Exception(f"Edge TTS synthesis failed: {result.stderr}")
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
            
        except ImportError:
            print("edge-tts not available. Install with: pip install edge-tts")
            raise
        except Exception as e:
            print(f"Edge TTS synthesis error: {e}")
            raise
    
    def _fallback_synthesize(self, text: str, personality: str = None) -> Tuple[bytes, Dict[str, Any]]:
        """Fallback to fast mock TTS if edge-tts fails."""
        # Calculate duration based on text length (very fast)
        duration = len(text) * 0.04  # 0.04 seconds per character (very fast)
        
        # Generate minimal audio data (just enough for the web UI to play)
        import math
        import struct
        
        samples = int(duration * self.sample_rate)
        audio_data = b""
        
        # Simple sine wave with personality-based frequency
        base_freq = 440.0
        if personality == "trickster":
            base_freq = 500.0  # Higher, energetic
        elif personality == "sage":
            base_freq = 380.0  # Lower, wise
        elif personality == "muse":
            base_freq = 460.0  # Creative
        elif personality == "jester":
            base_freq = 520.0  # Fast, humorous
        elif personality == "night_watch":
            base_freq = 400.0  # Mysterious
        
        # Generate minimal audio (just a short tone)
        for i in range(min(samples, 8000)):  # Limit to 0.5 seconds max
            sample = 0.3 * math.sin(2 * math.pi * base_freq * i / self.sample_rate)
            sample_int = int(sample * 32767)
            audio_data += struct.pack("<h", sample_int)
        
        # Convert to WAV format (minimal header)
        wav_data = self._pcm_to_wav(audio_data, self.sample_rate)
        
        metadata = {
            "duration": duration,
            "sample_rate": self.sample_rate,
            "voice": "fallback_default",
            "text_length": len(text),
            "engine": "fallback_tts",
            "personality": personality
        }
        
        return wav_data, metadata
    
    def _pcm_to_wav(self, pcm_data: bytes, sample_rate: int) -> bytes:
        """Convert PCM to WAV with minimal processing."""
        import struct
        
        channels = 1
        bits_per_sample = 16
        byte_rate = sample_rate * channels * bits_per_sample // 8
        block_align = channels * bits_per_sample // 8
        data_size = len(pcm_data)
        file_size = 36 + data_size
        
        wav_header = struct.pack('<4sI4s4sIHHIIHH4sI',
            b'RIFF', file_size, b'WAVE', b'fmt ', 16, 1, channels,
            sample_rate, byte_rate, block_align, bits_per_sample,
            b'data', data_size
        )
        
        return wav_header + pcm_data
    
    def get_available_voices(self) -> list[str]:
        return list(self.personality_voices.values())


class TTSManager:
    """Ultra-fast TTS manager with real speech synthesis."""
    
    def __init__(self):
        self.engine = EdgeTTSEngine()
    
    def synthesize(self, text: str, personality: str) -> Tuple[bytes, Dict[str, Any]]:
        """Ultra-fast speech synthesis with real speech."""
        return self.engine.synthesize(text, personality)
    
    def get_available_voices(self) -> list[str]:
        return self.engine.get_available_voices()
    
    def get_personality_settings(self, personality: str = None) -> Dict[str, Any]:
        return {}
    
    def get_all_personality_settings(self) -> Dict[str, Any]:
        return {}
    
    def get_amplitude_envelope(self, audio_data: bytes) -> list[float]:
        """Ultra-fast amplitude envelope (simplified)."""
        # Return a simple envelope for lighting
        return [0.5, 0.7, 0.3, 0.8, 0.4, 0.6, 0.2, 0.9, 0.5, 0.3]


# Global TTS manager instance
tts_manager = TTSManager()


