# Audio Configuration UI Guide

## Overview
The Phone Booth System now includes a **web-based audio configuration interface** that allows users to easily select and configure their microphone and speaker devices without editing configuration files.

## ✅ Feature Complete

### What's New:
- **🎤 Audio Device Selection**: Choose from all available microphones and speakers
- **🔧 Device Testing**: Test selected devices before saving
- **💾 Easy Configuration**: Save settings with a single click
- **🔄 Real-time Updates**: Changes take effect immediately
- **📱 User-Friendly Interface**: No technical knowledge required

## Web UI Integration

### Audio Configuration Panel
The web UI now includes a dedicated "Audio Configuration" section with:

1. **Microphone Dropdown**: Lists all available input devices
2. **Speaker Dropdown**: Lists all available output devices  
3. **Test Buttons**: Test selected devices before saving
4. **Save Button**: Apply configuration changes

### Device Information Displayed:
- **Device Index**: Internal system identifier
- **Device Name**: Human-readable device name
- **Host API**: Audio system (MME, WASAPI, DirectSound, etc.)
- **Default Indicator**: Shows which device is system default

## API Endpoints

### Get Available Devices
```
GET /api/audio/devices
```
Returns all available input and output devices with metadata.

### Get Current Configuration
```
GET /api/audio/config
```
Returns current audio settings.

### Update Configuration
```
POST /api/audio/config
Content-Type: application/json

{
    "input_device": 21,
    "output_device": 16
}
```
Updates audio device configuration.

### Test Devices
```
GET /api/audio/test/input/{device_index}
GET /api/audio/test/output/{device_index}
```
Tests specific input or output devices.

## Usage Instructions

### 1. Access the Web UI
- Start the system: `start_system.bat`
- Open: http://localhost:5000
- Scroll down to "Audio Configuration" section

### 2. Select Devices
- **Microphone**: Choose your preferred input device
- **Speaker**: Choose your preferred output device
- **Default Option**: Leave empty to use system defaults

### 3. Test Devices
- Click "Test" next to microphone to record for 3 seconds
- Click "Test" next to speaker to play a test tone
- Verify devices work correctly before saving

### 4. Save Configuration
- Click "💾 Save Audio Settings"
- Configuration is saved to `config/frontend.json`
- Changes take effect immediately

## Device Recommendations

### For Best Quality:
- **Input**: Use WASAPI devices (lower latency)
- **Output**: Use WASAPI devices (better quality)
- **Sample Rate**: System automatically uses 16,000 Hz for speech

### For Phone Booth Setup:
- **Input**: Dedicated microphone (not webcam mic)
- **Output**: Speakers that will be mounted in booth
- **Test**: Always test devices before final installation

## Example Configuration

### High-Quality Setup:
```json
{
    "audio": {
        "input_device": 21,    // WASAPI webcam mic
        "output_device": 16    // WASAPI speakers
    }
}
```

### Default System Setup:
```json
{
    "audio": {
        "input_device": null,  // Use system default
        "output_device": null  // Use system default
    }
}
```

## Technical Details

### Audio Parameters (Fixed):
- **Sample Rate**: 16,000 Hz (optimized for speech recognition)
- **Channels**: 1 (mono, optimized for speech)
- **Chunk Size**: 1024 samples
- **Format**: 16-bit PCM

### Supported Audio APIs:
- **MME**: Windows Multimedia Extensions
- **DirectSound**: Direct Sound API
- **WASAPI**: Windows Audio Session API (recommended)
- **WDM-KS**: Windows Driver Model Kernel Streaming

### Fallback Behavior:
- If specified device is unavailable, falls back to system default
- If PyAudio is not available, shows error message
- If device test fails, shows detailed error information

## Troubleshooting

### Common Issues:

#### "Failed to load audio devices"
- Check if PyAudio is installed: `pip install pyaudio`
- Verify audio drivers are working
- Check Windows audio settings

#### "Device test failed"
- Ensure device is not in use by another application
- Check Windows privacy settings for microphone access
- Verify device is properly connected

#### "Configuration not saved"
- Check file permissions on `config/frontend.json`
- Ensure web UI has write access to config directory
- Restart web UI if configuration is cached

#### "No audio output"
- Check Windows volume settings
- Verify speaker connections
- Test with different output device

### Error Messages:
- **Success**: Green message confirming action completed
- **Error**: Red message with specific error details
- **Warning**: Yellow message with helpful suggestions
- **Info**: Blue message with status information

## Integration with Existing System

### Automatic Detection:
- Web UI automatically loads available devices on startup
- Current configuration is loaded and displayed
- Changes are immediately reflected in the system

### Configuration Persistence:
- Settings are saved to `config/frontend.json`
- Survives system restarts
- Compatible with existing configuration format

### Backward Compatibility:
- Existing config files continue to work
- Missing audio settings use system defaults
- No breaking changes to existing functionality

## Development Features

### For Developers:
- All audio APIs are RESTful and well-documented
- Error handling provides detailed feedback
- Configuration changes are atomic and safe
- Test endpoints for device validation

### For System Administrators:
- No manual configuration file editing required
- User-friendly interface for device management
- Comprehensive device testing capabilities
- Configuration backup and restore support

## Next Steps

### Potential Enhancements:
1. **Audio Level Monitoring**: Real-time input/output levels
2. **Device Profiles**: Save multiple configurations
3. **Automatic Device Detection**: Auto-select best devices
4. **Audio Quality Testing**: Measure latency and quality
5. **Network Audio**: Support for remote audio devices

### Integration Opportunities:
1. **Hardware Setup**: Integrate with booth hardware configuration
2. **System Monitoring**: Audio device health monitoring
3. **User Preferences**: Per-user audio settings
4. **Deployment Tools**: Automated audio configuration for installations

## Conclusion

The Audio Configuration UI provides a **user-friendly, powerful, and reliable** way to configure audio devices for the Phone Booth System. It eliminates the need for technical knowledge while providing comprehensive device management capabilities.

**Key Benefits:**
- ✅ **Easy to Use**: No technical knowledge required
- ✅ **Comprehensive**: All devices and APIs supported
- ✅ **Reliable**: Robust error handling and testing
- ✅ **Flexible**: Works with any audio setup
- ✅ **Future-Proof**: Extensible for new features

The system is now ready for **production deployment** with professional audio configuration capabilities! 🎉
