#!/usr/bin/env bash
# Character Booth Frontend - Main Entry Point
# Purpose: Developer convenience script to run the frontend booth loop locally.

set -euo pipefail

echo "Character Booth Frontend - Starting..."
echo

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "WARNING: Virtual environment not detected."
    echo "Please activate your virtual environment first:"
    echo "  source .venv/bin/activate"
    echo
fi

# Change to project root directory (parent of frontend/)
cd "$(dirname "$0")/.."

echo "Starting booth application..."
echo "Press Ctrl+C to stop the application."
echo

# Start the web UI in background
echo "Starting web interface..."
python frontend/web_ui/app.py &
WEB_UI_PID=$!

# Wait a moment for web UI to start
sleep 3

# Start the frontend application
exec python -m frontend.booth.main


