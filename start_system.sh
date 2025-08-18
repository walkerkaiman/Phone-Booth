#!/bin/bash
# Phone Booth System - Master Startup Script
# ==========================================
# Starts backend, waits for it to be ready, then launches frontend

echo
echo "========================================"
echo "  Phone Booth System - Starting..."
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
cd "$(dirname "$0")"

echo "Step 1: Starting Backend Server..."
echo

# Start backend in background
./backend/run_backend.sh &
BACKEND_PID=$!

echo "Backend starting (PID: $BACKEND_PID)..."
echo "Waiting for backend to be ready..."

# Wait for backend to be accessible
while true; do
    sleep 2
    if python -c "import httpx; response = httpx.get('http://localhost:8080/v1/healthz', timeout=5); print('Backend is ready!' if response.status_code == 200 else 'Still waiting...')" 2>/dev/null; then
        echo "Backend is ready!"
        break
    else
        echo "Still waiting for backend..."
    fi
done

echo
echo "Backend is ready! Starting Frontend..."
echo

# Start frontend (which will also launch web UI)
./frontend/run_frontend.sh &
FRONTEND_PID=$!

echo
echo "========================================"
echo "  System Started Successfully!"
echo "========================================"
echo
echo "Backend: http://localhost:8080 (PID: $BACKEND_PID)"
echo "Web UI:  http://localhost:5000"
echo "Frontend PID: $FRONTEND_PID"
echo
echo "Both applications are running in background."
echo "To stop the system, use: kill $BACKEND_PID $FRONTEND_PID"
echo
echo "Press Ctrl+C to stop all processes..."
echo

# Wait for user to stop
trap "echo 'Stopping system...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
