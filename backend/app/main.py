"""
backend/app/main.py
=================================
High-level role:
- This is the backend server entrypoint for the Character Booth System.
- It is responsible for creating the web application (FastAPI) instance and wiring
  together the API routes defined in `api.py`.

Where this fits:
- Lives in the backend side of the project. The frontend phone booth devices talk to
  this service over HTTP to start/release sessions and to generate replies from the LLM.

What this file typically contains (when implemented):
- A `create_app()` function that builds and returns a FastAPI application.
- App-level configuration (logging, CORS) sourced from `config.py`.
- Route mounting from `api.py`.
- A very small health-check endpoint for uptime checks.

How it is used:
- A production process manager (e.g., systemd) or a development server (uvicorn)
  points at the app factory here, e.g.
    uvicorn backend.app.main:create_app --host 0.0.0.0 --port 8080

Note:
- This is a placeholder scaffold. The concrete logic will be implemented in later steps.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add the project root to Python path so imports work
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router


def create_app() -> FastAPI:
	"""Application factory that creates and configures the FastAPI app."""
	app = FastAPI(title="Character Booth Backend", version="0.1.0")

	# Minimal permissive CORS for development; tighten for production
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(api_router)
	return app


def run():
	"""Main entry point for the backend application."""
	print("Character Booth Backend - Starting...")
	print("(This is a placeholder implementation)")
	print("In the real implementation, this would:")
	print("1. Load configuration")
	print("2. Initialize logging")
	print("3. Create FastAPI app with routes")
	print("4. Start the server")
	return 0


if __name__ == "__main__":
	sys.exit(run())


