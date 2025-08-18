"""
frontend/booth/audio_io.py
=========================
Audio I/O utilities for microphone input and speaker output.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Generator, Optional

from .config import config


class AudioDevice:
    """Base class for audio device operations."""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.is_recording = False
        self.is_playing = False
    
    def start_recording(self) -> None:
        """Start recording audio."""
        self.is_recording = True
    
    def stop_recording(self) -> None:
        """Stop recording audio."""
        self.is_recording = False
    
    def start_playback(self) -> None:
        """Start audio playback."""
        self.is_playing = True
    
    def stop_playback(self) -> None:
        """Stop audio playback."""
        self.is_playing = False
    
    def read_audio(self) -> Generator[bytes, None, None]:
        """Read audio data from microphone."""
        raise NotImplementedError
    
    def write_audio(self, audio_data: bytes) -> None:
        """Write audio data to speaker."""
        raise NotImplementedError
    
    def close(self) -> None:
        """Close the audio device."""
        pass


class MockAudioDevice(AudioDevice):
    """Mock audio device for development and testing."""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 1024):
        super().__init__(sample_rate, channels, chunk_size)
        self.recording_buffer = b""
        self.playback_buffer = b""
        self.silence_chunk = b"\x00" * (chunk_size * 2)  # 16-bit audio
    
    def read_audio(self) -> Generator[bytes, None, None]:
        """Generate mock audio data (silence with occasional noise)."""
        while self.is_recording:
            # Simulate some audio input (mostly silence with occasional noise)
            if time.time() % 5 < 0.1:  # Brief noise every 5 seconds
                # Generate some mock audio data
                import random
                noise = bytes([random.randint(0, 255) for _ in range(self.chunk_size * 2)])
                yield noise
            else:
                yield self.silence_chunk
            time.sleep(0.1)  # Simulate real-time audio
    
    def write_audio(self, audio_data: bytes) -> None:
        """Store audio data for playback simulation."""
        if self.is_playing:
            self.playback_buffer += audio_data
            # Simulate playback time
            duration = len(audio_data) / (self.sample_rate * 2)  # 16-bit audio
            time.sleep(duration)
    
    def get_recording_buffer(self) -> bytes:
        """Get the recorded audio buffer."""
        return self.recording_buffer
    
    def clear_recording_buffer(self) -> None:
        """Clear the recording buffer."""
        self.recording_buffer = b""
    
    def get_playback_buffer(self) -> bytes:
        """Get the playback buffer."""
        return self.playback_buffer
    
    def clear_playback_buffer(self) -> None:
        """Clear the playback buffer."""
        self.playback_buffer = b""


class AudioManager:
    """Manages audio input and output devices."""
    
    def __init__(self):
        self.input_device: Optional[AudioDevice] = None
        self.output_device: Optional[AudioDevice] = None
        self.audio_config = config.audio
        self._setup_devices()
    
    def _setup_devices(self) -> None:
        """Set up audio input and output devices."""
        try:
            # Try to use real audio devices if available
            self._setup_real_audio()
        except Exception as e:
            print(f"Warning: Could not set up real audio devices: {e}")
            print("Using mock audio devices for development")
            self._setup_mock_audio()
    
    def _setup_real_audio(self) -> None:
        """Set up real audio devices using PyAudio."""
        try:
            import pyaudio
            
            p = pyaudio.PyAudio()
            
            # Set up input device (microphone)
            self.input_device = RealAudioDevice(
                p,
                is_input=True,
                sample_rate=self.audio_config.get("sample_rate", 16000),
                channels=self.audio_config.get("channels", 1),
                chunk_size=self.audio_config.get("chunk_size", 1024),
                device_index=self.audio_config.get("device")
            )
            
            # Set up output device (speaker)
            self.output_device = RealAudioDevice(
                p,
                is_input=False,
                sample_rate=self.audio_config.get("sample_rate", 16000),
                channels=self.audio_config.get("channels", 1),
                chunk_size=self.audio_config.get("chunk_size", 1024),
                device_index=self.audio_config.get("device")
            )
            
        except ImportError:
            raise Exception("PyAudio not available. Install with: pip install pyaudio")
    
    def _setup_mock_audio(self) -> None:
        """Set up mock audio devices for development."""
        self.input_device = MockAudioDevice(
            sample_rate=self.audio_config.get("sample_rate", 16000),
            channels=self.audio_config.get("channels", 1),
            chunk_size=self.audio_config.get("chunk_size", 1024)
        )
        self.output_device = MockAudioDevice(
            sample_rate=self.audio_config.get("sample_rate", 16000),
            channels=self.audio_config.get("channels", 1),
            chunk_size=self.audio_config.get("chunk_size", 1024)
        )
    
    def start_recording(self) -> None:
        """Start recording from microphone."""
        if self.input_device:
            self.input_device.start_recording()
    
    def stop_recording(self) -> None:
        """Stop recording from microphone."""
        if self.input_device:
            self.input_device.stop_recording()
    
    def start_playback(self) -> None:
        """Start audio playback."""
        if self.output_device:
            self.output_device.start_playback()
    
    def stop_playback(self) -> None:
        """Stop audio playback."""
        if self.output_device:
            self.output_device.stop_playback()
    
    def read_audio(self) -> Generator[bytes, None, None]:
        """Read audio data from microphone."""
        if self.input_device:
            yield from self.input_device.read_audio()
    
    def write_audio(self, audio_data: bytes) -> None:
        """Write audio data to speaker."""
        if self.output_device:
            self.output_device.write_audio(audio_data)
    
    def close(self) -> None:
        """Close all audio devices."""
        if self.input_device:
            self.input_device.close()
        if self.output_device:
            self.output_device.close()


class RealAudioDevice(AudioDevice):
    """Real audio device using PyAudio."""
    
    def __init__(self, pyaudio_instance: Any, is_input: bool, **kwargs):
        super().__init__(**kwargs)
        self.p = pyaudio_instance
        self.is_input = is_input
        self.stream = None
        self.device_index = kwargs.get("device_index")
    
    def start_recording(self) -> None:
        """Start recording audio."""
        if self.is_input:
            self.stream = self.p.open(
                format=self.p.get_format_from_width(2),  # 16-bit
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.chunk_size
            )
            self.is_recording = True
    
    def stop_recording(self) -> None:
        """Stop recording audio."""
        if self.stream and self.is_input:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.is_recording = False
    
    def start_playback(self) -> None:
        """Start audio playback."""
        if not self.is_input:
            self.stream = self.p.open(
                format=self.p.get_format_from_width(2),  # 16-bit
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                output_device_index=self.device_index,
                frames_per_buffer=self.chunk_size
            )
            self.is_playing = True
    
    def stop_playback(self) -> None:
        """Stop audio playback."""
        if self.stream and not self.is_input:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.is_playing = False
    
    def read_audio(self) -> Generator[bytes, None, None]:
        """Read audio data from microphone."""
        if not self.is_input or not self.stream:
            return
        
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                yield data
            except Exception as e:
                print(f"Audio read error: {e}")
                break
    
    def write_audio(self, audio_data: bytes) -> None:
        """Write audio data to speaker."""
        if self.is_input or not self.stream:
            return
        
        try:
            # Write audio data in chunks
            chunk_size = self.chunk_size * 2  # 16-bit audio
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i + chunk_size]
                if len(chunk) < chunk_size:
                    # Pad with silence if needed
                    chunk += b"\x00" * (chunk_size - len(chunk))
                self.stream.write(chunk)
        except Exception as e:
            print(f"Audio write error: {e}")
    
    def close(self) -> None:
        """Close the audio device."""
        if self.is_input:
            self.stop_recording()
        else:
            self.stop_playback()


# Global audio manager instance
audio_manager = AudioManager()


