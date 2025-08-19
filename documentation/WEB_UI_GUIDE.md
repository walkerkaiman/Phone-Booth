# Web UI Guide

This guide explains how to use the web-based Phone Booth Simulator for testing and development.

## Overview

The web UI provides a complete simulation of the phone booth experience, allowing you to:
- Test all personalities and conversation modes
- Simulate phone pickup/hangup actions
- View real-time conversation history
- See lighting effects based on audio amplitude
- Monitor performance statistics
- Test backend connectivity and responses

## Quick Start

### 1. Start the Backend

First, ensure the backend is running:

```bash
# Windows
backend\run_backend.bat

# macOS/Linux
./backend/run_backend.sh
```

The backend should be accessible at `http://localhost:8080`.

### 2. Start the Web UI

**Option A - Automatic Launch (Recommended):**
When you start the frontend, the web UI will automatically launch:

```bash
# Windows
frontend\run_frontend.bat

# macOS/Linux
./frontend/run_frontend.sh
```

**Option B - Manual Launch:**
If you want to run the web UI separately:

```bash
# Windows
frontend\web_ui\run_web_ui.bat

# macOS/Linux
./frontend/web_ui/run_web_ui.sh
```

The web UI will be available at `http://localhost:5000`.

### 3. Use the Interface

1. **Select Personality & Mode**: Choose from available personalities and conversation modes
2. **Pick Up Phone**: Click "📞 Pick Up Phone" to start a session
3. **Send Messages**: Type your message and click "🎤 Speak"
4. **View Responses**: See the AI's response and conversation history
5. **Hang Up**: Click "📞 Hang Up Phone" to end the session

## Interface Features

### Status Indicator

The status indicator shows the current state of the phone booth:
- **Idle**: No active session
- **Pickup**: Phone picked up, ready to speak
- **Listening**: Processing user input
- **Processing**: Generating AI response
- **Speaking**: Playing AI response
- **Hangup**: Session ended
- **Error**: Error occurred

### Personality Selection

Choose from five different personalities:
- **The Trickster**: Playful and mischievous
- **The Sage**: Wise and contemplative
- **The Muse**: Creative and inspiring
- **The Jester**: Humorous and entertaining
- **The Night Watch**: Mysterious and vigilant

### Conversation Modes

- **Chat**: General conversation
- **Riddle**: Riddle-based interactions
- **Haiku**: Haiku poetry mode
- **Story**: Storytelling mode

### Lighting Simulation

The lighting simulation shows how the physical booth's lighting would respond to the AI's speech:
- **Brightness**: Based on audio amplitude
- **Animation**: Real-time lighting changes
- **Visual Feedback**: Simulates the actual lighting effects

### Conversation History

View the complete conversation history with:
- **User Messages**: Your input
- **AI Responses**: Generated responses
- **Timestamps**: When each message was sent
- **Processing Time**: How long the AI took to respond
- **Scene Information**: Context from the simulated environment

### Statistics

Real-time statistics show:
- **Total Conversations**: Number of sessions started
- **Total Turns**: Number of message exchanges
- **Average Processing Time**: Mean response time
- **Uptime**: How long the system has been running

## API Endpoints

The web UI uses the following API endpoints:

### Status
- `GET /api/status` - Get current booth status

### Session Management
- `POST /api/pickup` - Start a new session
- `POST /api/hangup` - End the current session

### Communication
- `POST /api/speak` - Send a message and get response
- `GET /api/conversation` - Get conversation history

### Configuration
- `GET /api/personalities` - Get available personalities and modes

## Troubleshooting

### Backend Not Accessible

**Error**: "Backend not accessible at http://localhost:8080"

**Solution**:
1. Ensure the backend is running: `backend\run_backend.bat`
2. Check if port 8080 is available
3. Verify the backend configuration in `config/backend.json`

### Web UI Won't Start

**Error**: "Failed to start web UI"

**Solution**:
1. Check if port 5000 is available
2. Install dependencies: `pip install -r frontend/web_ui/requirements.txt`
3. Ensure you're in a virtual environment

### No Response from AI

**Error**: "Backend error" or no response

**Solution**:
1. Check backend logs for errors
2. Verify LLM engine configuration
3. Ensure model files are accessible (if using llama_cpp)
4. Check network connectivity between frontend and backend

### Session Errors

**Error**: "Session not found" or "Session expired"

**Solution**:
1. The web UI automatically handles session expiration
2. Try picking up the phone again
3. Check backend session configuration

## Development Features

### Real-time Updates

The web UI uses WebSocket connections for real-time updates:
- Status changes
- Conversation updates
- Statistics updates

### Error Handling

Comprehensive error handling for:
- Network connectivity issues
- Backend errors
- Session management problems
- Invalid user input

### Performance Monitoring

Real-time monitoring of:
- Response times
- Processing performance
- System uptime
- Conversation statistics

## Testing Scenarios

### Basic Functionality
1. Pick up phone with different personalities
2. Send simple messages
3. Verify responses are appropriate for the personality
4. Hang up phone

### Conversation Modes
1. Test each conversation mode
2. Verify mode-specific behavior
3. Check response quality and relevance

### Error Conditions
1. Test with backend offline
2. Test with invalid input
3. Test session expiration
4. Test network interruptions

### Performance Testing
1. Monitor response times
2. Test with long conversations
3. Check memory usage
4. Verify session cleanup

## Configuration

### Backend URL

The web UI connects to the backend at the URL specified in `config/frontend.json`:
```json
{
  "backend_url": "http://localhost:8080"
}
```

### Web UI Settings

The web UI runs on:
- **Host**: 0.0.0.0 (all interfaces)
- **Port**: 5000
- **Debug**: Enabled by default

### CORS Configuration

The web UI allows CORS from all origins for development. For production, configure appropriate CORS settings.

## Security Considerations

### Development Environment
- Debug mode enabled
- CORS allows all origins
- No authentication required
- HTTP only (no HTTPS)

### Production Deployment
- Disable debug mode
- Configure CORS properly
- Add authentication if needed
- Use HTTPS
- Configure proper firewall rules

## Integration with Physical Booths

The web UI uses the same backend API as the physical booths, ensuring:
- **Compatible Behavior**: Same responses and timing
- **Shared Configuration**: Uses the same personality and mode settings
- **Consistent Testing**: Validates the same code paths
- **Performance Validation**: Tests real backend performance

## Next Steps

1. **Test All Personalities**: Try each personality with different conversation modes
2. **Validate Responses**: Ensure responses are appropriate and engaging
3. **Performance Testing**: Monitor response times and system performance
4. **Integration Testing**: Test with real LLM models
5. **User Experience**: Gather feedback on the interface design

The web UI provides a complete testing environment for the Phone Booth System, allowing you to validate functionality before deploying to physical booths.
