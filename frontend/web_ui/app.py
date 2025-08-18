"""
frontend/web_ui/app.py
======================
Web-based UI for simulating phone booth interactions.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, jsonify, render_template, request, session
from flask_socketio import SocketIO, emit

from frontend.booth.config import config
from frontend.booth.net import BackendClient, BackendError
from frontend.booth.state import BoothState, BoothStateManager, ConversationTurn, SceneInfo
from frontend.booth.tts import tts_manager

# Import audio setup functions
try:
    from scripts.audio_setup import list_audio_devices, update_config, show_current_config
except ImportError:
    # Fallback if audio setup script is not available
    def list_audio_devices():
        return {"error": "Audio setup script not available"}
    
    def update_config(input_device=None, output_device=None):
        return False
    
    def show_current_config():
        return {"error": "Audio setup script not available"}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'phone-booth-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state manager
state_manager = BoothStateManager()
backend_client = BackendClient()


@app.route('/')
def index():
    """Main phone booth interface."""
    return render_template('phone_booth.html')


@app.route('/api/status')
def get_status():
    """Get current booth status."""
    return jsonify({
        'state': state_manager.state.value,
        'session_active': state_manager.session is not None,
        'session_id': state_manager.session.session_id if state_manager.session else None,
        'personality': state_manager.session.personality if state_manager.session else None,
        'mode': state_manager.session.mode if state_manager.session else None,
        'stats': state_manager.get_stats()
    })


@app.route('/api/pickup', methods=['POST'])
def pickup_phone():
    """Simulate picking up the phone."""
    try:
        data = request.get_json() or {}
        personality = data.get('personality', config.default_personality)
        mode = data.get('mode', 'chat')
        
        # Start new session
        session_info = state_manager.start_session(
            booth_id=config.booth_id,
            personality=personality,
            mode=mode
        )
        
        # Register with backend
        if backend_client.start_session(session_info):
            state_manager.transition_to(BoothState.PICKUP)
            return jsonify({
                'success': True,
                'session_id': session_info.session_id,
                'message': f'Phone picked up. Connected to {personality} personality.'
            })
        else:
            state_manager.transition_to(BoothState.ERROR, "Failed to connect to backend")
            return jsonify({
                'success': False,
                'error': 'Failed to connect to backend'
            }), 500
            
    except Exception as e:
        state_manager.transition_to(BoothState.ERROR, str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/hangup', methods=['POST'])
def hangup_phone():
    """Simulate hanging up the phone."""
    try:
        if state_manager.session:
            # Release session with backend
            backend_client.release_session(state_manager.session.session_id)
            
            # End local session
            state_manager.end_session()
        
        state_manager.transition_to(BoothState.HANGUP)
        return jsonify({
            'success': True,
            'message': 'Phone hung up. Session ended.'
        })
        
    except Exception as e:
        state_manager.transition_to(BoothState.ERROR, str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/speak', methods=['POST'])
def speak():
    """Simulate speaking into the phone."""
    try:
        if not state_manager.session:
            return jsonify({
                'success': False,
                'error': 'No active session. Pick up the phone first.'
            }), 400
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        user_message = data['message']
        personality = data.get('personality', state_manager.session.personality)
        mode = data.get('mode', state_manager.session.mode)
        
        # Transition to listening state
        state_manager.transition_to(BoothState.LISTENING)
        
        # Capture scene (simulated)
        scene = SceneInfo.create(
            caption="Web interface simulation",
            tags=["web", "simulation", "desktop"]
        )
        state_manager.update_scene(scene)
        
        # Transition to processing
        state_manager.transition_to(BoothState.PROCESSING)
        
        # Generate response from backend
        start_time = time.time()
        response = backend_client.generate_response(
            session=state_manager.session,
            user_text=user_message,
            scene=scene,
            personality=personality,
            mode=mode
        )
        processing_time = time.time() - start_time
        
        # Extract response
        assistant_text = response.get('text', 'Sorry, I could not generate a response.')
        
        # Synthesize speech
        audio_data, tts_metadata = tts_manager.synthesize(assistant_text, personality)
        
        # Create conversation turn
        turn = ConversationTurn.create(
            user_text=user_message,
            assistant_text=assistant_text,
            scene=scene,
            processing_time=processing_time
        )
        state_manager.add_conversation_turn(turn)
        
        # Transition to speaking
        state_manager.transition_to(BoothState.SPEAKING)
        
        # Get amplitude envelope for lighting simulation
        amplitude_envelope = tts_manager.get_amplitude_envelope(audio_data)
        
        return jsonify({
            'success': True,
            'response': assistant_text,
            'personality': personality,
            'processing_time': processing_time,
            'audio_duration': tts_metadata.get('duration', 0),
            'amplitude_envelope': amplitude_envelope,
            'session_id': state_manager.session.session_id
        })
        
    except BackendError as e:
        state_manager.transition_to(BoothState.ERROR, str(e))
        return jsonify({
            'success': False,
            'error': f'Backend error: {str(e)}'
        }), 500
    except Exception as e:
        state_manager.transition_to(BoothState.ERROR, str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/conversation')
def get_conversation():
    """Get conversation history."""
    if not state_manager.session:
        return jsonify({'conversation': []})
    
    conversation = []
    for turn in state_manager.conversation_history:
        conversation.append({
            'user_text': turn.user_text,
            'assistant_text': turn.assistant_text,
            'timestamp': turn.timestamp,
            'processing_time': turn.processing_time,
            'scene_caption': turn.scene.caption if turn.scene else None,
            'scene_tags': turn.scene.tags if turn.scene else []
        })
    
    return jsonify({'conversation': conversation})


@app.route('/api/personalities')
def get_personalities():
    """Get available personalities."""
    return jsonify({
        'personalities': [
            {'id': 'trickster', 'name': 'The Trickster', 'description': 'Playful and mischievous'},
            {'id': 'sage', 'name': 'The Sage', 'description': 'Wise and contemplative'},
            {'id': 'muse', 'name': 'The Muse', 'description': 'Creative and inspiring'},
            {'id': 'jester', 'name': 'The Jester', 'description': 'Humorous and entertaining'},
            {'id': 'night_watch', 'name': 'The Night Watch', 'description': 'Mysterious and vigilant'}
        ],
        'modes': config.modes
    })


@app.route('/api/audio/devices')
def get_audio_devices():
    """Get available audio devices."""
    try:
        import pyaudio
        
        p = pyaudio.PyAudio()
        devices = {
            'input_devices': [],
            'output_devices': [],
            'default_input': None,
            'default_output': None
        }
        
        # Get input devices
        for i in range(p.get_device_count()):
            try:
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    devices['input_devices'].append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': int(device_info['defaultSampleRate']),
                        'host_api': p.get_host_api_info_by_index(device_info['hostApi'])['name']
                    })
            except Exception:
                continue
        
        # Get output devices
        for i in range(p.get_device_count()):
            try:
                device_info = p.get_device_info_by_index(i)
                if device_info['maxOutputChannels'] > 0:
                    devices['output_devices'].append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxOutputChannels'],
                        'sample_rate': int(device_info['defaultSampleRate']),
                        'host_api': p.get_host_api_info_by_index(device_info['hostApi'])['name']
                    })
            except Exception:
                continue
        
        # Get default devices
        try:
            default_input = p.get_default_input_device_info()
            devices['default_input'] = default_input['index']
        except Exception:
            pass
        
        try:
            default_output = p.get_default_output_device_info()
            devices['default_output'] = default_output['index']
        except Exception:
            pass
        
        p.terminate()
        return jsonify(devices)
        
    except ImportError:
        return jsonify({'error': 'PyAudio not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/audio/config')
def get_audio_config():
    """Get current audio configuration."""
    try:
        audio_config = config.audio
        return jsonify({
            'sample_rate': audio_config.get('sample_rate', 16000),
            'channels': audio_config.get('channels', 1),
            'chunk_size': audio_config.get('chunk_size', 1024),
            'input_device': audio_config.get('input_device'),
            'output_device': audio_config.get('output_device')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/audio/config', methods=['POST'])
def update_audio_config():
    """Update audio configuration."""
    try:
        data = request.get_json()
        input_device = data.get('input_device')
        output_device = data.get('output_device')
        
        # Update the configuration
        success = update_config(input_device, output_device)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Audio configuration updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update audio configuration'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/audio/test/<device_type>/<int:device_index>')
def test_audio_device(device_type, device_index):
    """Test a specific audio device."""
    try:
        import pyaudio
        import time
        import math
        import struct
        
        p = pyaudio.PyAudio()
        
        if device_type == 'input':
            # Test input device
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=1024
            )
            
            # Record for 3 seconds
            frames = []
            for i in range(30):  # 3 seconds at 100ms chunks
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
                time.sleep(0.1)
            
            stream.stop_stream()
            stream.close()
            
            return jsonify({
                'success': True,
                'message': f'Input device {device_index} tested successfully. Recorded {len(frames)} chunks.'
            })
            
        elif device_type == 'output':
            # Test output device
            sample_rate = 16000
            duration = 2.0
            frequency = 440.0
            
            # Generate test tone
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
            stream.close()
            
            return jsonify({
                'success': True,
                'message': f'Output device {device_index} tested successfully. Test tone played.'
            })
        
        else:
            return jsonify({'error': 'Invalid device type'}), 400
        
        p.terminate()
        
    except ImportError:
        return jsonify({'error': 'PyAudio not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    print('Client connected')
    emit('status', {
        'state': state_manager.state.value,
        'session_active': state_manager.session is not None
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print('Client disconnected')


def run_web_ui(host: str = '0.0.0.0', port: int = 5000, debug: bool = True):
    """Run the web UI server."""
    print(f"Starting Phone Booth Web UI on http://{host}:{port}")
    
    # Get personalities and modes without Flask context
    personalities = [
        {'id': 'trickster', 'name': 'The Trickster', 'description': 'Playful and mischievous'},
        {'id': 'sage', 'name': 'The Sage', 'description': 'Wise and contemplative'},
        {'id': 'muse', 'name': 'The Muse', 'description': 'Creative and inspiring'},
        {'id': 'jester', 'name': 'The Jester', 'description': 'Humorous and entertaining'},
        {'id': 'night_watch', 'name': 'The Night Watch', 'description': 'Mysterious and vigilant'}
    ]
    print("Available personalities:", [p['id'] for p in personalities])
    print("Available modes:", config.modes)

    socketio.run(app, host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_ui()
