"""
frontend/booth/lighting/driver.py
=================================
High-level role:
- Declares the interface for lighting drivers used to set brightness (0–255) on the
  booth's lighting hardware.

Where this fits:
- `main.py` picks a concrete driver (null, PWM, etc.) based on config and uses it to
  reflect TTS amplitude in real time.

What this file typically contains (when implemented):
- An abstract `LightingDriver` with methods:
  - `start()` — initialize hardware.
  - `set_brightness(value: int)` — set current brightness (0–255).
  - `stop()` — teardown/cleanup.
- A factory to choose a concrete driver by name.

Notes for new contributors:
- Keep hardware-specific details in concrete drivers. This interface should remain
  simple and stable.
"""

# Placeholder interface
class LightingDriver:  # pylint: disable=too-few-public-methods
	"""Abstract base for lighting drivers."""

	def start(self):
		raise NotImplementedError

	def set_brightness(self, value: int):
		raise NotImplementedError

	def stop(self):
		raise NotImplementedError


