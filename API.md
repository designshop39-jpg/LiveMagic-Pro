# LiveMagic Pro - API Reference

## 📡 Utility Functions

### FFmpeg Management

#### `get_ffmpeg_path() -> str | None`
Get FFmpeg path, auto-download if needed.

**Returns:**
- `str`: Path to FFmpeg executable
- `None`: FFmpeg not found

**Example:**
```python
ffmpeg_path = get_ffmpeg_path()
if ffmpeg_path:
    print(f"Using FFmpeg: {ffmpeg_path}")
```

---

#### `detect_ffmpeg() -> str | None`
Check if FFmpeg is in PATH or cache.

**Returns:**
- `str`: Path if found
- `None`: Not found

**Example:**
```python
if detect_ffmpeg():
    print("FFmpeg is installed")
```

---

#### `download_ffmpeg() -> str | None`
Auto-download FFmpeg (Windows only).

**Returns:**
- `str`: Path to downloaded FFmpeg
- `None`: Download failed

**Note:** Only works on Windows. Uses gyan.dev builds.

---

### Video Processing

#### `get_duration(path: str) -> float`
Get video duration using ffprobe.

**Args:**
- `path` (str): Path to video file

**Returns:**
- `float`: Duration in seconds (0.0 on error)

**Example:**
```python
duration = get_duration("video.mp4")
print(f"Duration: {fmt_time(duration)}")
```

---

#### `fmt_time(seconds: float) -> str`
Format seconds to HH:MM:SS.

**Args:**
- `seconds` (float): Seconds to format

**Returns:**
- `str`: Formatted time ("MM:SS" or "HH:MM:SS")

**Example:**
```python
print(fmt_time(3661))  # "01:01:01"
print(fmt_time(61))    # "01:01"
```

---

#### `write_concat_file(paths: list, out_path: str) -> None`
Write FFmpeg concat demuxer file.

**Args:**
- `paths` (list): List of file paths
- `out_path` (str): Output concat file path

**Side Effects:**
- Creates/overwrites file at `out_path`

**Example:**
```python
videos = ["/path/to/video1.mp4", "/path/to/video2.mp4"]
write_concat_file(videos, "playlist.txt")
```

---

### Configuration

#### `load_config() -> dict`
Load configuration from config.json.

**Returns:**
- `dict`: Configuration with keys:
  - `theme` (str): "dark" or "light"
  - `encoder` (str): Encoder preset name
  - `resolution` (str): Resolution preset name
  - `audio` (str): Audio preset name

**Defaults:**
```python
{
    "theme": "dark",
    "encoder": "H.264 (CPU)",
    "resolution": "1280x720 (HD)",
    "audio": "Standard"
}
```

---

#### `save_config(config: dict) -> None`
Save configuration to config.json.

**Args:**
- `config` (dict): Configuration dictionary

**Side Effects:**
- Creates/overwrites config.json

---

### Helpers

#### `get_os_type() -> str`
Get operating system type.

**Returns:**
- `"windows"`: Windows OS
- `"darwin"`: macOS
- `"linux"`: Linux

---

## 🎬 SystemMonitor Class

### Methods

#### `__init__()`
Initialize system monitor with empty history.

**Attributes:**
- `cpu_history` (deque): Last 60 CPU readings
- `ram_history` (deque): Last 60 RAM readings
- `net_history` (deque): Last 60 network readings
- `fps` (float): Current FPS
- `bitrate` (float): Current bitrate
- `process` (Process): Optional monitored process

---

#### `update() -> None`
Update system metrics.

**Side Effects:**
- Appends CPU, RAM, network values to history
- Maintains rolling 60-second window

**Example:**
```python
monitor = SystemMonitor()
monitor.update()
print(f"CPU: {monitor.get_avg_cpu()}%")
```

---

#### `get_avg_cpu() -> float`
Get average CPU usage from history.

**Returns:**
- `float`: Average CPU percentage (0-100)

---

#### `get_avg_ram() -> float`
Get average RAM usage from history.

**Returns:**
- `float`: Average RAM percentage (0-100)

---

#### `get_bitrate_mbps() -> float`
Calculate network bitrate from history.

**Returns:**
- `float`: Bitrate in Mbps

**Formula:**
```
bitrate = (last_bytes - first_bytes) * 8 / (1_000_000 * 60)
```

---

## 🎮 EnhancedChannelPanel Class

### Properties

#### `playlist: list[str]`
List of video file paths in playlist.

#### `is_live: bool`
Whether stream is currently running.

#### `channel_no: int`
Unique channel number (1, 2, 3, ...).

### Methods

#### `add_files() -> None`
Open file dialog and add videos to playlist.

**Side Effects:**
- Modifies `self.playlist`
- Updates listbox UI

---

#### `del_selected() -> None`
Delete selected items from playlist.

**Side Effects:**
- Removes from `self.playlist`
- Updates listbox UI

---

#### `clear_playlist() -> None`
Clear entire playlist with confirmation.

**Side Effects:**
- Clears `self.playlist`
- Clears listbox UI

---

#### `start_stream() -> None`
Start streaming (creates worker thread).

**Validation:**
- Playlist not empty
- Stream key present

**Side Effects:**
- Sets `self.is_live = True`
- Creates FFmpeg subprocess
- Starts monitoring

**Raises:**
- Shows messagebox on validation error

---

#### `stop_stream() -> None`
Stop streaming gracefully.

**Side Effects:**
- Sets stop flag
- Terminates FFmpeg process
- Sets `self.is_live = False`
- Resets UI

---

#### `view_log() -> None`
Display log file in popup window.

**Side Effects:**
- Opens new window with last 60 lines of log

---

#### `paste_key() -> None`
Paste stream key from clipboard.

**Side Effects:**
- Updates `self.key_var` from clipboard

---

#### `open_settings() -> None`
Open advanced settings window.

**Window Contents:**
- Video encoder selection
- Resolution & bitrate selection
- Audio settings
- Watermark options

---

#### `refresh_log() -> None`
Refresh log display in Logs tab.

**Side Effects:**
- Reads log file (last 5000 chars)
- Updates log text widget

---

#### `save_log() -> None`
Save log to user-selected file.

**Side Effects:**
- Opens save dialog
- Writes log content to file

---

#### `clear_log() -> None`
Clear log file with confirmation.

**Side Effects:**
- Truncates log file
- Clears log text display

---

### Internal Methods

#### `_stream_worker() -> None`
FFmpeg streaming worker (runs in thread).

**Workflow:**
1. Validate FFmpeg available
2. Get encoder/resolution/audio settings
3. Build FFmpeg command
4. Start subprocess
5. Monitor progress
6. Handle stop signal
7. Cleanup

**Note:** Runs in separate thread via `threading.Thread`

---

#### `_build_rtmp_url() -> str`
Build RTMP URL from platform and key.

**Returns:**
- `str`: Full RTMP(S) URL

**Example:**
```python
self.platform_var.set("YouTube")
self.key_var.set("YOUR_KEY")
url = self._build_rtmp_url()
# url = "rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"
```

---

#### `after_gui(fn: Callable) -> None`
Schedule function on GUI thread from worker thread.

**Args:**
- `fn` (callable): Function to run

**Usage:**
```python
self.after_gui(lambda: self.status_var.set("Updated"))
```

---

## 🖥️ EnhancedApp Class

### Methods

#### `add_channel() -> None`
Create and add new streaming channel.

**Side Effects:**
- Creates EnhancedChannelPanel
- Adds to grid layout
- Appends to `self.channels`

---

#### `remove_channel(panel: EnhancedChannelPanel) -> None`
Remove streaming channel.

**Args:**
- `panel` (EnhancedChannelPanel): Channel to remove

**Side Effects:**
- Destroys panel widget
- Removes from `self.channels`
- Re-grids remaining panels

---

#### `toggle_theme() -> None`
Toggle between dark and light theme.

**Side Effects:**
- Updates config
- Saves to config.json
- Shows info messagebox (restart needed)

---

#### `check_ffmpeg() -> None`
Check FFmpeg status and show result.

**Side Effects:**
- Shows messagebox with FFmpeg path or error

---

#### `download_ffmpeg_action() -> None`
Download FFmpeg with confirmation.

**Side Effects:**
- Shows confirmation dialog
- Downloads FFmpeg (~200MB)
- Shows success/error messagebox

---

#### `open_ffmpeg_folder() -> None`
Open FFmpeg folder in file explorer.

**Side Effects:**
- Opens `.cache/ffmpeg/` folder

---

## 📊 Constants

### Platforms
```python
PLATFORM_URLS = {
    "YouTube": "rtmp://a.rtmp.youtube.com/live2/",
    "Facebook": "rtmps://live-api-s.facebook.com:443/rtmp/",
    "Twitch": "rtmp://live-tyo.twitch.tv/app/",
    "Custom URL": "",
}
```

### Encoders
```python
ENCODER_PRESETS = {
    "H.264 (CPU)": {"codec": "libx264", "preset": "veryfast", "crf": 23},
    "H.265 (CPU)": {"codec": "libx265", "preset": "veryfast", "crf": 23},
    "NVIDIA NVENC": {"codec": "h264_nvenc", "preset": "fast"},
    "Intel QuickSync": {"codec": "h264_qsv", "preset": "veryfast"},
    "AMD AMF": {"codec": "h264_amf", "preset": "veryfast"},
}
```

### Resolutions
```python
RESSOLUTION_PRESETS = [
    ("1920x1080 (Full HD)", 1920, 1080, 5000),
    ("1280x720 (HD)", 1280, 720, 3000),
    ("854x480 (SD)", 854, 480, 1500),
    ("640x360 (Mobile)", 640, 360, 800),
]
```

### Audio
```python
AUDIO_PRESETS = {
    "High Quality": {"bitrate": 320, "sample_rate": 48000},
    "Standard": {"bitrate": 192, "sample_rate": 44100},
    "Low Bandwidth": {"bitrate": 128, "sample_rate": 44100},
}
```

---

## 🔄 Event Flow

### Stream Start to Stop

```
User clicks "▶ START"
    ↓
start_stream() validates inputs
    ↓
set is_live = True
    ↓
spawn _stream_worker() thread
    ↓
[Thread] Build FFmpeg command
    ↓
[Thread] Start subprocess
    ↓
[Thread] Monitor loop:
  - Collect CPU/RAM metrics
  - Update progress bar
  - Check stop_flag
    ↓
User clicks "⏹ STOP"
    ↓
set stop_flag = True
    ↓
[Thread] Detects stop_flag
    ↓
[Thread] Terminate process
    ↓
[Thread] Reset UI
    ↓
set is_live = False
```

---

## 🎯 Common Usage Patterns

### Add Video and Stream
```python
channel = EnhancedChannelPanel(parent, app)
channel.playlist.append("/path/to/video.mp4")
channel.listbox.insert("end", "video.mp4")
channel.key_var.set("STREAM_KEY")
channel.platform_var.set("YouTube")
channel.start_stream()
```

### Monitor Stream
```python
while channel.is_live:
    monitor.update()
    cpu = monitor.get_avg_cpu()
    ram = monitor.get_avg_ram()
    bitrate = monitor.get_bitrate_mbps()
    time.sleep(1)
```

### Schedule Stream
```python
channel.sched_enabled.set(True)
channel.sched_time_var.set("18:00")
channel.run_mode_var.set("Fixed Duration")
channel.dur_hours.set("2")
channel.dur_mins.set("30")
# App auto-starts at 18:00 and runs for 2.5 hours
```

---

**For more details, check DEVELOPMENT.md**
