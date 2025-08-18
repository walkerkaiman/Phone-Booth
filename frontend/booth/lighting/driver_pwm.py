"""
frontend/booth/lighting/driver_pwm.py
====================================
High-level role:
- A GPIO PWM-based lighting driver for platforms like Raspberry Pi.

Where this fits:
- Selected by config when `lighting.driver` is "pwm" and hardware is available.

What this file typically contains (when implemented):
- A `PWMLightingDriver` that sets up a PWM channel on the configured GPIO pin and maps
  brightness (0–255) to a duty cycle.

Notes for new contributors:
- Keep GPIO access isolated here; detect platform and handle missing libs gracefully.
"""

from .driver import LightingDriver


class PWMLightingDriver(LightingDriver):  # pylint: disable=too-few-public-methods
	"""Placeholder PWM lighting driver implementation."""

	def __init__(self, gpio_pin: int = 18):
		self.gpio_pin = gpio_pin

	def start(self):
		return None

	def set_brightness(self, value: int):
		_ = (self.gpio_pin, value)
		return None

	def stop(self):
		return None


