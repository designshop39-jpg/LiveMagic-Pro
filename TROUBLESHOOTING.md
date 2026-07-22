# LiveMagic Pro - Troubleshooting Guide

## 🔧 Common Issues & Solutions

### Installation Issues

#### Python Not Found
**Error:** `python: command not found` or `'python' is not recognized`

**Solution:**
1. Install Python 3.9+ from https://www.python.org/downloads/
2. On Windows: ✅ Check "Add Python to PATH" during installation
3. Restart terminal/command prompt
4. Verify: `python --version`

---

#### pip Command Not Found
**Error:** `pip: command not found`

**Solution:**
```bash
# Try pip3 instead
pip3 install -r requirements.txt

# Or use python module
python -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```

---

#### Module Not Found
**Error:** `ModuleNotFoundError: No module named 'psutil'`

**Solution:**
```bash
pip install --upgrade psutil
# Or reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

---

### FFmpeg Issues

#### FFmpeg Not Found
**Error:** `FFmpeg not found. Install or allow auto-download.`

**Solution:**

**Windows:**
1. Click ⚙ Settings → Download FFmpeg
2. Wait for auto-download (~200MB)
3. Restart app

**Or manually:**
1. Download: https://www.gyan.dev/ffmpeg/builds/
2. Extract to folder (e.g., `C:\ffmpeg`)
3. Add to PATH:
   - Right-click This PC → Properties
   - Advanced system settings → Environment Variables
   - New variable: `PATH` = `C:\ffmpeg\bin`
4. Restart terminal
5. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

---

#### FFmpeg Download Failed
**Error:** `Failed to download FFmpeg`

**Solution:**
1. Check internet connection
2. Check firewall/proxy settings
3. Download manually:
   - https://www.gyan.dev/ffmpeg/builds/
   - Extract to `.cache/ffmpeg/`
4. Try again

---

### Streaming Issues

#### Stream Won't Connect
**Error:** Connection timeout or "Connection refused"

**Solution:**
1. ✅ **Verify Stream Key**
   - YouTube: https://studio.youtube.com/credentials/rt/manage
   - Facebook: facebook.com/live/producers
   - Twitch: twitch.tv → Settings → Channel
2. ✅ **Check Internet**
   - Test: `ping google.com`
   - Speed test: https://speedtest.net
   - Need: 5+ Mbps upload
3. ✅ **Check Firewall**
   - Allow LiveMagic Pro through firewall
   - Windows: Settings → Firewall → Allow app
4. ✅ **Verify Platform**
   - Correct platform selected?
   - YouTube/Facebook/Twitch/Custom?

---

#### Invalid Stream Key
**Error:** `401 Unauthorized` or `403 Forbidden`

**Solution:**
1. Generate new stream key
   - YouTube: Restart stream
   - Facebook: Create new live video
   - Twitch: Reset stream key in settings
2. Copy fresh key (don't mix up stream name/key)
3. Paste in app (use 👁 toggle to verify)
4. Try again

---

#### No Video Showing on Stream
**Error:** Stream connects but no video visible

**Solution:**
1. ✅ **Check Playlist**
   - Videos added?
   - File paths correct?
   - Files not moved/deleted?
2. ✅ **Check FFmpeg Logs**
   - 📝 Logs tab → Check for errors
   - Look for "Error" or "failed"
3. ✅ **Try Local File**
   - Add simple test video (e.g., short MP4)
   - Test with different format
4. ✅ **Check File Format**
   - Supported: MP4, MKV, MOV, AVI, FLV, TS, WebM
   - Verify with: `ffprobe video.mp4`

---

### Performance Issues

#### High CPU Usage (>90%)
**Symptoms:** App sluggish, fan loud, stuttering

**Solution:**
1. ✅ **Use GPU Encoding**
   - ⚙ Settings → Video Encoder
   - Select: NVIDIA NVENC / Intel QuickSync / AMD AMF
   - CPU should drop to 20-30%

2. ✅ **Lower Resolution**
   - ⚙ Settings → Resolution & Bitrate
   - Change: 1920x1080 → 1280x720 → 854x480

3. ✅ **Reduce FPS**
   - Default: 60 FPS
   - Try: 30 FPS

4. ✅ **Close Other Apps**
   - Close browsers, games, editors
   - Check Task Manager
   - Kill bandwidth hogs

---

#### High RAM Usage (>80%)
**Symptoms:** App becomes unresponsive

**Solution:**
1. Restart application
2. Close other applications
3. Reduce playlist size
4. Clear logs: 📝 Logs tab → 🗑 Clear Log
5. Restart computer

---

#### Low Bitrate / Buffering
**Symptoms:** Viewers see low quality, buffering

**Solution:**
1. ✅ **Check Internet Speed**
   - Need: 5-10 Mbps upload
   - Test: https://speedtest.net
   - Use: Ethernet (not WiFi)

2. ✅ **Reduce Bitrate in App**
   - ⚙ Settings → Resolution & Bitrate
   - Lower resolution
   - Lower bitrate preset

3. ✅ **Check Network**
   - Close other downloads
   - Disable VPN
   - Restart router

---

### Audio Issues

#### No Audio in Stream
**Symptoms:** Video plays but no sound

**Solution:**
1. ✅ **Check System Volume**
   - Unmute speakers
   - Check system volume
   - Verify headphones not plugged in

2. ✅ **Check Audio Settings**
   - ⚙ Settings → Audio Settings
   - Verify bitrate (not 0)
   - Try different preset

3. ✅ **Check Video Files**
   - Verify files have audio tracks
   - Test: `ffprobe -v error -select_streams a:0 -show_entries stream=codec_type video.mp4`
   - Re-encode if needed

4. ✅ **Reset Audio**
   - Restart application
   - Try different audio preset
   - Restart system

---

#### Distorted/Glitchy Audio
**Symptoms:** Audio crackling, stuttering, cutting out

**Solution:**
1. Lower audio bitrate in settings
2. Try different sample rate (44.1kHz vs 48kHz)
3. Reduce overall bitrate
4. Close audio apps (Discord, Spotify)
5. Update audio drivers

---

### UI Issues

#### App Won't Start
**Error:** Crashes on launch

**Solution:**
```bash
# Run with debug output
python -u live_streamer_enhanced.py

# Check for errors in console
# Delete config.json to reset settings
rm config.json
python live_streamer_enhanced.py
```

---

#### Window Too Small / Unreadable
**Symptoms:** UI elements cut off or tiny text

**Solution:**
1. Drag window to resize
2. Maximize window (double-click title bar)
3. Restart app
4. Check screen resolution (set to at least 1024x768)

---

#### Buttons Not Responding
**Symptoms:** Click button, nothing happens

**Solution:**
1. Wait 5-10 seconds (may be processing)
2. Check FFmpeg logs for errors
3. Restart application
4. Check if stream is still running (may be stuck)
5. Force quit and restart

---

### File Issues

#### File Not Found in Playlist
**Error:** "File not found" when starting stream

**Solution:**
1. ✅ **Verify File Path**
   - File still exists?
   - Path hasn't changed?
   - Correct filename spelling?

2. ✅ **Check File Permissions**
   - File readable?
   - Not locked by another app?

3. ✅ **Use Absolute Path**
   - Instead of relative path
   - Example: `C:\Videos\video.mp4`
   - Not: `..\..\videos\video.mp4`

---

#### Unsupported File Format
**Error:** "Format not recognized"

**Solution:**
1. Check file extension
2. Verify file format:
   ```bash
   ffprobe video.mp4
   ```
3. Convert if needed:
   ```bash
   ffmpeg -i input.mov -c:v libx264 -c:a aac output.mp4
   ```
4. Try different video

---

### Logging Issues

#### Can't View Logs
**Error:** Logs tab empty or error

**Solution:**
1. Start a stream (logs created on first stream)
2. Check logs directory exists: `logs/`
3. Verify permissions on log files
4. Try: 📝 Logs → 🔄 Refresh

---

#### Logs Growing Too Large
**Issue:** Log files taking up disk space

**Solution:**
1. 📝 Logs tab → 🗑 Clear Log
2. Or manually delete: `logs/channel_*.log`
3. Archive old logs if needed

---

### System-Specific Issues

#### Windows: Permission Denied
**Error:** `PermissionError: [Errno 13]`

**Solution:**
1. Run app as Administrator
2. Check file permissions
3. Disable antivirus temporarily
4. Try different folder for videos

---

#### macOS: App Not Opening
**Error:** "App is damaged" or "can't be opened"

**Solution:**
```bash
# Run from terminal instead
python3 live_streamer_enhanced.py

# Or remove quarantine
xattr -d com.apple.quarantine live_streamer_enhanced.py
```

---

#### Linux: Permission Denied
**Error:** `Permission denied` or `No such file or directory`

**Solution:**
```bash
# Make executable
chmod +x live_streamer_enhanced.py

# Run
./live_streamer_enhanced.py

# Or use python directly
python3 live_streamer_enhanced.py
```

---

## 📊 Getting Help

### Check Logs
1. 📝 Logs tab in app
2. Or view file: `logs/channel_N.log`
3. Look for **ERROR** or **warning** lines

### Debug Output
```bash
python -u live_streamer_enhanced.py 2>&1 | tee debug.log
```

### Report Issues
1. Gather information:
   - Python version: `python --version`
   - FFmpeg version: `ffmpeg -version`
   - OS (Windows/Mac/Linux)
   - Error message (full text)
2. Check existing issues: https://github.com/designshop39-jpg/LiveMagic-Pro/issues
3. Create new issue with details

### Performance Tips
- Use wired Ethernet
- Close unnecessary apps
- Use GPU encoding if available
- Keep videos reasonably sized
- Restart app daily for long streams

---

**Still having issues? Create an issue on GitHub with your error message and log files!**
