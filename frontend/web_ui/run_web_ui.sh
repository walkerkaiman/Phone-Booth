#!/bin/bash
# Phone Booth Web UI Startup Script
# ===================================

echo
echo "========================================"
echo "  Phone Booth Web UI - Starting..."
echo "========================================"
echo

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "WARNING: Virtual environment not detected!"
    echo "Please activate your virtual environment first:"
    echo "  source .venv/bin/activate"
    echo
    exit 1
fi

# Change to project root directory
cd "$(dirname "$0")/../.."

# Check if backend is running
echo "Checking backend connectivity..."
if python -c "import httpx; response = httpx.get('http://localhost:8080/v1/healthz', timeout=5); print('Backend is running' if response.status_code == 200 else 'Backend not responding')" 2>/dev/null; then
    echo "Backend is running"
else
    echo "WARNING: Backend not accessible at http://localhost:8080"
    echo "Please start the backend first:"
    echo "  ./backend/run_backend.sh"
    echo
    exit 1
fi

# Install web UI dependencies if needed
echo "Installing web UI dependencies..."
pip install -r frontend/web_ui/requirements.txt

# Start the web UI
echo
echo "Starting Phone Booth Web UI..."
echo
echo "Access the interface at: http://localhost:5000"
echo
echo "Press Ctrl+C to stop the server."
echo

python frontend/web_ui/app.py
