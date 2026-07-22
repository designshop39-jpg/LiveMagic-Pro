#!/bin/bash
# LiveMagic Pro Setup Script for macOS/Linux

echo "============================================"
echo "LiveMagic Pro - Setup Script"
echo "============================================"
echo ""

# Check Python version
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Install dependencies
echo "[2/4] Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Check FFmpeg
echo "[3/4] Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n 1)
    echo "✅ $FFMPEG_VERSION"
else
    echo "⚠️  FFmpeg not found"
    echo "Install with: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
fi
echo ""

# Create directories
echo "[4/4] Creating directories..."
mkdir -p logs .cache
chmod +x live_streamer_enhanced.py
echo "✅ Directories created"
echo ""

echo "============================================"
echo "✅ Setup Complete!"
echo "============================================"
echo ""
echo "To start streaming:"
echo "  python3 live_streamer_enhanced.py"
echo ""
echo "Or simply:"
echo "  ./live_streamer_enhanced.py"
echo ""
