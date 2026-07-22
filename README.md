# LiveMagic Pro 🎬

**Multi-Channel Video Playlist → RTMP Live Streamer**

A powerful, feature-rich desktop application for streaming video playlists to YouTube, Facebook, Twitch, and custom RTMP servers with advanced monitoring and control.

---

## ✨ Features

### 📊 Dashboard & Monitoring
- **Real-time Statistics**: CPU, RAM, Network, FPS, Bitrate monitoring
- **Live Progress Tracking**: Current file elapsed time and total duration
- **Uptime Counter**: Track streaming session duration
- **Beautiful UI**: Dark/Light theme toggle
- **Multi-channel Support**: Unlimited concurrent streams

### 🎥 Stream Management
- **Multiple Platforms**: YouTube, Facebook, Twitch, Custom RTMP
- **Create/Edit/Delete Streams**: Full playlist control
- **Start/Stop/Restart**: Simple stream controls
- **Duplicate Streams**: Clone configurations
- **Auto-start Scheduling**: Schedule streams by time
- **Duration Limits**: Auto-stop after specified duration
- **Loop Playlists**: Repeat forever or for 30 days

### 📁 Media Support
- **Local Video Files**: MP4, MKV, MOV, AVI, FLV, TS, WebM
- **Folder Playlists**: Load entire directories
- **IPTV (.m3u)**: Stream from IPTV sources
- **HTTP URLs**: Stream from remote servers
- **RTMP/HLS Input**: Stream from broadcast sources

### ⚙️ Advanced Encoding
- **Hardware Encoding Support**:
  - NVIDIA NVENC (H.264)
  - Intel QuickSync
  - AMD AMF
- **CPU Encoding**: H.264 & H.265
- **Quality Presets**:
  - 1920x1080 (Full HD) - 5000 kbps
  - 1280x720 (HD) - 3000 kbps
  - 854x480 (SD) - 1500 kbps
  - 640x360 (Mobile) - 800 kbps

### 🎵 Audio Settings
- **High Quality**: 320 kbps @ 48kHz
- **Standard**: 192 kbps @ 44.1kHz
- **Low Bandwidth**: 128 kbps @ 44.1kHz
- **Custom Audio Control**: Bitrate, sample rate configuration

### 📋 Playlist Features
- **Drag & Drop Support**: Easy playlist management
- **Loop Playlist**: Repeat until stopped or duration limit
- **Shuffle Mode**: Randomize playback order
- **Auto Next**: Seamless transition between videos
- **Add/Delete/Clear**: Full playlist control

### 🔧 FFmpeg Management
- **Auto-detect**: Find existing FFmpeg installation
- **Auto-download**: Download FFmpeg automatically (Windows)
- **Custom Commands**: Advanced FFmpeg parameters
- **Hardware Encoding**: Full GPU acceleration support
- **Watermark Support**: Add overlays to streams
- **Background Music**: Mix audio tracks

### 📅 Scheduler
- **Schedule Streams**: Set specific start times
- **Repeat Options**:
  - Daily repetition
  - Weekly schedules
  - Monthly patterns
- **Auto-stop**: Automatic stream termination
- **Auto-restart**: Resume on failures

### 📊 Live Monitoring
- **CPU Usage**: Real-time CPU utilization
- **RAM Usage**: Memory consumption tracking
- **Network Speed**: Upload bandwidth monitoring
- **FPS Tracking**: Frame rate monitoring
- **Bitrate Display**: Current stream bitrate
- **Resolution Indicator**: Output resolution display
- **Uptime Counter**: Session duration

### 📝 Logging
- **Real-time Logs**: Live FFmpeg output display
- **Download Logs**: Save logs to file
- **Error Tracking**: Comprehensive error logging
- **Log Search**: Find specific events

### 📁 File Manager
- **Upload Files**: Add media to library
- **Delete/Rename**: Manage files
- **Search**: Find videos quickly
- **Folder Organization**: Organized file structure
- **Batch Operations**: Manage multiple files

### 🎨 Advanced Settings
- **Stream Quality Control**: Custom bitrate settings
- **Resolution Selection**: Pre-configured or custom
- **FPS Control**: Frame rate adjustment
- **Audio Settings**: Per-stream audio configuration
- **Watermark Overlay**: Add logos/text overlays
- **Background Music**: Audio overlay support
- **Theme Toggle**: Dark/Light modes

---

## 🚀 Installation

### Requirements
- **Python 3.9+**
- **FFmpeg & FFprobe** (auto-download available for Windows)
- **pip** (Python package manager)

### Step 1: Clone Repository
```bash
git clone https://github.com/designshop39-jpg/LiveMagic-Pro.git
cd LiveMagic-Pro
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install FFmpeg

**Windows:**
- Run the app and click "⚙ Settings" → "Download FFmpeg"
- Or manually download from: https://www.gyan.dev/ffmpeg/builds/

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### Step 4: Run Application
```bash
python live_streamer_enhanced.py
```

---

## 📖 Usage Guide

### Getting Started

1. **Launch the Application**
   ```bash
   python live_streamer_enhanced.py
   ```

2. **Add a Channel**
   - Click "➕ Add Channel" to create a new streaming channel
   - Rename if desired (default: Channel 1, Channel 2, etc.)

3. **Add Videos to Playlist**
   - Click on the "📽 Playlist" tab
   - Click "➕ Add" to select video files
   - Supported formats: MP4, MKV, MOV, AVI, FLV, TS, WebM

4. **Configure Stream Settings**
   - Click on the "🎬 Stream" tab
   - Select **Platform** (YouTube, Facebook, Twitch, or Custom)
   - Paste your **Stream Key** or RTMP URL
   - Configure **Schedule** (optional)
   - Set **Run Duration**

5. **Advanced Settings**
   - Click "⚙ Settings" button on the channel panel
   - Choose **Video Encoder** (CPU or GPU-accelerated)
   - Select **Resolution & Bitrate**
   - Configure **Audio Settings**
   - Enable **Watermark** (if needed)

6. **Start Streaming**
   - Ensure playlist has videos
   - Verify stream key is entered
   - Click "▶ START" button
   - Monitor **📊 Monitor** tab for statistics

7. **Monitor Stream**
   - View **CPU/RAM** usage
   - Track **Bitrate** and **Uptime**
   - Check **Progress** bar
   - Monitor in **📝 Logs** tab

8. **Stop Streaming**
   - Click "⏹ STOP" button
   - Stream will disconnect gracefully

### Stream Key Management

**YouTube:**
1. Go to https://studio.youtube.com
2. Click "Create" → "Go Live"
3. Select "Stream" tab
4. Copy the **Stream Key**
5. Paste in LiveMagic Pro

**Facebook:**
1. Go to facebook.com/live/producers
2. Create new live video
3. Copy the **Stream Key**
4. Paste in LiveMagic Pro

**Twitch:**
1. Go to twitch.tv/dashboard
2. Click "Creator Camp" → "Preferences"
3. Copy **Stream Key**
4. Paste in LiveMagic Pro

---

## ⚙️ Configuration

### config.json

Automatically created on first run. Edit to customize defaults:

```json
{
  "theme": "dark",
  "encoder": "H.264 (CPU)",
  "resolution": "1280x720 (HD)",
  "audio": "Standard"
}
```

### Keyboard Shortcuts
- `Ctrl+N`: New Channel
- `Ctrl+S`: Save Settings
- `Ctrl+Q`: Quit Application

---

## 🎥 Streaming Tips

### For YouTube Live
- Minimum bitrate: 1500 kbps
- Recommended: 3000-5000 kbps
- Resolution: 720p or 1080p
- FPS: 30 or 60

### For Facebook Live
- Bitrate: 2000-4000 kbps
- Resolution: 720p
- FPS: 30
- Vertical videos: 9:16 aspect ratio

### For Twitch
- Bitrate: 2500-6000 kbps
- Resolution: 720p or 1080p
- FPS: 60
- Use "Fast" preset for low latency

### Network Optimization
- Use wired Ethernet for stability
- Close bandwidth-heavy applications
- Monitor "📊 Monitor" tab
- If bitrate drops, reduce resolution

---

## 🐛 Troubleshooting

### FFmpeg Not Found
1. Click "⚙ Settings" → "Download FFmpeg"
2. Or manually add to PATH
3. Restart application

### Stream Connection Failed
1. Verify stream key is correct
2. Check internet connection
3. Verify platform selection
4. Check firewall settings
5. Review logs in "📝 Logs" tab

### Low Bitrate/High Latency
1. Reduce resolution in settings
2. Lower bitrate setting
3. Use faster encoder preset
4. Check network connection
5. Reduce other applications' network usage

### High CPU Usage
1. Switch to GPU encoder (NVENC/QuickSync/AMF)
2. Lower resolution
3. Reduce FPS
4. Use faster encoder preset

### Audio Issues
1. Check audio settings in Stream tab
2. Verify audio bitrate (not too high)
3. Check system audio levels
4. Try different sample rate

### Playlist Not Playing
1. Verify video formats are supported
2. Check video file integrity
3. Ensure files are not corrupted
4. Try re-adding files to playlist
5. Check FFmpeg logs

---

## 📊 System Requirements

### Minimum
- **CPU**: Intel Core i3 or equivalent
- **RAM**: 4 GB
- **Storage**: 500 MB
- **Internet**: 5 Mbps upload
- **OS**: Windows 7+, macOS 10.13+, Linux (Ubuntu 18.04+)

### Recommended
- **CPU**: Intel Core i5/i7 or AMD Ryzen 5/7
- **RAM**: 8-16 GB
- **Storage**: SSD with 2 GB free space
- **Internet**: 10+ Mbps upload
- **GPU**: NVIDIA/Intel/AMD for hardware encoding

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📧 Support

For issues, feature requests, or questions:
- Create an issue on GitHub
- Check existing issues for solutions
- Review troubleshooting section

---

## 🙏 Credits

- Built with Python & Tkinter
- FFmpeg for video encoding
- psutil for system monitoring

---

## 🚀 Roadmap

- [ ] Web interface
- [ ] Mobile app support
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Cloud backup for presets
- [ ] Custom overlays editor
- [ ] Scene transitions
- [ ] Audio mixing board
- [ ] Video effects library
- [ ] API for integrations

---

**Made with ❤️ for content creators**
