"""
frontend/booth/lighting/driver_null.py
=====================================
High-level role:
- A no-op lighting driver for development or when lighting is disabled.

Where this fits:
- Selected by config when `lighting.enabled` is false or `driver` is "null".

What this file typically contains (when implemented):
- A `NullLightingDriver` implementing the `LightingDriver` interface with empty methods.
"""

from .driver import LightingDriver


class NullLightingDriver(LightingDriver):  # pylint: disable=too-few-public-methods
	"""No-op implementation of the lighting driver API."""

	def start(self):
		return None

	def set_brightness(self, value: int):
		_ = value
		return None

	def stop(self):
		return None


