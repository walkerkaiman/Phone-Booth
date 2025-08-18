#!/usr/bin/env bash
# Character Booth Backend - Main Entry Point
# Purpose: Developer convenience script to run the backend server locally.
# In production, use systemd (see scripts/systemd/backend.service) or another process manager.

set -euo pipefail

echo "Character Booth Backend - Starting..."
echo

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "WARNING: Virtual environment not detected."
    echo "Please activate your virtual environment first:"
    echo "  source .venv/bin/activate"
    echo
fi

# Change to project root directory (parent of backend/)
cd "$(dirname "$0")/.."

# Set up environment
APP_IMPORT="backend.app.main:create_app"
HOST="0.0.0.0"
PORT="8080"

echo "Starting server on $HOST:$PORT..."
echo "Press Ctrl+C to stop the server."
echo

# Start the server
exec uvicorn "$APP_IMPORT" --host "$HOST" --port "$PORT"


