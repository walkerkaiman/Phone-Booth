"""
frontend/booth/state.py
=======================
High-level role:
- Holds the booth's runtime state: whether the handset is up, the current `session_id`,
  selected personality and mode, and simple finite-state-machine (FSM) status.

Where this fits:
- Used by `main.py` to coordinate transitions between idle, listening, thinking, and
  speaking states. State resets on hangup.

What this file typically contains (when implemented):
- A dataclass or small class with fields: `session_id`, `booth_id`, `personality`,
  `mode`, and flags such as `listening`, `speaking`.
- Helpers to generate a new UUIDv4 and to reset to defaults.
"""

# Placeholder marker
STATE_DEFINED = False


