### Character Booth System — Phone-Booth Conversational Installation

The Character Booth System is a multi-device art installation where physical phone booths act as conversational kiosks. Each booth captures audio from a handset microphone and a single scene snapshot from a webcam, then sends them (together with a locally generated `session_id` and the selected personality) to a centralized backend hosting an LLM. The backend returns a personality-driven text reply, which the booth converts to audio with local TTS and uses to drive lighting brightness.

This repository contains a complete, modular scaffold for both backend and frontend sides, including configuration files, persona assets, scripts, and testing placeholders.

---

## Overview

- **Frontend (booth):** Runs on each physical booth. Handles microphone capture (with VAD), ASR transcription, webcam snapshot to scene tags/caption, HTTP requests, local TTS playback, and lighting control driven by the reply audio amplitude.
- **Backend (service):** Exposes HTTP endpoints for session lifecycle and text generation. Maintains short rolling conversation history per session, loads persona prompts and shared guardrails, and proxies requests to a pluggable LLM engine (local `llama-cpp-python` by default or an Ollama proxy).
- **Transport:** HTTP/JSON. HTTPS is optional depending on deployment.
- **Privacy:** Scene info is lightweight (colors/objects/brightness). No identity/age/gender guesses.

---

## Repository Layout

- **`backend/`**: Backend service implementation
  - `app/`
    - `main.py`: Server entrypoint (app factory to wire routes; placeholder now)
    - `api.py`: Declares HTTP API routes and handlers (placeholder)
    - `config.py`: Loads/holds backend settings and defaults (placeholder)
    - `log.py`: Logging configuration helpers (placeholder)
    - `models/schemas.py`: Request/response schemas for API (placeholder)
    - `llm/`: LLM engine interface and implementations
      - `engine.py`: Abstract engine interface (placeholder)
      - `llama_cpp_engine.py`: Local llama.cpp engine (placeholder)
      - `ollama_proxy.py`: Remote Ollama proxy engine (placeholder)
    - `sessions/`: Session models and storage backend(s)
      - `models.py`: Session/Turn data models (placeholder)
      - `store.py`: Session store interface and factory (placeholder)
      - `redis_store.py`: Redis-backed store (placeholder)
    - `personas/`: Persona definitions and loader
      - `model.py`: Persona model (placeholder)
      - `loader.py`: Reads prompts/metadata and builds system prompts (placeholder)
    - `prompts/guardrails.txt`: Shared safety baseline appended to persona prompts
  - `assets/personas/`: Persona assets (prompts + metadata JSON)
    - `trickster/`, `sage/`, `muse/`, `jester/`, `night_watch/`
    - `index.json`: Optional catalog of personas and defaults
  - `requirements.txt`: Backend Python dependencies
  - `run_backend.bat` / `run_backend.sh`: Dev helper to start the server with Uvicorn (Windows/macOS/Linux)

- **`frontend/`**: Booth client implementation
  - `booth/`
    - `main.py`: Orchestrates the booth loop (placeholder)
    - `state.py`: Holds session + FSM state (placeholder)
    - `audio_io.py`: Microphone/speaker I/O utilities (placeholder)
    - `vad.py`: Voice Activity Detection utilities (placeholder)
    - `asr.py`: Faster-Whisper transcription wrapper (placeholder)
    - `vision.py`: Webcam snapshot + scene tag extraction (placeholder)
    - `tts.py`: Piper-based text-to-speech + amplitude envelope (placeholder)
    - `net.py`: HTTP client to call backend endpoints (placeholder)
    - `config.py`: Frontend configuration loader/defaults (placeholder)
    - `log.py`: Frontend logging setup (placeholder)
    - `lighting/`
      - `driver.py`: Lighting driver interface (placeholder)
      - `driver_null.py`: No-op driver
      - `driver_pwm.py`: PWM GPIO driver (placeholder)
      - `mapper.py`: Amplitude-to-brightness mapper (placeholder)
  - `web_ui/`: Web-based phone booth simulator
    - `app.py`: Flask web application
    - `templates/phone_booth.html`: Main interface template
    - `requirements.txt`: Web UI dependencies
    - `run_web_ui.bat` / `run_web_ui.sh`: Web UI startup scripts
  - `requirements.txt`: Frontend Python dependencies
  - `run_frontend.bat` / `run_frontend.sh`: Dev helper to run the booth loop (Windows/macOS/Linux)

- **`config/`**: Example configuration JSON
  - `backend.json`: Backend engine, sessions, and logging settings
  - `frontend.json`: Booth defaults, audio/ASR/TTS/lighting configuration

- **`assets/`**
  - `prompts/`: Placeholder for shared prompt files
  - `audio/`: Placeholder for pickup/hangup or other SFX

- **`scripts/`**
  - `install_models.bat` / `install_models.sh`: Placeholder to download model assets (Windows/macOS/Linux; edit for real URLs)
  - `systemd/`: Example unit files (`backend.service`, `frontend.service`)

- **Master Startup Scripts**
  - `start_system.bat` / `start_system.sh`: One-command startup for entire system (Windows/macOS/Linux)

- **`tests/`**: Pytest scaffolding for backend and frontend

---

## Features (Design Targets)

- **Sessions:** Frontend generates UUIDv4 on pickup; backend registers/releases, stores short rolling history, and auto-expires after TTL.
- **ASR:** Faster-Whisper (ctranslate2) for low-latency local transcription.
- **TTS:** Piper for local synthesis; amplitude envelope drives lighting brightness (0–255) with smoothing.
- **Vision:** Single frame per user turn to produce a caption and tags; strictly no identity inference.
- **Personas:** Persona-specific system prompts with shared guardrails and mode-specific behavior (chat, riddle, haiku, story).
- **LLM Engines:** Pluggable interface; local `llama-cpp-python` or remote `ollama` proxy.
- **Error Handling:** If `/v1/generate` returns 404 (expired session), the frontend transparently creates a new session.

---

## Requirements

- Python 3.10+ recommended
- Platform-specific audio/video dependencies depending on your OS
  - On Linux: ALSA/PulseAudio for audio, V4L2 for webcams
  - On Windows/macOS: Ensure microphone/speaker/webcam drivers are available
- Models
  - LLM: GGUF model for llama.cpp (e.g., `llama3.1-8b.Q4_K_M.gguf`)
  - ASR: Faster-Whisper model files managed by `ctranslate2`
  - TTS: Piper voice models matching persona `default_voice`

---

## Setup

Create and activate a virtual environment (recommended).

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
```

Install dependencies.

```bash
# Backend
pip install -r backend/requirements.txt

# Frontend
pip install -r frontend/requirements.txt
```

Download models (edit `scripts/install_models.bat` or `scripts/install_models.sh` to add real URLs), or place models under a known path (e.g., `C:\\models` or `/models`).

---

## Configuration

- **Backend:** `config/backend.json`

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "cors_origins": ["*"]
  },
  "llm": {
    "engine": "llama_cpp",
    "model_path": "/models/llama3.1-8b.Q4_K_M.gguf",
    "context_length": 2048,
    "temperature": 0.8,
    "top_p": 0.9,
    "max_tokens": 180,
    "n_gpu_layers": -1,
    "n_threads": null,
    "verbose": false
  },
  "sessions": {
    "ttl_seconds": 600,
    "history_max_turns": 8,
    "store": "memory"
  },
  "logging": {"level": "INFO", "json": true}
}
```

**LLM Engine Options:**
- `"engine": "echo"` - Development/testing (echoes user input)
- `"engine": "llama_cpp"` - Local inference with llama-cpp-python
- `"engine": "ollama"` - Remote inference via Ollama API

**GPU Configuration:**
- `"n_gpu_layers": -1` - Use all available GPU layers
- `"n_gpu_layers": 0` - CPU-only inference
- `"n_gpu_layers": 10` - Use first 10 layers on GPU

- **Frontend:** `config/frontend.json`

```json
{
  "backend_url": "http://backend.local:8080",
  "booth_id": "booth-12",
  "default_personality": "trickster",
  "audio": {"sample_rate": 16000},
  "asr": {"model_size": "small", "compute_type": "int8"},
  "tts": {
    "voice_map": {
      "trickster": "en_US-lessac-high",
      "sage": "en_GB-alan-medium"
    }
  },
  "lighting": {"enabled": true, "driver": "pwm", "gpio_pin": 18},
  "modes": ["chat", "riddle", "haiku", "story"]
}
```

---

## Running (Development)

The scripts are the primary entry points for running the applications. They handle environment setup, dependency checks, and provide helpful error messages.

### Quick Start (Recommended)

**One-command startup for the entire system:**

**Windows:**
```bat
start_system.bat
```

**macOS/Linux:**
```bash
./start_system.sh
```

This will:
- Start the backend server
- Wait for it to be ready
- Launch the frontend (which automatically starts the web UI)
- Open both applications in separate windows/processes
- Provide access URLs for both services

### Manual Startup

### Network Deployment

For production deployment with backend and frontend on separate computers, see [NETWORK_SETUP.md](NETWORK_SETUP.md) for detailed instructions.

### Backend

**Primary method - Use the entry point script:**

**Windows:**
```bat
backend\run_backend.bat
```

**macOS/Linux:**
```bash
./backend/run_backend.sh
```

The script will:
- Check for virtual environment activation
- Start the FastAPI server on `http://0.0.0.0:8080`
- Provide helpful error messages if setup is incomplete

**Alternative - Direct Uvicorn (for advanced users):**
```bash
uvicorn backend.app.main:create_app --host 0.0.0.0 --port 8080
```

### Frontend (Booth)

**Web UI (Recommended for Development):**

A web-based interface that simulates phone booth interactions for testing and development.

**Windows:**
```bat
frontend\web_ui\run_web_ui.bat
```

**macOS/Linux:**
```bash
./frontend/web_ui/run_web_ui.sh
```

The web UI provides:
- Visual phone booth interface
- Personality and mode selection
- Real-time conversation history
- Lighting simulation
- Performance statistics
- Access at: http://localhost:5000

**Physical Booth (Production):**

**Windows:**
```bat
frontend\run_frontend.bat
```

**macOS/Linux:**
```bash
./frontend/run_frontend.sh
```

The script will:
- Check for virtual environment activation
- **Automatically launch the web UI** in a new window/background
- Start the booth application
- Provide helpful error messages if setup is incomplete

**Note:** The web UI will be available at http://localhost:5000 when the frontend starts.

**Alternative - Direct Python (for advanced users):**
```bash
python -m frontend.booth.main
```

---

## API Reference (Planned)

Base path: `/v1`

- **POST** `/session/start` — register client-provided `session_id`

Request:
```json
{
  "session_id": "uuid-v4-string",
  "booth_id": "booth-12",
  "personality": "trickster",
  "mode": "chat"
}
```

Response:
```json
{
  "session_id": "uuid-v4-string",
  "created": true,
  "expires_in_seconds": 600
}
```

- **POST** `/generate` — generate a personality-driven reply

Request:
```json
{
  "session_id": "uuid-v4-string",
  "personality": "trickster",
  "mode": "riddle",
  "user_text": "What do you know?",
  "scene": {"caption": "Red scarf under neon", "tags": ["scarf", "neon", "night"]}
}
```

Response:
```json
{
  "text": "Neon keeps secrets; your scarf knows one.",
  "personality": "trickster",
  "usage": {"prompt_tokens": 236, "completion_tokens": 32, "total_tokens": 268}
}
```

Errors:
- `404 Not Found` if session does not exist or expired. Frontend should auto-create a new session and retry.

- **POST** `/session/release` — delete session state

Request:
```json
{"session_id": "uuid-v4-string"}
```

Response:
```json
{"ok": true}
```

- **GET** `/v1/healthz` — service health check

Response:
```json
{"ok": true}
```

---

## Personas

- Persona directories live under `backend/assets/personas/{id}/` containing:
  - `system_prompt.txt`: The persona’s system prompt
  - `metadata.json`: Display metadata and default voice
- A shared baseline is in `backend/app/prompts/guardrails.txt`.
- Optional catalog: `backend/assets/personas/index.json`.

Add a new persona:
1) Create `backend/assets/personas/{new_id}/system_prompt.txt`
2) Add `metadata.json` with `{id, name, description, default_voice, reply_length}`
3) Update `index.json` (optional) and `frontend/config` voice map as needed

---

## Lighting

- **Mapping:** Brightness is derived from the TTS audio amplitude envelope and scaled to 0–255 with smoothing (attack/release) defined in `frontend/booth/lighting/mapper.py`.
- **Drivers:**
  - `driver_null.py`: No-op, for development or when disabled
  - `driver_pwm.py`: PWM GPIO driver for devices like Raspberry Pi (placeholder)
- Disable lighting entirely by setting `lighting.enabled` to `false` in `config/frontend.json`.

---

## Privacy & Safety

- Public-space guardrails enforce PG language and avoid identity assumptions.
- Vision: strictly no identity, age, or gender guesses. Use only colors/objects/brightness.
- Replies should not reference cameras, images, or being an AI.

---

## Testing & Quality

- **Linting/Style:** Pylint (Google style), Black, and isort. Configure via `.pylintrc` and `pyproject.toml` (to be added).
- **Tests:** Pytest scaffolding exists under `tests/`; add unit and integration tests for both backend and frontend modules.

Run tests (example):
```bash
pytest -q
```

---

## Deployment (Example)

- Use the provided systemd units under `scripts/systemd/` as a starting point.
- Configure working directory and environment as needed.
- Ensure models are present at paths referenced by configuration.

---

## Roadmap

- ✅ Implement minimal FastAPI app in `backend/app/main.py` and route handlers in `api.py`.
- ✅ Implement in-memory session store and optional Redis store.
- ✅ Implement LlamaCppEngine for local LLM inference.
- Implement frontend loop with real audio I/O, VAD, ASR, vision tagging, TTS, and lighting control.
- Add comprehensive tests and CI.
- Provide scripts to fetch models automatically and validate integrity.

---

## License

See `LICENSE`.

# Phone-Booth