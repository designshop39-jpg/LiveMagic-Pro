# LiveMagic Pro - Developer Guide

## 🏗️ Project Structure

```
LiveMagic-Pro/
├── live_streamer_enhanced.py      # Main application
├── README.md                       # Project overview
├── INSTALLATION.md                 # Setup instructions
├── QUICKSTART.md                   # 5-minute quick start
├── FEATURES.md                     # Complete feature list
├── TROUBLESHOOTING.md              # Troubleshooting guide
├── DEVELOPMENT.md                  # Developer guide
├── API.md                          # API reference
├── requirements.txt                # Python dependencies
├── config.json                     # Default configuration
├── setup.sh                        # Linux/macOS setup script
├── setup.bat                       # Windows setup script
├── install.py                      # Python installer
├── .gitignore                      # Git ignore rules
└── logs/                           # Runtime logs directory
```

---

## 📦 Architecture

### Main Components

#### 1. **SystemMonitor** (Line ~280)
```python
class SystemMonitor:
    """Monitor CPU, RAM, Network, FPS, Bitrate"""
    - update(): Collect system metrics
    - get_avg_cpu(): Average CPU usage
    - get_avg_ram(): Average RAM usage
    - get_bitrate_mbps(): Network bitrate
```

#### 2. **EnhancedChannelPanel** (Line ~310)
```python
class EnhancedChannelPanel(ttk.Frame):
    """Single streaming channel"""
    - _build_ui(): Create UI tabs
    - add_files(): Add videos to playlist
    - start_stream(): Start streaming
    - stop_stream(): Stop streaming
    - _stream_worker(): FFmpeg handler thread
```

#### 3. **EnhancedApp** (Line ~970)
```python
class EnhancedApp:
    """Main application window"""
    - add_channel(): Create new channel
    - remove_channel(): Delete channel
    - _scheduler_loop(): Background scheduler
    - on_close(): Cleanup on exit
```

---

## 🔧 Key Functions

### Utility Functions (Lines 100-250)

#### FFmpeg Management
```python
def get_ffmpeg_path():
    """Get FFmpeg path, auto-download if needed"""
    # Returns path to FFmpeg binary or None

def detect_ffmpeg():
    """Check if FFmpeg is installed"""
    # Checks PATH and .cache/ffmpeg/

def download_ffmpeg():
    """Auto-download FFmpeg for Windows"""
    # Downloads from gyan.dev
```

#### Video Processing
```python
def get_duration(path):
    """Get video duration using ffprobe"""
    # Returns seconds or 0.0 on error

def write_concat_file(paths, out_path):
    """Write FFmpeg concat demuxer file"""
    # Creates playlist for seamless looping
```

#### Configuration
```python
def load_config():
    """Load from config.json"""
    # Returns dict with settings

def save_config(config):
    """Save to config.json"""
    # Persists user settings
```

---

## 🎬 Streaming Workflow

### Start Stream

1. **User clicks "▶ START"**
   - Validates playlist not empty
   - Validates stream key present
   - Creates worker thread

2. **_stream_worker() executes**
   - Gets FFmpeg path
   - Builds RTMP URL
   - Gets encoder/resolution/audio settings
   - Writes concat file
   - Builds FFmpeg command
   - Starts subprocess
   - Monitors until stopped

3. **FFmpeg Command** (Line ~890)
   ```bash
   ffmpeg -re -stream_loop -1 \
     -f concat -safe 0 -i playlist.txt \
     -c:v libx264 -preset veryfast \
     -b:v 3000k -maxrate 3000k -bufsize 6000k \
     -vf scale=1280:720 -pix_fmt yuv420p \
     -c:a aac -b:a 192k -ar 44100 -ac 2 \
     -f flv rtmp://...
   ```

4. **Progress Updates**
   - Monitor collects CPU/RAM/network
   - UI updates every 1 second
   - Progress bar reflects playlist position

5. **Stop Stream**
   - Set stop_flag
   - Terminate FFmpeg process
   - Reset UI
   - Close log file

---

## 🎨 UI Structure

### Tab-Based Interface

```
┌─ Channel Panel ─────────────────────┐
│ [Channel Name] ● STREAMING [Btns]   │
├─────────────────────────────────────┤
│ ┌─ Tabs ──────────────────────────┐ │
│ │ 📽 Playlist  🎬 Stream  📊 ...  │ │
│ ├──────────────────────────────────┤ │
│ │ [Listbox with videos]            │ │
│ │ [Buttons: Add, Delete, Clear]    │ │
│ │ [Loop/Shuffle options]           │ │
│ └──────────────────────────────────┘ │
├─────────────────────────────────────┤
│ 🔴 OFF  [▶ START]  [⏹ STOP]        │
└─────────────────────────────────────┘
```

### Configuration Hierarchy

```
app.config (global)
├── theme: "dark" | "light"
├── encoder: "H.264 (CPU)" | ...
├── resolution: "1280x720 (HD)" | ...
└── audio: "Standard" | ...

channel.config (per-channel override)
├── encoder
├── resolution
├── audio
└── watermark_file
```

---

## 🚀 Extension Points

### Adding New Encoder

1. Add to **ENCODER_PRESETS** (Line ~45)
```python
ENCODER_PRESETS = {
    "New Encoder": {
        "codec": "codec_name",
        "preset": "preset_name",
    },
    ...
}
```

2. Update **Settings Window** (Line ~750)
```python
for enc in ENCODER_PRESETS.keys():
    ttk.Radiobutton(...).pack()
```

3. FFmpeg automatically uses selected encoder

### Adding New Platform

1. Add to **PLATFORM_URLS** (Line ~51)
```python
PLATFORM_URLS = {
    "New Platform": "rtmp://platform.com/live/",
    ...
}
```

2. UI automatically adds to dropdown

### Adding New Resolution Preset

1. Add to **RESOLUTION_PRESETS** (Line ~58)
```python
RESOLUTION_PRESETS = [
    ("1024x576 (Custom)", 1024, 576, 2000),
    ...
]
```

---

## 🔄 Threading Model

### Main Thread
- Tkinter event loop
- UI updates
- User input handling

### Stream Worker Thread
- FFmpeg subprocess
- Log file writing
- Blocking operations

### Scheduler Thread
- Background daemon
- Checks time every 1 second
- Auto-triggers streams

### Communication
```python
def after_gui(self, fn):
    """Run function on GUI thread from worker thread"""
    self.after(0, fn)  # Schedule on main thread
```

---

## 📝 File Format Standards

### config.json
```json
{
  "theme": "dark",
  "encoder": "H.264 (CPU)",
  "resolution": "1280x720 (HD)",
  "audio": "Standard"
}
```

### Log File (channel_N.log)
```
============================================================
2026-07-22 13:00:00.000000 - Stream started
============================================================
Command: ffmpeg -re -stream_loop -1 ...

[Output from FFmpeg ...]
frame=  150 fps= 30 q=-1.0 Lsize=...
```

### Concat File (channel_N_playlist.txt)
```
file '/absolute/path/to/video1.mp4'
file '/absolute/path/to/video2.mp4'
file '/absolute/path/to/video3.mp4'
```

---

## 🐛 Debugging

### Enable Debug Mode
```bash
python -u live_streamer_enhanced.py 2>&1 | tee debug.log
```

### Check Logs
```bash
# View recent stream logs
tail -f logs/channel_1.log

# View all logs
cat logs/channel_*.log
```

### FFmpeg Debugging
```bash
# Test FFmpeg with verbose output
ffmpeg -v debug -i input.mp4 -f flv rtmp://...

# Validate concat file
ffmpeg -f concat -i playlist.txt -c copy -f null -
```

---

## 📊 Performance Considerations

### Memory Usage
- **Idle**: ~50-100 MB
- **Streaming**: ~200-400 MB
- **Multiple channels**: +100-150 MB each

### CPU Usage
- **H.264 (CPU)**: 30-80% (depends on resolution)
- **NVENC/QuickSync**: 5-20%
- **Monitor updates**: ~1% (1 per second)

### Disk I/O
- **Log files**: ~1-5 MB per hour streaming
- **Temp files**: Negligible
- **Cache**: <100 MB

---

## 🔐 Security Considerations

### Stream Keys
- Never logged (masked with *)
- Stored in config.json (not encrypted)
- Recommend: Store in password manager

### File Access
- All files read as string paths
- No absolute path validation
- User responsible for file permissions

### Network
- No authentication required
- RTMPS (TLS) supported
- No proxy support (yet)

---

## 🧪 Testing

### Unit Testing Ideas
```python
def test_get_duration():
    assert get_duration("test.mp4") > 0

def test_fmt_time():
    assert fmt_time(3661) == "01:01:01"

def test_config_persistence():
    save_config({"test": "value"})
    assert load_config()["test"] == "value"
```

### Manual Testing
1. Test with different video formats
2. Test with different resolutions
3. Test with GPU encoders (if available)
4. Test scheduler with short intervals
5. Test with 10+ channels
6. Test stream interruption recovery

---

## 📚 Code Style

### Conventions
- Snake_case for functions/variables
- PascalCase for classes
- UPPER_CASE for constants
- 4-space indentation
- Comments for complex logic
- Docstrings for public functions

### Example
```python
def get_ffmpeg_path():
    """Get FFmpeg path, auto-download if needed"""
    ffmpeg = detect_ffmpeg()
    if ffmpeg:
        return ffmpeg
    
    if get_os_type() == "windows":
        ffmpeg = download_ffmpeg()
        if ffmpeg:
            return ffmpeg
    
    return None
```

---

## 🚀 Contribution Workflow

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes
4. Test thoroughly
5. Commit with clear message: `git commit -m "Add new feature"`
6. Push: `git push origin feature/your-feature`
7. Create Pull Request

---

## 📖 Additional Resources

- FFmpeg Documentation: https://ffmpeg.org/documentation.html
- Tkinter Guide: https://docs.python.org/3/library/tkinter.html
- RTMP Protocol: https://en.wikipedia.org/wiki/Real_Time_Messaging_Protocol
- FFprobe Reference: https://ffmpeg.org/ffprobe.html

---

**Happy coding! 🚀**
