"""
backend/app/personas/loader.py
==============================
Persona loading utilities.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from .model import Persona

# Get the project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "backend" / "assets" / "personas"
GUARDRAILS_PATH = PROJECT_ROOT / "backend" / "app" / "prompts" / "guardrails.txt"


def _read_text(path: Path) -> str:
	return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def load_personas() -> Dict[str, Persona]:
	"""Load all personas from assets and combine with guardrails text.

	Returns a mapping id -> Persona.
	"""
	personas: Dict[str, Persona] = {}
	guardrails = _read_text(GUARDRAILS_PATH) if GUARDRAILS_PATH.exists() else ""
	
	print(f"Loading personas from: {ASSETS_DIR}")
	print(f"Guardrails path: {GUARDRAILS_PATH}")
	
	for meta_path in ASSETS_DIR.glob("*/metadata.json"):
		persona_dir = meta_path.parent
		metadata = _read_json(meta_path)
		prompt_path = persona_dir / "system_prompt.txt"
		base_prompt = _read_text(prompt_path) if prompt_path.exists() else ""
		full_prompt = f"{base_prompt}\n\n{guardrails}".strip()
		
		print(f"Loaded persona: {metadata['id']} from {persona_dir}")
		
		personas[metadata["id"]] = Persona(
			id=metadata["id"],
			name=metadata.get("name", metadata["id"]),
			description=metadata.get("description", ""),
			default_voice=metadata.get("default_voice", ""),
			reply_length=metadata.get("reply_length", "short"),
			system_prompt=full_prompt,
		)
	
	print(f"Loaded {len(personas)} personas: {list(personas.keys())}")
	return personas



