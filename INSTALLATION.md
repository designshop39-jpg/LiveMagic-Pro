# Installation Guide - LiveMagic Pro

## Prerequisites

- **Python 3.9 or higher**
- **pip** (Python package manager)
- **Git** (optional, for cloning)
- **5GB free disk space** (for FFmpeg)

---

## Step-by-Step Installation

### 1. Clone the Repository

**Using Git:**
```bash
git clone https://github.com/designshop39-jpg/LiveMagic-Pro.git
cd LiveMagic-Pro
```

**Or Download ZIP:**
- Go to https://github.com/designshop39-jpg/LiveMagic-Pro
- Click "Code" → "Download ZIP"
- Extract the ZIP file
- Open terminal in extracted folder

---

### 2. Install Python Dependencies

**Windows:**
```bash
pip install -r requirements.txt
```

**macOS:**
```bash
pip3 install -r requirements.txt
```

**Linux:**
```bash
pip install -r requirements.txt
```

---

### 3. Install FFmpeg

#### Windows

**Option A: Auto-Download (Recommended)**
1. Run the application
2. Click "⚙ Settings" button
3. Click "Download FFmpeg"
4. Wait for download to complete
5. FFmpeg will be installed automatically

**Option B: Manual Installation**
1. Download FFmpeg:
   - Go to https://www.gyan.dev/ffmpeg/builds/
   - Download "ffmpeg-release-essentials.zip"
2. Extract to a folder
3. Add to PATH:
   - Right-click "This PC" → "Properties"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", click "New"
   - Variable name: `PATH`
   - Variable value: `C:\path\to\ffmpeg\bin` (your FFmpeg bin folder)
   - Click OK
4. Restart terminal

#### macOS

**Using Homebrew (Recommended):**
```bash
brew install ffmpeg
```

**Or Manual Installation:**
1. Download from https://ffmpeg.org/download.html
2. Extract and add to PATH
3. Verify: `ffmpeg -version`

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
ffprobe -version
```

---

### 4. Verify Installation

**Check Python:**
```bash
python --version
```
Should show 3.9 or higher

**Check FFmpeg:**
```bash
ffmpeg -version
ffprobe -version
```
Should display version info

**Check Dependencies:**
```bash
pip show psutil
```
Should show psutil information

---

### 5. Run the Application

**Windows/macOS/Linux:**
```bash
python live_streamer_enhanced.py
```

Or:
```bash
python3 live_streamer_enhanced.py
```

---

## Troubleshooting Installation

### "Python not found"
- Install Python from https://www.python.org/downloads/
- Add Python to PATH during installation
- Restart terminal

### "pip: command not found"
- Python not properly installed
- Try `python -m pip` instead of `pip`
- On macOS/Linux, try `pip3`

### "FFmpeg not found"
- Verify FFmpeg is installed
- Check it's in your PATH
- Restart the application
- Or use auto-download from settings

### "Module not found"
- Reinstall requirements: `pip install -r requirements.txt`
- Use `pip install --upgrade` to update packages
- Check you're in the correct directory

### "Permission denied" (Linux/macOS)
- Run: `chmod +x live_streamer_enhanced.py`
- Or use: `python live_streamer_enhanced.py`

### Application won't start
1. Check Python version: `python --version`
2. Verify FFmpeg: `ffmpeg -version`
3. Check dependencies: `pip list`
4. Try running with `python -u live_streamer_enhanced.py` for debug output
5. Check logs in `.cache/logs/` folder

---

## System-Specific Notes

### Windows
- If using Python from Microsoft Store, install Visual C++ redistributable
- For GPU encoding (NVENC), install NVIDIA drivers
- For Intel QuickSync, update Intel drivers

### macOS
- Requires macOS 10.13 or higher
- May need to allow app in Security Settings
- GPU encoding may be limited on older Macs

### Linux
- Ubuntu 18.04 or higher recommended
- Some distributions may need additional libraries
- GPU encoding requires NVIDIA CUDA toolkit or AMD ROCm

---

## Performance Optimization

### For Better Streaming Quality
1. Install GPU drivers for your video card
2. Use hardware encoding (NVENC/QuickSync/AMF)
3. Allocate more RAM (close other applications)
4. Use wired internet connection
5. Use SSD for better file read performance

### For Lower CPU Usage
1. Enable hardware encoding in settings
2. Reduce resolution
3. Lower frame rate
4. Use faster encoder preset

---

## Next Steps

1. Read README.md for features overview
2. Check USAGE.md for detailed guide
3. Configure your first stream
4. Test with a local stream or test channel
5. Start streaming!

---

## Getting Help

- Check GitHub Issues: https://github.com/designshop39-jpg/LiveMagic-Pro/issues
- Review troubleshooting in README
- Check application logs in `logs/` folder
- Create new issue with error details

---

**Installation complete! Enjoy streaming with LiveMagic Pro! 🎬**
