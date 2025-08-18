# Network Setup Guide

This guide explains how to deploy the Character Booth System with the backend on one computer and frontend(s) on separate computer(s) on the same network.

## Network Architecture

```
┌─────────────────┐    Network    ┌─────────────────┐
│   Backend PC    │◄─────────────►│  Frontend PC    │
│                 │               │                 │
│ • LLM Engine    │               │ • Audio I/O     │
│ • Session Store │               │ • Webcam        │
│ • API Server    │               │ • TTS/Lighting  │
│ • Port 8080     │               │ • HTTP Client   │
└─────────────────┘               └─────────────────┘
```

## Backend Setup (Server Computer)

### 1. Find Your Backend IP Address

**Windows:**
```cmd
ipconfig
```
Look for your network adapter (usually "Ethernet adapter" or "Wireless LAN adapter") and note the IPv4 address.

**macOS/Linux:**
```bash
ifconfig
# or
ip addr show
```

### 2. Configure Backend

The backend is already configured to accept network connections:
- **Host**: `0.0.0.0` (accepts connections from any IP)
- **Port**: `8080`
- **CORS**: Configured to allow cross-origin requests

### 3. Start Backend Server

```bash
# From project root
./backend/run_backend.sh
# or on Windows
backend\run_backend.bat
```

You should see:
```
Starting server on 0.0.0.0:8080...

Network Access:
  - Local: http://localhost:8080
  - Network: http://[YOUR_IP]:8080
  - Update config/frontend.json with your backend IP
```

### 4. Test Backend Accessibility

From another computer on the network:
```bash
curl http://[BACKEND_IP]:8080/healthz
```

Should return: `{"ok": true}`

## Frontend Setup (Booth Computer)

### 1. Update Frontend Configuration

Edit `config/frontend.json`:
```json
{
  "backend_url": "http://192.168.1.100:8080",
  "booth_id": "booth-12",
  ...
}
```

Replace `192.168.1.100` with your backend computer's actual IP address.

### 2. Test Network Connectivity

Before running the frontend, test connectivity:
```bash
# Test basic connectivity
ping [BACKEND_IP]

# Test HTTP connectivity
curl http://[BACKEND_IP]:8080/healthz
```

### 3. Start Frontend

```bash
# From project root
./frontend/run_frontend.sh
# or on Windows
frontend\run_frontend.bat
```

## Network Troubleshooting

### Common Issues

**1. Connection Refused**
- Check if backend is running
- Verify IP address is correct
- Ensure firewall allows port 8080

**2. CORS Errors**
- Backend CORS is configured to allow all origins (`*`)
- If issues persist, check browser console for specific errors

**3. Slow Response Times**
- Check network latency: `ping [BACKEND_IP]`
- Consider local LLM models for better performance

### Firewall Configuration

**Windows Firewall:**
1. Open Windows Defender Firewall
2. Click "Allow an app or feature through Windows Defender Firewall"
3. Click "Change settings" → "Allow another app"
4. Browse to your Python executable
5. Ensure both Private and Public are checked

**macOS Firewall:**
1. System Preferences → Security & Privacy → Firewall
2. Click "Firewall Options"
3. Add Python and allow incoming connections

**Linux (ufw):**
```bash
sudo ufw allow 8080
```

### Security Considerations

**For Production:**
1. **Restrict CORS**: Update `config/backend.json`:
   ```json
   {
     "server": {
       "cors_origins": ["http://192.168.1.101:3000", "http://192.168.1.102:3000"]
     }
   }
   ```

2. **Use HTTPS**: Set up SSL certificates for secure communication

3. **Network Isolation**: Consider VLANs or dedicated network segments

4. **Authentication**: Add API key or token-based authentication

## Multiple Frontends

To run multiple booth frontends:

1. **Unique Booth IDs**: Each frontend needs a unique `booth_id`:
   ```json
   // Booth 1
   {"booth_id": "booth-01", "backend_url": "http://192.168.1.100:8080"}
   
   // Booth 2  
   {"booth_id": "booth-02", "backend_url": "http://192.168.1.100:8080"}
   ```

2. **Backend Capacity**: The backend can handle multiple concurrent sessions

3. **Network Bandwidth**: Ensure sufficient bandwidth for multiple audio streams

## Monitoring

### Backend Health Check
```bash
curl http://[BACKEND_IP]:8080/healthz
```

### Network Latency
```bash
ping [BACKEND_IP]
```

### Port Status
```bash
# Check if port 8080 is listening
netstat -an | grep 8080
```

## Performance Optimization

1. **Local Models**: Use local LLM models for lower latency
2. **Network Quality**: Use wired Ethernet when possible
3. **Backend Resources**: Ensure sufficient CPU/RAM for LLM inference
4. **Audio Compression**: Consider audio compression for network transmission

## Example Network Configuration

**Typical Home Network:**
- Backend: `192.168.1.100:8080`
- Frontend 1: `192.168.1.101`
- Frontend 2: `192.168.1.102`

**Small Office Network:**
- Backend: `10.0.1.50:8080`
- Frontend 1: `10.0.1.51`
- Frontend 2: `10.0.1.52`
- Frontend 3: `10.0.1.53`
