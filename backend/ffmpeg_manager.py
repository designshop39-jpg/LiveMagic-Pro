import subprocess
import os
import platform
import urllib.request
import zipfile
from pathlib import Path
from config import settings
import logging

logger = logging.getLogger(__name__)

class FFmpegManager:
    """Manage FFmpeg installation and execution"""
    
    @staticmethod
    def detect_ffmpeg():
        """Detect if FFmpeg is installed and in PATH"""
        try:
            subprocess.run([settings.FFMPEG_PATH, "-version"], 
                         capture_output=True, check=True)
            logger.info(f"FFmpeg found at: {settings.FFMPEG_PATH}")
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False
    
    @staticmethod
    def get_ffmpeg_path():
        """Get FFmpeg path, download if needed"""
        if FFmpegManager.detect_ffmpeg():
            return settings.FFMPEG_PATH
        
        if settings.FFMPEG_AUTO_DOWNLOAD and platform.system() == "Windows":
            return FFmpegManager.download_ffmpeg()
        
        raise Exception("FFmpeg not found. Please install FFmpeg manually.")
    
    @staticmethod
    def download_ffmpeg():
        """Download FFmpeg for Windows"""
        try:
            logger.info("Downloading FFmpeg...")
            url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            filepath = settings.CACHE_DIR / "ffmpeg.zip"
            
            urllib.request.urlretrieve(url, filepath)
            logger.info("Extracting FFmpeg...")
            
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(settings.CACHE_DIR)
            
            # Find FFmpeg binary
            for root, dirs, files in os.walk(settings.CACHE_DIR):
                if "ffmpeg.exe" in files:
                    ffmpeg_path = os.path.join(root, "ffmpeg.exe")
                    logger.info(f"FFmpeg installed at: {ffmpeg_path}")
                    return ffmpeg_path
        
        except Exception as e:
            logger.error(f"Failed to download FFmpeg: {e}")
            raise
    
    @staticmethod
    def get_video_duration(file_path):
        """Get duration of a video file in seconds"""
        try:
            result = subprocess.run(
                [settings.FFPROBE_PATH, "-v", "error",
                 "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1",
                 file_path],
                capture_output=True,
                text=True
            )
            return float(result.stdout.strip())
        except Exception as e:
            logger.error(f"Error getting video duration: {e}")
            return 0.0
    
    @staticmethod
    def get_video_info(file_path):
        """Get detailed video information"""
        try:
            result = subprocess.run(
                [settings.FFPROBE_PATH, "-v", "error",
                 "-show_format", "-show_streams",
                 "-print_format", "json",
                 file_path],
                capture_output=True,
                text=True
            )
            import json
            return json.loads(result.stdout)
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {}
    
    @staticmethod
    def build_ffmpeg_command(playlist_file, output_url, bitrate=3000, 
                            resolution="1280x720", fps=30, audio_bitrate=192,
                            encoder="libx264"):
        """Build FFmpeg command for streaming"""
        return [
            settings.FFMPEG_PATH,
            "-re",
            "-f", "concat",
            "-safe", "0",
            "-i", playlist_file,
            "-c:v", encoder,
            "-preset", "veryfast",
            "-b:v", f"{bitrate}k",
            "-maxrate", f"{bitrate * 1.5}k",
            "-bufsize", f"{bitrate * 2}k",
            "-vf", f"scale={resolution.split('x')[0]}:{resolution.split('x')[1]}",
            "-r", str(fps),
            "-c:a", "aac",
            "-b:a", f"{audio_bitrate}k",
            "-ac", "2",
            "-f", "flv",
            output_url
        ]
