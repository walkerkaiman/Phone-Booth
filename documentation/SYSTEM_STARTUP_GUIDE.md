# System Startup Guide

This guide explains how to use the master startup scripts to launch the entire Phone Booth System with a single command.

## Overview

The master startup scripts (`start_system.bat` for Windows, `start_system.sh` for macOS/Linux) provide a convenient way to start the entire Phone Booth System with one command. They handle:

- Starting the backend server
- Waiting for the backend to be ready
- Launching the frontend (which automatically starts the web UI)
- Managing multiple processes
- Providing clear status updates

## Quick Start

### Prerequisites

1. **Virtual Environment**: Ensure your virtual environment is activated
2. **Dependencies**: Install all required dependencies
3. **Backend Configuration**: Ensure `config/backend.json` is properly configured

### Windows

```bat
start_system.bat
```

### macOS/Linux

```bash
./start_system.sh
```

## What Happens

### Step 1: Environment Check
- Verifies virtual environment is activated
- Changes to project root directory
- Provides helpful error messages if setup is incomplete

### Step 2: Backend Startup
- Starts the backend server in a new window/background process
- Displays the backend process ID (macOS/Linux)
- Shows "Backend starting..." status

### Step 3: Backend Health Check
- Polls `http://localhost:8080/healthz` every 2 seconds
- Waits for backend to respond with HTTP 200
- Shows "Still waiting for backend..." until ready
- Displays "Backend is ready!" when accessible

### Step 4: Frontend Launch
- Starts the frontend application
- Automatically launches the web UI (included in frontend startup)
- Opens applications in separate windows/processes

### Step 5: System Ready
- Displays success message with access URLs
- Shows process IDs for management
- Provides instructions for stopping the system

## Access URLs

Once the system is started, you can access:

- **Backend API**: http://localhost:8080
- **Web UI**: http://localhost:5000
- **Backend Health Check**: http://localhost:8080/v1/healthz

## Process Management

### Windows
- Backend runs in a separate command window titled "Phone Booth Backend"
- Frontend runs in a separate command window titled "Phone Booth Frontend"
- Close the respective windows to stop individual services

### macOS/Linux
- Both processes run in the background
- Process IDs are displayed for management
- Use `kill <PID>` to stop individual processes
- Press `Ctrl+C` in the master script to stop all processes

## Stopping the System

### Windows
1. Close the "Phone Booth Backend" window to stop the backend
2. Close the "Phone Booth Frontend" window to stop the frontend
3. Close the master script window

### macOS/Linux
1. Press `Ctrl+C` in the master script terminal
2. The script will automatically stop both backend and frontend processes
3. Alternatively, use `kill <BACKEND_PID> <FRONTEND_PID>` with the displayed PIDs

## Troubleshooting

### Backend Won't Start
**Symptoms**: Script hangs at "Still waiting for backend..."

**Solutions**:
1. Check if port 8080 is available
2. Verify backend configuration in `config/backend.json`
3. Check backend logs in the backend window
4. Ensure all dependencies are installed

### Frontend Won't Start
**Symptoms**: Backend starts but frontend fails

**Solutions**:
1. Check if port 5000 is available (web UI)
2. Verify frontend configuration in `config/frontend.json`
3. Ensure backend is accessible at http://localhost:8080
4. Check frontend logs in the frontend window

### Virtual Environment Issues
**Symptoms**: "Virtual environment not detected" error

**Solutions**:
1. Activate your virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
2. Ensure you're in the project root directory
3. Verify the virtual environment exists

### Port Conflicts
**Symptoms**: "Address already in use" errors

**Solutions**:
1. Check if other services are using ports 8080 or 5000
2. Stop conflicting services
3. Modify configuration to use different ports
4. Use `netstat -an | findstr :8080` (Windows) or `lsof -i :8080` (macOS/Linux) to identify conflicts

## Advanced Usage

### Custom Ports
If you need to use different ports:

1. Modify `config/backend.json`:
   ```json
   {
     "server": {
       "port": 8081
     }
   }
   ```

2. Update the health check URL in the startup script:
   ```bash
   # In start_system.sh
   httpx.get('http://localhost:8081/healthz', timeout=5)
   ```

### Background Operation
For production deployment:

1. Use `nohup` on macOS/Linux:
   ```bash
   nohup ./start_system.sh > system.log 2>&1 &
   ```

2. Use Windows Task Scheduler for automatic startup

### Monitoring
Monitor system health:

1. Check backend health: `curl http://localhost:8080/v1/healthz`
2. Check web UI: `curl http://localhost:5000/api/status`
3. Monitor logs in respective windows/processes

## Integration with Development Workflow

### Development Mode
The master startup script is perfect for development:

1. **Quick Testing**: Start entire system with one command
2. **Integrated Testing**: Test both backend and frontend together
3. **Web UI Access**: Automatically get web interface for testing
4. **Process Management**: Easy to stop and restart

### Continuous Development
For ongoing development:

1. Start system with master script
2. Make code changes
3. Restart individual services as needed
4. Use web UI for immediate testing
5. Stop system when done

## Best Practices

1. **Always use virtual environment**: Ensures dependency isolation
2. **Check logs**: Monitor both backend and frontend windows for errors
3. **Test connectivity**: Verify both services are accessible before proceeding
4. **Clean shutdown**: Use proper stopping methods to avoid orphaned processes
5. **Regular restarts**: Restart system periodically during long development sessions

## Next Steps

1. **Test the System**: Use the web UI to test all personalities and modes
2. **Monitor Performance**: Check response times and system resources
3. **Customize Configuration**: Adjust settings in `config/` files
4. **Add Models**: Install and configure LLM models for production use
5. **Deploy**: Use the systemd scripts for production deployment

The master startup script provides a streamlined way to get the entire Phone Booth System running quickly and efficiently for development and testing.
