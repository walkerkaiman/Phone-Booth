#!/bin/bash
# Install Piper TTS Models
# ========================

echo "🎤 Piper TTS Model Installer"
echo "============================="
echo

# Check if virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "WARNING: Virtual environment not detected!"
    echo "Please activate your virtual environment first:"
    echo "  source .venv/bin/activate"
    echo
    exit 1
fi

# Change to project root
cd "$(dirname "$0")/.."

echo "Installing Piper TTS models..."
echo

# Run the installer script
python scripts/install_piper_models.py

echo
echo "Installation complete!"
echo
echo "To use the new models:"
echo "1. Restart the web UI"
echo "2. Test with different personalities"
echo
