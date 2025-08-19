"""
frontend/booth/net.py
====================
HTTP client for communicating with the backend API.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from .config import config
from .state import SessionInfo, SceneInfo


class BackendClient:
    """HTTP client for backend API communication."""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.backend_url
        self.client = httpx.Client(timeout=30.0)
        self.session_retries = config.session.get("max_retries", 3)
        self.retry_delay = config.session.get("retry_delay_s", 1.0)
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an HTTP request to the backend."""
        url = urljoin(self.base_url, endpoint)
        
        try:
            if method.upper() == "GET":
                response = self.client.get(url)
            elif method.upper() == "POST":
                response = self.client.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise SessionNotFoundError(f"Session not found: {e.response.text}")
            elif e.response.status_code >= 500:
                raise BackendError(f"Backend server error: {e.response.text}")
            else:
                raise BackendError(f"HTTP {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise BackendError(f"Network error: {e}")
        except json.JSONDecodeError as e:
            raise BackendError(f"Invalid JSON response: {e}")
    
    def health_check(self) -> bool:
        """Check if the backend is healthy."""
        try:
            response = self._make_request("GET", "/healthz")
            return response.get("ok", False)
        except Exception:
            return False
    
    def start_session(self, session: SessionInfo) -> bool:
        """Start a new session with the backend."""
        data = {
            "session_id": session.session_id,
            "booth_id": session.booth_id,
            "personality": session.personality,
            "mode": session.mode
        }
        
        for attempt in range(self.session_retries):
            try:
                response = self._make_request("POST", "/v1/session/start", data)
                print(f"Session started: {session.session_id}")
                return True
            except SessionNotFoundError:
                # Session already exists, try to continue
                print(f"Session already exists: {session.session_id}")
                return True
            except BackendError as e:
                if attempt < self.session_retries - 1:
                    print(f"Session start attempt {attempt + 1} failed: {e}")
                    time.sleep(self.retry_delay)
                else:
                    print(f"Failed to start session after {self.session_retries} attempts: {e}")
                    raise
        
        return False
    
    def generate_response(
        self,
        session: SessionInfo,
        user_text: str,
        scene: Optional[SceneInfo] = None,
        personality: Optional[str] = None,
        mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a response from the backend."""
        # Prepare scene data
        scene_data = None
        if scene:
            scene_data = {
                "caption": scene.caption,
                "tags": scene.tags
            }
        
        data = {
            "session_id": session.session_id,
            "user_text": user_text,
            "scene": scene_data
        }
        
        # Add optional overrides
        if personality:
            data["personality"] = personality
        if mode:
            data["mode"] = mode
        
        for attempt in range(self.session_retries):
            try:
                response = self._make_request("POST", "/v1/generate", data)
                return response
            except SessionNotFoundError:
                # Session expired, need to restart
                print(f"Session expired, restarting: {session.session_id}")
                if self.start_session(session):
                    # Retry the generation
                    continue
                else:
                    raise BackendError("Failed to restart expired session")
            except BackendError as e:
                if attempt < self.session_retries - 1:
                    print(f"Generation attempt {attempt + 1} failed: {e}")
                    time.sleep(self.retry_delay)
                else:
                    print(f"Failed to generate response after {self.session_retries} attempts: {e}")
                    raise
        
        raise BackendError("Failed to generate response")
    
    def release_session(self, session_id: str) -> bool:
        """Release a session with the backend."""
        data = {"session_id": session_id}
        
        try:
            response = self._make_request("POST", "/v1/session/release", data)
            print(f"Session released: {session_id}")
            return True
        except BackendError as e:
            print(f"Failed to release session {session_id}: {e}")
            return False
    
    def get_models(self) -> Dict[str, Any]:
        """Get available models and current model."""
        try:
            response = self._make_request("GET", "/v1/models")
            return response
        except BackendError as e:
            print(f"Failed to get models: {e}")
            return {
                "models": [],
                "current_model": "unknown",
                "engine_type": "unknown"
            }
    
    def switch_model(self, model_name: str) -> Dict[str, Any]:
        """Switch to a different model."""
        data = {"model_name": model_name}
        
        try:
            response = self._make_request("POST", "/v1/models/switch", data)
            print(f"Switched to model: {model_name}")
            return response
        except BackendError as e:
            print(f"Failed to switch model to {model_name}: {e}")
            raise
    
    def get_current_model(self) -> Dict[str, Any]:
        """Get current model information."""
        try:
            response = self._make_request("GET", "/v1/models/current")
            return response
        except BackendError as e:
            print(f"Failed to get current model: {e}")
            return {
                "current_model": "unknown",
                "engine_type": "unknown"
            }
    
    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()


class BackendError(Exception):
    """Base exception for backend communication errors."""
    pass


class SessionNotFoundError(BackendError):
    """Exception raised when a session is not found or has expired."""
    pass


# Global client instance
backend_client = BackendClient()


