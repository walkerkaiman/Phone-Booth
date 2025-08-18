"""
frontend/booth/net.py
=====================
High-level role:
- HTTP client helpers for communicating with the backend API.

Where this fits:
- Used by `main.py` to call `/v1/session/start`, `/v1/generate`, and `/v1/session/release`.

What this file typically contains (when implemented):
- A small wrapper around `requests` with retry logic and timeouts.
- Functions:
  - `start_session(base_url, payload) -> dict`
  - `generate(base_url, payload) -> dict`
  - `release_session(base_url, session_id) -> dict`
- Error handling that auto-retries start when `/generate` returns 404 (as per design).

Notes for new contributors:
- Keep interfaces simple; return parsed JSON and raise clear exceptions on failure.
"""

# Placeholder marker
NET_AVAILABLE = False


