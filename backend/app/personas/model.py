"""
backend/app/personas/model.py
=============================
Persona models.
"""

from __future__ import annotations

from pydantic import BaseModel


class Persona(BaseModel):
	id: str
	name: str
	description: str
	default_voice: str
	reply_length: str
	system_prompt: str



