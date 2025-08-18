#!/usr/bin/env python3
"""
Audio Device Setup and Configuration Script
==========================================
This script helps configure audio input and output devices for the Phone Booth System.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def list_audio_devices():
    """List all available audio devices."""
    try:
        import pyaudio
        
        p = pyaudio.PyAudio()
        
        print("🎤 Available Audio Devices")
        print("=" * 50)
        
        # List input devices
        print("\n📥 INPUT DEVICES (Microphones):")
        print("-" * 30)
        for i in range(p.get_device_count()):
            try:
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    print(f"  [{i}] {device_info['name']}")
                    print(f"      Channels: {device_info['maxInputChannels']}")
                    print(f"      Sample Rate: {device_info['defaultSampleRate']:.0f} Hz")
                    print(f"      Host API: {p.get_host_api_info_by_index(device_info['hostApi'])['name']}")
                    print()
            except Exception as e:
                print(f"  [{i}] Error reading device info: {e}")
        
        # List output devices
        print("\n📤 OUTPUT DEVICES (Speakers):")
        print("-" * 30)
        for i in range(p.get_device_count()):
            try:
                device_info = p.get_device_info_by_index(i)
                if device_info['maxOutputChannels'] > 0:
                    print(f"  [{i}] {device_info['name']}")
                    print(f"      Channels: {device_info['maxOutputChannels']}")
                    print(f"      Sample Rate: {device_info['defaultSampleRate']:.0f} Hz")
                    print(f"      Host API: {p.get_host_api_info_by_index(device_info['hostApi'])['name']}")
                    print()
            except Exception as e:
                print(f"  [{i}] Error reading device info: {e}")
        
        # List default devices
        print("\n⚙️  DEFAULT DEVICES:")
        print("-" * 20)
        try:
            default_input = p.get_default_input_device_info()
            print(f"  Default Input: [{default_input['index']}] {default_input['name']}")
        except Exception as e:
            print(f"  Default Input: Not available ({e})")
        
        try:
            default_output = p.get_default_output_device_info()
            print(f"  Default Output: [{default_output['index']}] {default_output['name']}")
        except Exception as e:
            print(f"  Default Output: Not available ({e})")
        
        p.terminate()
        
    except ImportError:
        print("❌ PyAudio not installed. Install with: pip install pyaudio")
        return False
    
    return True

def test_audio_device(device_index: int, is_input: bool = True):
    """Test a specific audio device."""
    try:
        import pyaudio
        import time
        
        p = pyaudio.PyAudio()
        
        device_info = p.get_device_info_by_index(device_index)
        device_type = "Input" if is_input else "Output"
        
        print(f"🧪 Testing {device_type} Device: [{device_index}] {device_info['name']}")
        print("=" * 60)
        
        if is_input:
            # Test input device
            print("🎤 Testing microphone input...")
            print("   Speak into the microphone for 5 seconds...")
            
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=1024
            )
            
            frames = []
            for i in range(50):  # 5 seconds at 100ms chunks
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
                print(f"\rRecording... {i+1}/50", end="", flush=True)
                time.sleep(0.1)
            
            stream.stop_stream()
            stream.close()
            print(f"\n✅ Recording complete! Captured {len(frames)} chunks")
            
        else:
            # Test output device
            print("🔊 Testing speaker output...")
            print("   Playing test tone...")
            
            # Generate a test tone
            import math
            import struct
            
            sample_rate = 16000
            duration = 2.0  # 2 seconds
            frequency = 440.0  # A4 note
            
            audio_data = b""
            for i in range(int(sample_rate * duration)):
                sample = 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate)
                sample_int = int(sample * 32767)
                audio_data += struct.pack("<h", sample_int)
            
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                output=True,
                output_device_index=device_index,
                frames_per_buffer=1024
            )
            
            stream.write(audio_data)
            stream.stop_stream()
            stream.close()
            print("✅ Test tone played!")
        
        p.terminate()
        return True
        
    except Exception as e:
        print(f"❌ Error testing device: {e}")
        return False

def update_config(input_device: int = None, output_device: int = None):
    """Update the frontend configuration with specific device indices."""
    config_path = project_root / "config" / "frontend.json"
    
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return False
    
    try:
        import json
        
        # Load current config
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Update audio configuration
        if "audio" not in config:
            config["audio"] = {}
        
        if input_device is not None:
            config["audio"]["input_device"] = input_device
            print(f"✅ Set input device to index {input_device}")
        
        if output_device is not None:
            config["audio"]["output_device"] = output_device
            print(f"✅ Set output device to index {output_device}")
        
        # Save updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent='\t', ensure_ascii=False)
        
        print(f"✅ Configuration saved to {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def show_current_config():
    """Show the current audio configuration."""
    config_path = project_root / "config" / "frontend.json"
    
    print("⚙️  Current Audio Configuration")
    print("=" * 40)
    
    if config_path.exists():
        try:
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            audio_config = config.get("audio", {})
            print(f"  Sample Rate: {audio_config.get('sample_rate', 'default (16000)')}")
            print(f"  Channels: {audio_config.get('channels', 'default (1)')}")
            print(f"  Chunk Size: {audio_config.get('chunk_size', 'default (1024)')}")
            print(f"  Input Device: {audio_config.get('input_device', 'default system device')}")
            print(f"  Output Device: {audio_config.get('output_device', 'default system device')}")
            
        except Exception as e:
            print(f"  Error reading config: {e}")
    else:
        print("  No config file found, using defaults")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Audio Device Setup for Phone Booth System")
    parser.add_argument("--list", action="store_true", help="List all available audio devices")
    parser.add_argument("--test-input", type=int, help="Test input device by index")
    parser.add_argument("--test-output", type=int, help="Test output device by index")
    parser.add_argument("--set-input", type=int, help="Set input device index in config")
    parser.add_argument("--set-output", type=int, help="Set output device index in config")
    parser.add_argument("--show-config", action="store_true", help="Show current audio configuration")
    
    args = parser.parse_args()
    
    if args.list:
        list_audio_devices()
    
    if args.test_input is not None:
        test_audio_device(args.test_input, is_input=True)
    
    if args.test_output is not None:
        test_audio_device(args.test_output, is_input=False)
    
    if args.set_input is not None or args.set_output is not None:
        update_config(args.set_input, args.set_output)
    
    if args.show_config:
        show_current_config()
    
    # If no arguments provided, show help
    if not any([args.list, args.test_input, args.test_output, args.set_input, args.set_output, args.show_config]):
        parser.print_help()
        print("\n📋 Quick Start:")
        print("  1. List devices: python scripts/audio_setup.py --list")
        print("  2. Test input: python scripts/audio_setup.py --test-input 0")
        print("  3. Test output: python scripts/audio_setup.py --test-output 0")
        print("  4. Set devices: python scripts/audio_setup.py --set-input 0 --set-output 1")
        print("  5. Show config: python scripts/audio_setup.py --show-config")

if __name__ == "__main__":
    main()
