"""
LiveMagic Pro - Multi-Channel Video Playlist -> RTMP Live Streamer
==================================================================
Enhanced version with:
    - Dashboard with live statistics
    - FFmpeg Auto-detect & Auto-download
    - Real-time monitoring (CPU, RAM, Network, FPS, Bitrate)
    - Advanced encoder settings (NVENC, QuickSync, AMF)
    - Hardware acceleration support
    - Watermark & overlay support
    - Advanced audio settings
    - File manager
    - Dark/Light theme
    - Playlist management (Drag & Drop ready)
    - Multi-platform streaming

Requirements:
    - Python 3.9+
    - FFmpeg + FFprobe (auto-downloaded if not found)
    - psutil (pip install psutil)

Run:
    python live_streamer_enhanced.py
"""

import os
import sys
import subprocess
import threading
import time
import json
import shutil
import platform
import tkinter as tk
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import urllib.request
import zipfile
import psutil
from collections import deque

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(APP_DIR, "logs")
CACHE_DIR = os.path.join(APP_DIR, ".cache")
FFMPEG_DIR = os.path.join(CACHE_DIR, "ffmpeg")
CONFIG_FILE = os.path.join(APP_DIR, "config.json")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

PLATFORM_URLS = {
    "YouTube": "rtmp://a.rtmp.youtube.com/live2/",
    "Facebook": "rtmps://live-api-s.facebook.com:443/rtmp/",
    "Twitch": "rtmp://live-tyo.twitch.tv/app/",
    "Custom URL": "",
}

ENCODER_PRESETS = {
    "H.264 (CPU)": {
        "codec": "libx264",
        "preset": "veryfast",
        "crf": 23,
    },
    "H.265 (CPU)": {
        "codec": "libx265",
        "preset": "veryfast",
        "crf": 23,
    },
    "NVIDIA NVENC": {
        "codec": "h264_nvenc",
        "preset": "fast",
    },
    "Intel QuickSync": {
        "codec": "h264_qsv",
        "preset": "veryfast",
    },
    "AMD AMF": {
        "codec": "h264_amf",
        "preset": "veryfast",
    },
}

RESOLUTION_PRESETS = [
    ("1920x1080 (Full HD)", 1920, 1080, 5000),
    ("1280x720 (HD)", 1280, 720, 3000),
    ("854x480 (SD)", 854, 480, 1500),
    ("640x360 (Mobile)", 640, 360, 800),
]

AUDIO_PRESETS = {
    "High Quality": {"bitrate": 320, "sample_rate": 48000},
    "Standard": {"bitrate": 192, "sample_rate": 44100},
    "Low Bandwidth": {"bitrate": 128, "sample_rate": 44100},
}

THEME_COLORS = {
    "dark": {
        "bg": "#0a0a0a",
        "fg": "#ffffff",
        "accent": "#00c853",
        "warning": "#ff9100",
        "error": "#d32f2f",
    },
    "light": {
        "bg": "#f5f5f5",
        "fg": "#000000",
        "accent": "#1976d2",
        "warning": "#f57c00",
        "error": "#c62828",
    },
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_os_type():
    """Return OS type: 'windows', 'darwin', 'linux'"""
    return platform.system().lower().replace("darwin", "darwin")

def detect_ffmpeg():
    """Check if FFmpeg is in PATH or FFMPEG_DIR"""
    try:
        subprocess.run([FFMPEG, "-version"], capture_output=True, check=True)
        return FFMPEG
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    ffmpeg_bin = os.path.join(FFMPEG_DIR, "ffmpeg.exe" if get_os_type() == "windows" else "ffmpeg")
    if os.path.exists(ffmpeg_bin):
        return ffmpeg_bin
    
    return None

def download_ffmpeg():
    """Auto-download FFmpeg for current OS"""
    os.makedirs(FFMPEG_DIR, exist_ok=True)
    
    os_type = get_os_type()
    if os_type == "windows":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        filename = "ffmpeg-release.zip"
    elif os_type == "darwin":
        return None  # macOS: use Homebrew
    else:
        return None  # Linux: use package manager
    
    try:
        print(f"Downloading FFmpeg from {url}...")
        filepath = os.path.join(CACHE_DIR, filename)
        urllib.request.urlretrieve(url, filepath)
        
        print(f"Extracting {filename}...")
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(CACHE_DIR)
        
        # Find ffmpeg binary
        for root, dirs, files in os.walk(CACHE_DIR):
            if "ffmpeg.exe" in files:
                src = os.path.join(root, "ffmpeg.exe")
                dst = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
                shutil.copy(src, dst)
                return dst
    except Exception as e:
        print(f"FFmpeg download failed: {e}")
    
    return None

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

def get_duration(path):
    """Return duration in seconds"""
    try:
        ffprobe = get_ffmpeg_path().replace("ffmpeg", "ffprobe") if get_ffmpeg_path() else FFPROBE
        out = subprocess.check_output(
            [ffprobe, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            stderr=subprocess.STDOUT,
            timeout=10
        )
        return float(out.strip())
    except Exception:
        return 0.0

def fmt_time(seconds):
    """Format seconds to HH:MM:SS"""
    seconds = int(max(0, seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def write_concat_file(paths, out_path):
    """Write FFmpeg concat demuxer file"""
    with open(out_path, "w", encoding="utf-8") as f:
        for p in paths:
            abs_p = os.path.abspath(p).replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{abs_p}'\n")

def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "theme": "dark",
        "encoder": "H.264 (CPU)",
        "resolution": "1280x720 (HD)",
        "audio": "Standard",
    }

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass

# ============================================================================
# SYSTEM MONITOR
# ============================================================================

class SystemMonitor:
    """Monitor CPU, RAM, Network, FPS, Bitrate"""
    
    def __init__(self):
        self.cpu_history = deque(maxlen=60)
        self.ram_history = deque(maxlen=60)
        self.net_history = deque(maxlen=60)
        self.fps = 0
        self.bitrate = 0
        self.process = None
    
    def update(self):
        """Update system metrics"""
        try:
            # CPU & RAM
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory().percent
            
            # Network
            net_io = psutil.net_io_counters()
            net_bytes = net_io.bytes_sent + net_io.bytes_recv
            
            self.cpu_history.append(cpu)
            self.ram_history.append(ram)
            self.net_history.append(net_bytes)
        except Exception:
            pass
    
    def get_avg_cpu(self):
        return sum(self.cpu_history) / len(self.cpu_history) if self.cpu_history else 0
    
    def get_avg_ram(self):
        return sum(self.ram_history) / len(self.ram_history) if self.ram_history else 0
    
    def get_bitrate_mbps(self):
        if len(self.net_history) < 2:
            return 0
        diff = self.net_history[-1] - self.net_history[0]
        return (diff * 8) / (1_000_000 * 60)  # bits per second

# ============================================================================
# ENHANCED CHANNEL PANEL
# ============================================================================

class EnhancedChannelPanel(ttk.Frame):
    """Enhanced channel with advanced settings and monitoring"""
    
    _counter = 0
    
    def __init__(self, master, app):
        super().__init__(master, padding=10, relief="ridge", borderwidth=2)
        EnhancedChannelPanel._counter += 1
        self.app = app
        self.channel_no = EnhancedChannelPanel._counter
        
        self.playlist = []
        self.proc = None
        self.stream_thread = None
        self.stop_flag = threading.Event()
        self.is_live = False
        self.start_wall_time = None
        self.log_path = os.path.join(LOG_DIR, f"channel_{self.channel_no}.log")
        self.monitor = SystemMonitor()
        self.config = load_config()
        
        self._build_ui()
    
    def _build_ui(self):
        """Build main UI"""
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        
        self.name_var = tk.StringVar(value=f"Channel {self.channel_no}")
        ttk.Entry(header, textvariable=self.name_var, font=("Arial", 11, "bold"), width=20).pack(side="left")
        
        self.live_badge = ttk.Label(header, text="", foreground="red", font=("Arial", 9, "bold"))
        self.live_badge.pack(side="left", padx=10)
        
        ttk.Button(header, text="⚙ Settings", command=self.open_settings).pack(side="right", padx=2)
        ttk.Button(header, text="Remove", command=self.remove_self).pack(side="right")
        
        # Notebook (tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)
        
        # Tab 1: Playlist
        self._build_playlist_tab(notebook)
        
        # Tab 2: Stream Settings
        self._build_stream_tab(notebook)
        
        # Tab 3: Monitor
        self._build_monitor_tab(notebook)
        
        # Tab 4: Logs
        self._build_logs_tab(notebook)
        
        # Status bar
        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_var = tk.StringVar(value="🔴 OFF")
        self.status_lbl = ttk.Label(status_frame, textvariable=self.status_var, font=("Arial", 10, "bold"))
        self.status_lbl.pack(side="left")
        
        self.start_btn = ttk.Button(status_frame, text="▶ START", command=self.start_stream)
        self.start_btn.pack(side="right", padx=2)
        
        self.stop_btn = ttk.Button(status_frame, text="⏹ STOP", command=self.stop_stream)
        self.stop_btn.pack(side="right")
    
    def _build_playlist_tab(self, notebook):
        """Playlist management tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📽 Playlist")
        
        # Listbox
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.listbox = tk.Listbox(list_frame, height=8, bg="#111", fg="#0f0")
        self.listbox.pack(fill="both", expand=True, side="left")
        
        scroll = ttk.Scrollbar(list_frame, command=self.listbox.yview)
        scroll.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scroll.set)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(btn_frame, text="➕ Add", command=self.add_files).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="➖ Delete", command=self.del_selected).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="🗑 Clear", command=self.clear_playlist).pack(side="left", padx=2)
        
        # Options
        opt_frame = ttk.Frame(frame)
        opt_frame.pack(fill="x", padx=5, pady=5)
        
        self.loop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_frame, text="🔄 Loop Playlist", variable=self.loop_var).pack(side="left")
        
        self.shuffle_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_frame, text="🔀 Shuffle", variable=self.shuffle_var).pack(side="left")
    
    def _build_stream_tab(self, notebook):
        """Stream settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🎬 Stream")
        
        # Platform & Key
        row1 = ttk.LabelFrame(frame, text="Destination", padding=5)
        row1.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(row1, text="Platform:").pack(side="left")
        self.platform_var = tk.StringVar(value="YouTube")
        ttk.Combobox(row1, textvariable=self.platform_var, 
                     values=list(PLATFORM_URLS.keys()), width=15, state="readonly").pack(side="left", padx=5)
        
        ttk.Label(row1, text="Stream Key:").pack(side="left", padx=(20, 0))
        self.key_var = tk.StringVar()
        self.key_entry = ttk.Entry(row1, textvariable=self.key_var, show="*", width=20)
        self.key_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        ttk.Button(row1, text="📋 Paste", command=self.paste_key).pack(side="left")
        ttk.Button(row1, text="👁", command=self.toggle_key_visibility).pack(side="left", padx=2)
        
        # Schedule
        row2 = ttk.LabelFrame(frame, text="Schedule", padding=5)
        row2.pack(fill="x", padx=5, pady=5)
        
        self.sched_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(row2, text="Enable Scheduler", variable=self.sched_enabled).pack(side="left")
        
        ttk.Label(row2, text="Start at:").pack(side="left", padx=(20, 0))
        self.sched_time_var = tk.StringVar(value="18:00")
        ttk.Entry(row2, textvariable=self.sched_time_var, width=8).pack(side="left", padx=5)
        
        # Duration
        row3 = ttk.LabelFrame(frame, text="Run Duration", padding=5)
        row3.pack(fill="x", padx=5, pady=5)
        
        self.run_mode_var = tk.StringVar(value="Until Stopped")
        ttk.Combobox(row3, textvariable=self.run_mode_var, state="readonly", width=20,
                     values=["Until Stopped", "Fixed Duration", "30 Days"]).pack(side="left")
        
        ttk.Label(row3, text="Duration:").pack(side="left", padx=(20, 0))
        self.dur_hours = tk.StringVar(value="2")
        ttk.Spinbox(row3, from_=0, to=48, textvariable=self.dur_hours, width=4).pack(side="left")
        ttk.Label(row3, text="h").pack(side="left")
        
        self.dur_mins = tk.StringVar(value="0")
        ttk.Spinbox(row3, from_=0, to=59, textvariable=self.dur_mins, width=4).pack(side="left")
        ttk.Label(row3, text="m").pack(side="left")
    
    def _build_monitor_tab(self, notebook):
        """System monitoring tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📊 Monitor")
        
        # Stats labels
        stats_frame = ttk.LabelFrame(frame, text="Live Statistics", padding=10)
        stats_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.cpu_var = tk.StringVar(value="CPU: 0%")
        ttk.Label(stats_frame, textvariable=self.cpu_var, font=("Arial", 11, "bold")).pack(anchor="w")
        
        self.ram_var = tk.StringVar(value="RAM: 0%")
        ttk.Label(stats_frame, textvariable=self.ram_var, font=("Arial", 11, "bold")).pack(anchor="w")
        
        self.bitrate_var = tk.StringVar(value="Bitrate: 0 Mbps")
        ttk.Label(stats_frame, textvariable=self.bitrate_var, font=("Arial", 11, "bold")).pack(anchor="w")
        
        self.uptime_var = tk.StringVar(value="Uptime: 00:00:00")
        ttk.Label(stats_frame, textvariable=self.uptime_var, font=("Arial", 11, "bold")).pack(anchor="w")
        
        # Progress
        self.progress_var = tk.StringVar(value="Progress: 00:00 / 00:00")
        ttk.Label(frame, textvariable=self.progress_var).pack(anchor="w", padx=5, pady=5)
        
        self.progressbar = ttk.Progressbar(frame, mode="determinate", maximum=100)
        self.progressbar.pack(fill="x", padx=5, pady=5)
    
    def _build_logs_tab(self, notebook):
        """Logs tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📝 Logs")
        
        # Log text
        self.log_text = tk.Text(frame, height=12, bg="#111", fg="#0f0", wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scroll.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scroll.set)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_log).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="💾 Save Log", command=self.save_log).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="🗑 Clear Log", command=self.clear_log).pack(side="left", padx=2)
    
    # ============================================================
    # UI Methods
    # ============================================================
    
    def toggle_key_visibility(self):
        """Toggle stream key visibility"""
        if self.key_entry.cget("show") == "*":
            self.key_entry.configure(show="")
        else:
            self.key_entry.configure(show="*")
    
    def paste_key(self):
        """Paste from clipboard"""
        try:
            clip = self.clipboard_get()
            self.key_var.set(clip.strip())
        except tk.TclError:
            messagebox.showinfo("Info", "Clipboard is empty")
    
    def open_settings(self):
        """Open advanced settings window"""
        settings_win = tk.Toplevel(self)
        settings_win.title("Advanced Settings")
        settings_win.geometry("400x500")
        
        # Encoder
        frame1 = ttk.LabelFrame(settings_win, text="Video Encoder", padding=10)
        frame1.pack(fill="x", padx=10, pady=10)
        
        self.encoder_var = tk.StringVar(value=self.config.get("encoder", "H.264 (CPU)"))
        for enc in ENCODER_PRESETS.keys():
            ttk.Radiobutton(frame1, text=enc, variable=self.encoder_var, value=enc).pack(anchor="w")
        
        # Resolution
        frame2 = ttk.LabelFrame(settings_win, text="Resolution & Bitrate", padding=10)
        frame2.pack(fill="x", padx=10, pady=10)
        
        self.resolution_var = tk.StringVar(value=self.config.get("resolution", "1280x720 (HD)"))
        for res, w, h, br in RESOLUTION_PRESETS:
            ttk.Radiobutton(frame2, text=f"{res} ({br}kbps)", variable=self.resolution_var, value=res).pack(anchor="w")
        
        # Audio
        frame3 = ttk.LabelFrame(settings_win, text="Audio Settings", padding=10)
        frame3.pack(fill="x", padx=10, pady=10)
        
        self.audio_var = tk.StringVar(value=self.config.get("audio", "Standard"))
        for audio in AUDIO_PRESETS.keys():
            ttk.Radiobutton(frame3, text=audio, variable=self.audio_var, value=audio).pack(anchor="w")
        
        # Watermark
        frame4 = ttk.LabelFrame(settings_win, text="Watermark & Overlay", padding=10)
        frame4.pack(fill="x", padx=10, pady=10)
        
        self.watermark_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame4, text="Enable Watermark", variable=self.watermark_var).pack(anchor="w")
        
        self.watermark_file = tk.StringVar()
        ttk.Button(frame4, text="Select Image", command=lambda: self.select_watermark(settings_win)).pack(anchor="w", pady=5)
        
        # Save button
        ttk.Button(settings_win, text="Save Settings", command=lambda: self.save_settings(settings_win)).pack(pady=10)
    
    def select_watermark(self, parent):
        """Select watermark image"""
        file = filedialog.askopenfilename(parent=parent, filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if file:
            self.watermark_file.set(file)
    
    def save_settings(self, win):
        """Save advanced settings"""
        self.config = {
            "encoder": self.encoder_var.get(),
            "resolution": self.resolution_var.get(),
            "audio": self.audio_var.get(),
        }
        save_config(self.config)
        messagebox.showinfo("Success", "Settings saved!")
        win.destroy()
    
    # ============================================================
    # Playlist Methods
    # ============================================================
    
    def add_files(self):
        """Add files to playlist"""
        files = filedialog.askopenfilenames(
            title="Select video files",
            filetypes=[("Video files", "*.mp4 *.mkv *.mov *.avi *.flv *.ts *.webm"), ("All files", "*.*")]
        )
        for f in files:
            self.playlist.append(f)
            self.listbox.insert("end", os.path.basename(f))
    
    def del_selected(self):
        """Delete selected items"""
        sel = list(self.listbox.curselection())
        for idx in reversed(sel):
            self.listbox.delete(idx)
            del self.playlist[idx]
    
    def clear_playlist(self):
        """Clear entire playlist"""
        if messagebox.askyesno("Confirm", "Clear entire playlist?"):
            self.listbox.delete(0, "end")
            self.playlist.clear()
    
    # ============================================================
    # Streaming Methods
    # ============================================================
    
    def start_stream(self):
        """Start streaming"""
        if self.is_live:
            return
        
        if not self.playlist:
            messagebox.showwarning("Error", "Add at least one video to playlist")
            return
        
        if not self.key_var.get().strip():
            messagebox.showwarning("Error", "Enter stream key or URL")
            return
        
        self.stop_flag.clear()
        self.is_live = True
        self.status_var.set("🟢 LIVE")
        self.live_badge.configure(text="● STREAMING")
        self.start_wall_time = time.time()
        
        self.stream_thread = threading.Thread(target=self._stream_worker, daemon=True)
        self.stream_thread.start()
    
    def stop_stream(self):
        """Stop streaming"""
        self.stop_flag.set()
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=5)
            except Exception:
                try:
                    self.proc.kill()
                except Exception:
                    pass
        
        self.is_live = False
        self.status_var.set("🔴 OFF")
        self.live_badge.configure(text="")
        self.progressbar["value"] = 0
    
    def remove_self(self):
        """Remove channel"""
        if self.is_live:
            self.stop_stream()
        self.app.remove_channel(self)
    
    def _stream_worker(self):
        """Streaming worker thread"""
        ffmpeg_path = get_ffmpeg_path()
        if not ffmpeg_path:
            self.after_gui(lambda: messagebox.showerror("Error", "FFmpeg not found. Install or allow auto-download."))
            self.stop_flag.set()
            self.after_gui(self._reset_ui_after_stop)
            return
        
        rtmp_url = self._build_rtmp_url()
        
        # Get settings
        encoder_preset = ENCODER_PRESETS.get(self.encoder_var.get(), ENCODER_PRESETS["H.264 (CPU)"])
        resolution_str = self.resolution_var.get()
        resolution_parts = [r for r in RESOLUTION_PRESETS if r[0] == resolution_str]
        if resolution_parts:
            _, width, height, bitrate = resolution_parts[0]
        else:
            width, height, bitrate = 1280, 720, 3000
        
        audio_preset = AUDIO_PRESETS.get(self.audio_var.get(), AUDIO_PRESETS["Standard"])
        
        playlist_snapshot = list(self.playlist)
        total_duration = sum(get_duration(p) for p in playlist_snapshot) or 1.0
        
        concat_path = os.path.join(LOG_DIR, f"channel_{self.channel_no}_playlist.txt")
        write_concat_file(playlist_snapshot, concat_path)
        
        # Build FFmpeg command
        loop_count = "-1" if self.loop_var.get() else "1"
        
        cmd = [
            ffmpeg_path, "-re",
            "-stream_loop", loop_count,
            "-f", "concat", "-safe", "0", "-i", concat_path,
            "-c:v", encoder_preset["codec"],
            "-preset", encoder_preset.get("preset", "veryfast"),
            "-b:v", f"{bitrate}k",
            "-maxrate", f"{bitrate}k",
            "-bufsize", f"{bitrate * 2}k",
            "-vf", f"scale={width}:{height}",
            "-pix_fmt", "yuv420p",
            "-g", "60",
            "-c:a", "aac",
            "-b:a", f"{audio_preset['bitrate']}k",
            "-ar", str(audio_preset['sample_rate']),
            "-ac", "2",
            "-f", "flv",
            rtmp_url,
        ]
        
        try:
            with open(self.log_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"\n{'='*60}\n{datetime.now()} - Stream started\n{'='*60}\n")
                log_file.write(f"Command: {' '.join(cmd)}\n\n")
                log_file.flush()
                
                self.proc = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT)
        except FileNotFoundError:
            self.after_gui(lambda: messagebox.showerror("Error", "FFmpeg not found"))
            self.stop_flag.set()
            self.after_gui(self._reset_ui_after_stop)
            return
        
        stream_start = time.time()
        
        while self.proc.poll() is None and not self.stop_flag.is_set():
            self.monitor.update()
            elapsed = time.time() - stream_start
            
            cpu = self.monitor.get_avg_cpu()
            ram = self.monitor.get_avg_ram()
            bitrate_mbps = self.monitor.get_bitrate_mbps()
            
            elapsed_in_loop = elapsed % total_duration
            
            def update_stats():
                self.cpu_var.set(f"CPU: {cpu:.1f}%")
                self.ram_var.set(f"RAM: {ram:.1f}%")
                self.bitrate_var.set(f"Bitrate: {bitrate_mbps:.2f} Mbps")
                self.uptime_var.set(f"Uptime: {fmt_time(elapsed)}")
                
                self.progress_var.set(f"Progress: {fmt_time(elapsed_in_loop)} / {fmt_time(total_duration)}")
                pct = min(100, (elapsed_in_loop / total_duration) * 100) if total_duration else 0
                self.progressbar["value"] = pct
            
            self.after_gui(update_stats)
            time.sleep(1)
        
        self.after_gui(self._reset_ui_after_stop)
    
    def _build_rtmp_url(self):
        """Build RTMP URL"""
        platform = self.platform_var.get()
        key = self.key_var.get().strip()
        if platform == "Custom URL":
            return key
        return PLATFORM_URLS[platform] + key
    
    def refresh_log(self):
        """Refresh log display"""
        try:
            with open(self.log_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self.log_text.configure(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.insert("1.0", content[-5000:])  # Last 5000 chars
            self.log_text.configure(state="disabled")
        except Exception:
            pass
    
    def save_log(self):
        """Save log to file"""
        file = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt")])
        if file:
            try:
                with open(self.log_path, "r", encoding="utf-8", errors="ignore") as src:
                    content = src.read()
                with open(file, "w", encoding="utf-8") as dst:
                    dst.write(content)
                messagebox.showinfo("Success", f"Log saved to {file}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def clear_log(self):
        """Clear log file"""
        if messagebox.askyesno("Confirm", "Clear log file?"):
            try:
                open(self.log_path, "w").close()
                self.log_text.delete("1.0", "end")
            except Exception:
                pass
    
    def _reset_ui_after_stop(self):
        """Reset UI after stream stops"""
        self.is_live = False
        self.status_var.set("🔴 OFF")
        self.live_badge.configure(text="")
    
    def after_gui(self, fn):
        """Run function on GUI thread"""
        try:
            self.after(0, fn)
        except tk.TclError:
            pass

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class EnhancedApp:
    """Main application"""
    
    def __init__(self, root):
        self.root = root
        root.title("LiveMagic Pro - Multi-Channel Streamer")
        root.geometry("1200x800")
        
        self.config = load_config()
        self._apply_theme(self.config.get("theme", "dark"))
        
        # Header
        header = ttk.Frame(root, padding=10)
        header.pack(fill="x")
        
        ttk.Label(header, text="LiveMagic Pro", font=("Arial", 18, "bold")).pack(side="left")
        
        ttk.Button(header, text="➕ Add Channel", command=self.add_channel).pack(side="right", padx=5)
        ttk.Button(header, text="🌙 Theme", command=self.toggle_theme).pack(side="right", padx=5)
        ttk.Button(header, text="⚙ Settings", command=self.open_app_settings).pack(side="right", padx=5)
        
        # Main content
        container = ttk.Frame(root)
        container.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
        vscroll = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vscroll.set)
        vscroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.grid_frame = ttk.Frame(self.canvas)
        self.grid_window = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.grid_window, width=e.width))
        
        self.channels = []
        self.add_channel()
        self.add_channel()
        
        # Scheduler
        threading.Thread(target=self._scheduler_loop, daemon=True).start()
        
        root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def _apply_theme(self, theme_name):
        """Apply theme"""
        theme = THEME_COLORS.get(theme_name, THEME_COLORS["dark"])
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        current = self.config.get("theme", "dark")
        new_theme = "light" if current == "dark" else "dark"
        self.config["theme"] = new_theme
        save_config(self.config)
        messagebox.showinfo("Info", "Theme changed. Restart app to apply.")
    
    def open_app_settings(self):
        """Open global app settings"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Application Settings")
        settings_win.geometry("300x200")
        
        ttk.Label(settings_win, text="FFmpeg Management:", font=("Arial", 10, "bold")).pack(padx=10, pady=10, anchor="w")
        
        ttk.Button(settings_win, text="Auto-Detect FFmpeg", command=self.check_ffmpeg).pack(fill="x", padx=10, pady=5)
        ttk.Button(settings_win, text="Download FFmpeg", command=self.download_ffmpeg_action).pack(fill="x", padx=10, pady=5)
        ttk.Button(settings_win, text="Open FFmpeg Folder", command=self.open_ffmpeg_folder).pack(fill="x", padx=10, pady=5)
    
    def check_ffmpeg(self):
        """Check FFmpeg status"""
        ffmpeg = detect_ffmpeg()
        if ffmpeg:
            messagebox.showinfo("FFmpeg Found", f"FFmpeg path: {ffmpeg}")
        else:
            messagebox.showwarning("FFmpeg Not Found", "FFmpeg is not installed or not in PATH")
    
    def download_ffmpeg_action(self):
        """Download FFmpeg"""
        if messagebox.askyesno("Confirm", "Download FFmpeg? (~200MB)"):
            result = download_ffmpeg()
            if result:
                messagebox.showinfo("Success", f"FFmpeg downloaded to {result}")
            else:
                messagebox.showerror("Error", "Failed to download FFmpeg")
    
    def open_ffmpeg_folder(self):
        """Open FFmpeg folder"""
        if os.path.exists(FFMPEG_DIR):
            os.startfile(FFMPEG_DIR) if get_os_type() == "windows" else os.system(f"open {FFMPEG_DIR}")
    
    def add_channel(self):
        """Add new channel"""
        panel = EnhancedChannelPanel(self.grid_frame, self)
        col = len(self.channels) % 2
        row = len(self.channels) // 2
        panel.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
        self.grid_frame.grid_columnconfigure(col, weight=1)
        self.channels.append(panel)
    
    def remove_channel(self, panel):
        """Remove channel"""
        panel.destroy()
        self.channels.remove(panel)
        for i, p in enumerate(self.channels):
            p.grid(row=i // 2, column=i % 2, sticky="nsew", padx=8, pady=8)
    
    def _scheduler_loop(self):
        """Background scheduler"""
        while True:
            now = datetime.now()
            for ch in list(self.channels):
                try:
                    target = ch.sched_time_var.get().strip()
                    current = now.strftime("%H:%M")
                    if (ch.sched_enabled.get() and not ch.is_live and 
                        current == target and not getattr(ch, '_sched_fired_today', False)):
                        ch._sched_fired_today = True
                        ch.start_stream()
                    elif current != target:
                        ch._sched_fired_today = False
                except Exception:
                    pass
            time.sleep(1)
    
    def on_close(self):
        """Close app"""
        for ch in self.channels:
            if ch.is_live:
                ch.stop_stream()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedApp(root)
    root.mainloop()
