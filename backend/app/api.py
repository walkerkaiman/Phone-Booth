"""
backend/app/api.py
===================
HTTP API routes for the backend service using FastAPI.
"""

from __future__ import annotations

import time
from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from .config import config
from .llm.engine import create_engine, LanguageModelEngine
from .models.schemas import (
	GenerateRequest,
	GenerateResponse,
	HealthzResponse,
	SessionReleaseRequest,
	SessionReleaseResponse,
	SessionStartRequest,
	SessionStartResponse,
	ModelListResponse,
	ModelSwitchRequest,
	ModelSwitchResponse,
)
from .personas.loader import load_personas
from .sessions.models import Session, Turn, truncate_history
from .sessions.store import InMemorySessionStore, SessionStore


router = APIRouter(prefix="/v1")


def get_store() -> SessionStore:
	# In a real app, this would be created in app state and injected.
	# Here we use a module-level singleton for simplicity in the scaffold.
	if not hasattr(get_store, "_store"):
		setattr(get_store, "_store", InMemorySessionStore())
	return getattr(get_store, "_store")


def get_engine() -> LanguageModelEngine:
	if not hasattr(get_engine, "_engine"):
		# Create engine based on configuration
		llm_config = config.llm
		setattr(get_engine, "_engine", create_engine(llm_config))
	return getattr(get_engine, "_engine")


def get_personas() -> Dict[str, dict]:
	if not hasattr(get_personas, "_cache"):
		setattr(get_personas, "_cache", load_personas())
	return getattr(get_personas, "_cache")


@router.get("/healthz", response_model=HealthzResponse)
def healthz() -> HealthzResponse:
	return HealthzResponse(ok=True)


@router.post("/session/start", response_model=SessionStartResponse)
def session_start(
	request: SessionStartRequest,
	store: SessionStore = Depends(get_store),
):
	# Validate UUID format from client string
	try:
		session_uuid = UUID(request.session_id)
	except ValueError as exc:
		raise HTTPException(status_code=400, detail="Invalid session_id (UUIDv4 expected)") from exc

	now = time.time()
	session = Session(
		session_id=session_uuid,
		booth_id=request.booth_id,
		personality=request.personality,
		mode=request.mode,
		turns=[],
		created_at=now,
		updated_at=now,
	)
	session, created = store.create_if_absent(session)
	return SessionStartResponse(session_id=str(session.session_id), created=created, expires_in_seconds=session.ttl_seconds)


@router.post("/generate", response_model=GenerateResponse)
def generate(
	request: GenerateRequest,
	store: SessionStore = Depends(get_store),
	engine: LanguageModelEngine = Depends(get_engine),
):
	# Resolve session
	try:
		session_uuid = UUID(request.session_id)
	except ValueError as exc:
		raise HTTPException(status_code=400, detail="Invalid session_id") from exc

	session = store.get(session_uuid)
	if session is None:
		raise HTTPException(status_code=404, detail="Session not found or expired")

	# Apply optional per-turn overrides
	personality = request.personality or session.personality
	mode = request.mode or session.mode

	# Build messages with short rolling history
	messages = []
	for t in session.turns:
		messages.append({"role": t.role, "content": t.content})
	messages.append({"role": "user", "content": request.user_text})

	# Minimal system prompt construction using loaded persona
	personas = get_personas()
	persona = personas.get(personality)
	if persona is None:
		raise HTTPException(status_code=400, detail="Unknown personality id")
	system_prompt = persona.system_prompt
	if mode:
		system_prompt = f"{system_prompt}\n\n[MODE={mode}]"

	# Debug: Log the messages being sent to LLM
	print(f"=== LLM DEBUG ===")
	print(f"Session ID: {session.session_id}")
	print(f"Personality: {personality}")
	print(f"Mode: {mode}")
	print(f"System Prompt: {system_prompt[:200]}...")
	print(f"Messages being sent to LLM:")
	for i, msg in enumerate(messages):
		print(f"  {i}: {msg['role']}: {msg['content'][:100]}...")
	print(f"User Text: {request.user_text}")
	print(f"==================")

	# Get generation parameters from config
	llm_config = config.llm
	text, usage = engine.generate(
		system_prompt=system_prompt,
		messages=messages,
		max_tokens=llm_config.get("max_tokens", 180),
		temperature=llm_config.get("temperature", 0.8),
		top_p=llm_config.get("top_p", 0.9),
	)

	# Append user and assistant turns
	now = time.time()
	store.append_turn(session.session_id, Turn(role="user", content=request.user_text, ts=now))
	store.append_turn(session.session_id, Turn(role="assistant", content=text, ts=now))

	# Trim history to configured limit
	history_max_turns = config.sessions.get("history_max_turns", 8)
	truncate_history(session, history_max_turns=history_max_turns)

	return GenerateResponse(text=text, personality=personality, usage=usage)


@router.post("/session/release", response_model=SessionReleaseResponse)
def session_release(request: SessionReleaseRequest, store: SessionStore = Depends(get_store)):
	try:
		session_uuid = UUID(request.session_id)
	except ValueError as exc:
		raise HTTPException(status_code=400, detail="Invalid session_id") from exc
	store.release(session_uuid)
	return SessionReleaseResponse(ok=True)


@router.get("/models", response_model=ModelListResponse)
def list_models(engine: LanguageModelEngine = Depends(get_engine)):
	"""List available models."""
	try:
		if hasattr(engine, 'get_available_models'):
			models = engine.get_available_models()
			current_model = getattr(engine, 'model_name', 'unknown')
			return ModelListResponse(
				models=models,
				current_model=current_model,
				engine_type=config.llm.get("engine", "unknown")
			)
		else:
			# For non-Ollama engines, return basic info
			return ModelListResponse(
				models=[],
				current_model=getattr(engine, 'model_name', 'unknown'),
				engine_type=config.llm.get("engine", "unknown")
			)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")


@router.post("/models/switch", response_model=ModelSwitchResponse)
def switch_model(
	request: ModelSwitchRequest,
	engine: LanguageModelEngine = Depends(get_engine)
):
	"""Switch to a different model."""
	try:
		if hasattr(engine, 'set_model'):
			engine.set_model(request.model_name)
			return ModelSwitchResponse(
				success=True,
				model_name=request.model_name,
				message=f"Switched to model: {request.model_name}"
			)
		else:
			raise HTTPException(
				status_code=400,
				detail="Current engine does not support model switching"
			)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to switch model: {str(e)}")


@router.get("/models/current")
def get_current_model(engine: LanguageModelEngine = Depends(get_engine)):
	"""Get current model information."""
	try:
		current_model = getattr(engine, 'model_name', 'unknown')
		engine_type = config.llm.get("engine", "unknown")
		return {
			"current_model": current_model,
			"engine_type": engine_type
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to get current model: {str(e)}")



