"""
frontend/booth/state.py
======================
State management for the booth application.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class BoothState(Enum):
    """Booth state machine states."""
    IDLE = "idle"
    PICKUP = "pickup"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    HANGUP = "hangup"
    ERROR = "error"


@dataclass
class SessionInfo:
    """Session information for backend communication."""
    session_id: str
    booth_id: str
    personality: str
    mode: str
    created_at: float
    last_activity: float
    
    @classmethod
    def create(cls, booth_id: str, personality: str, mode: str = "chat") -> SessionInfo:
        """Create a new session."""
        now = time.time()
        return cls(
            session_id=str(uuid4()),
            booth_id=booth_id,
            personality=personality,
            mode=mode,
            created_at=now,
            last_activity=now
        )
    
    def update_activity(self) -> None:
        """Update the last activity timestamp."""
        self.last_activity = time.time()


@dataclass
class AudioBuffer:
    """Audio buffer for processing."""
    data: bytes = field(default_factory=bytes)
    sample_rate: int = 16000
    channels: int = 1
    timestamp: float = field(default_factory=time.time)
    
    def append(self, chunk: bytes) -> None:
        """Append audio data to the buffer."""
        self.data += chunk
        self.timestamp = time.time()
    
    def clear(self) -> None:
        """Clear the buffer."""
        self.data = bytes()
        self.timestamp = time.time()
    
    def get_duration(self) -> float:
        """Get the duration of the audio in seconds."""
        if not self.data:
            return 0.0
        # Calculate duration based on sample rate and data size
        bytes_per_sample = 2  # 16-bit audio
        total_samples = len(self.data) // bytes_per_sample
        return total_samples / self.sample_rate


@dataclass
class SceneInfo:
    """Scene information from camera capture."""
    caption: str
    tags: List[str]
    timestamp: float
    image_data: Optional[bytes] = None
    
    @classmethod
    def create(cls, caption: str, tags: List[str], image_data: Optional[bytes] = None) -> SceneInfo:
        """Create a new scene info."""
        return cls(
            caption=caption,
            tags=tags,
            timestamp=time.time(),
            image_data=image_data
        )


@dataclass
class ConversationTurn:
    """A single turn in the conversation."""
    user_text: str
    assistant_text: str
    scene: Optional[SceneInfo]
    timestamp: float
    processing_time: float
    
    @classmethod
    def create(cls, user_text: str, assistant_text: str, scene: Optional[SceneInfo], processing_time: float) -> ConversationTurn:
        """Create a new conversation turn."""
        return cls(
            user_text=user_text,
            assistant_text=assistant_text,
            scene=scene,
            timestamp=time.time(),
            processing_time=processing_time
        )


class BoothStateManager:
    """Manages the state of the booth application."""
    
    def __init__(self):
        self.state = BoothState.IDLE
        self.session: Optional[SessionInfo] = None
        self.audio_buffer = AudioBuffer()
        self.current_scene: Optional[SceneInfo] = None
        self.conversation_history: List[ConversationTurn] = []
        self.error_message: Optional[str] = None
        self.stats = {
            "total_conversations": 0,
            "total_turns": 0,
            "total_processing_time": 0.0,
            "start_time": time.time()
        }
    
    def transition_to(self, new_state: BoothState, error_message: Optional[str] = None) -> None:
        """Transition to a new state."""
        old_state = self.state
        self.state = new_state
        self.error_message = error_message
        
        print(f"State transition: {old_state.value} -> {new_state.value}")
        if error_message:
            print(f"Error: {error_message}")
    
    def start_session(self, booth_id: str, personality: str, mode: str = "chat") -> SessionInfo:
        """Start a new session."""
        self.session = SessionInfo.create(booth_id, personality, mode)
        self.stats["total_conversations"] += 1
        return self.session
    
    def end_session(self) -> None:
        """End the current session."""
        self.session = None
        self.audio_buffer.clear()
        self.current_scene = None
        self.conversation_history.clear()
    
    def add_conversation_turn(self, turn: ConversationTurn) -> None:
        """Add a conversation turn to history."""
        self.conversation_history.append(turn)
        self.stats["total_turns"] += 1
        self.stats["total_processing_time"] += turn.processing_time
        
        # Keep only recent history (last 10 turns)
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def update_scene(self, scene: SceneInfo) -> None:
        """Update the current scene."""
        self.current_scene = scene
    
    def get_session_age(self) -> float:
        """Get the age of the current session in seconds."""
        if not self.session:
            return 0.0
        return time.time() - self.session.created_at
    
    def get_idle_time(self) -> float:
        """Get the idle time since last activity in seconds."""
        if not self.session:
            return 0.0
        return time.time() - self.session.last_activity
    
    def is_session_expired(self, max_age_seconds: int = 600) -> bool:
        """Check if the session has expired."""
        return self.get_session_age() > max_age_seconds
    
    def is_idle_too_long(self, max_idle_seconds: int = 300) -> bool:
        """Check if the session has been idle too long."""
        return self.get_idle_time() > max_idle_seconds
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        uptime = time.time() - self.stats["start_time"]
        avg_processing_time = (
            self.stats["total_processing_time"] / self.stats["total_turns"]
            if self.stats["total_turns"] > 0 else 0.0
        )
        
        return {
            **self.stats,
            "uptime_seconds": uptime,
            "avg_processing_time": avg_processing_time,
            "current_state": self.state.value,
            "session_active": self.session is not None,
            "conversation_history_length": len(self.conversation_history)
        }
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "total_conversations": 0,
            "total_turns": 0,
            "total_processing_time": 0.0,
            "start_time": time.time()
        }


