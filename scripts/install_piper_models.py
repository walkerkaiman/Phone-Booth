#!/usr/bin/env python3
"""
Script to download and install Piper TTS models.
"""

import os
import sys
import json
import urllib.request
from pathlib import Path
import zipfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Model definitions - these are popular, high-quality models
MODELS = {
    "en_US-lessac-high": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/high/en_US-lessac-high.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/high/en_US-lessac-high.onnx.json",
        "description": "High-quality US English voice (Lessac)"
    },
    "en_GB-alan-medium": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx.json",
        "description": "Medium-quality British English voice (Alan)"
    },
    "en_US-lessac-medium": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json",
        "description": "Medium-quality US English voice (Lessac)"
    },
    "en_US-amy-low": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/low/en_US-amy-low.onnx",
        "config_url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/low/en_US-amy-low.onnx.json",
        "description": "Low-quality US English voice (Amy) - faster, smaller"
    }
}

def download_file(url: str, filepath: Path, description: str) -> bool:
    """Download a file with progress indication."""
    try:
        print(f"Downloading {description}...")
        print(f"URL: {url}")
        print(f"Target: {filepath}")
        
        # Create directory if it doesn't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Download with progress
        def progress_hook(block_num, block_size, total_size):
            if total_size > 0:
                percent = min(100, (block_num * block_size * 100) // total_size)
                print(f"\rProgress: {percent}%", end="", flush=True)
        
        urllib.request.urlretrieve(url, filepath, progress_hook)
        print(f"\n✅ Downloaded: {filepath.name}")
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to download {filepath.name}: {e}")
        return False

def install_models(models_dir: Path = None, selected_models: list = None):
    """Install Piper TTS models."""
    if models_dir is None:
        models_dir = project_root / "models"
    
    if selected_models is None:
        selected_models = list(MODELS.keys())
    
    print("🎤 Piper TTS Model Installer")
    print("=" * 50)
    print(f"Models directory: {models_dir}")
    print(f"Selected models: {', '.join(selected_models)}")
    print()
    
    # Create models directory
    models_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(selected_models)
    
    for model_id in selected_models:
        if model_id not in MODELS:
            print(f"❌ Unknown model: {model_id}")
            continue
            
        model_info = MODELS[model_id]
        print(f"\n📦 Installing {model_id}")
        print(f"   Description: {model_info['description']}")
        
        # Download model file
        model_path = models_dir / f"{model_id}.onnx"
        if not download_file(model_info["url"], model_path, f"{model_id} model"):
            continue
            
        # Download config file
        config_path = models_dir / f"{model_id}.onnx.json"
        if not download_file(model_info["config_url"], config_path, f"{model_id} config"):
            # Remove the model file if config download failed
            if model_path.exists():
                model_path.unlink()
            continue
            
        success_count += 1
        print(f"✅ Successfully installed {model_id}")
    
    print(f"\n🎉 Installation complete!")
    print(f"   Successfully installed: {success_count}/{total_count} models")
    print(f"   Models directory: {models_dir}")
    
    if success_count > 0:
        print(f"\n📝 Next steps:")
        print(f"   1. Update config/frontend.json to use the new models")
        print(f"   2. Restart the web UI to use real TTS")
        print(f"   3. Test with different personalities")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Install Piper TTS models")
    parser.add_argument("--models-dir", type=Path, help="Directory to install models")
    parser.add_argument("--models", nargs="+", choices=list(MODELS.keys()), 
                       help="Specific models to install")
    parser.add_argument("--list", action="store_true", help="List available models")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available Piper TTS models:")
        print("=" * 40)
        for model_id, info in MODELS.items():
            print(f"  {model_id}: {info['description']}")
        return
    
    install_models(args.models_dir, args.models)

if __name__ == "__main__":
    main()
