import os
import json
from pathlib import Path
from config import settings
import logging

logger = logging.getLogger(__name__)

class SourceManager:
    """Manage different stream source types"""
    
    @staticmethod
    def parse_local_video(path):
        """Parse local video file"""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        supported_formats = [".mp4", ".mkv", ".mov", ".avi", ".flv", ".ts", ".webm"]
        if file_path.suffix.lower() not in supported_formats:
            raise ValueError(f"Unsupported format: {file_path.suffix}")
        
        return {
            "type": "local_video",
            "path": str(file_path),
            "filename": file_path.name,
            "size": file_path.stat().st_size,
            "format": file_path.suffix.lower()
        }
    
    @staticmethod
    def parse_folder_playlist(folder_path):
        """Parse folder and create playlist"""
        folder = Path(folder_path)
        if not folder.is_dir():
            raise NotADirectoryError(f"Not a directory: {folder_path}")
        
        supported_formats = [".mp4", ".mkv", ".mov", ".avi", ".flv", ".ts", ".webm"]
        videos = []
        
        for file in sorted(folder.iterdir()):
            if file.is_file() and file.suffix.lower() in supported_formats:
                videos.append({
                    "path": str(file),
                    "filename": file.name,
                    "size": file.stat().st_size
                })
        
        return {
            "type": "folder_playlist",
            "folder_path": str(folder),
            "video_count": len(videos),
            "videos": videos
        }
    
    @staticmethod
    def parse_iptv_m3u(m3u_path):
        """Parse IPTV .m3u playlist file"""
        file_path = Path(m3u_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {m3u_path}")
        
        if file_path.suffix.lower() != ".m3u":
            raise ValueError("File must be .m3u format")
        
        channels = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    # Extract channel info
                    parts = line.split(",")
                    channel_name = parts[-1] if len(parts) > 1 else "Unknown"
                elif line.startswith("http"):
                    channels.append({
                        "name": channel_name,
                        "url": line,
                        "type": "iptv_stream"
                    })
        
        return {
            "type": "iptv",
            "file_path": str(file_path),
            "channel_count": len(channels),
            "channels": channels
        }
    
    @staticmethod
    def validate_http_url(url):
        """Validate HTTP video URL"""
        import requests
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'video' in content_type or url.endswith(('.mp4', '.mkv', '.mov', '.m3u8')):
                    return {
                        "type": "http_url",
                        "url": url,
                        "content_type": content_type,
                        "size": response.headers.get('content-length', 'Unknown')
                    }
        except Exception as e:
            logger.error(f"Error validating URL: {e}")
        
        raise ValueError(f"Invalid or inaccessible HTTP URL: {url}")
    
    @staticmethod
    def validate_rtmp_input(rtmp_url):
        """Validate RTMP input stream"""
        if not rtmp_url.startswith("rtmp"):
            raise ValueError("Invalid RTMP URL")
        
        return {
            "type": "rtmp_input",
            "url": rtmp_url,
            "protocol": "rtmp" if rtmp_url.startswith("rtmp://") else "rtmps"
        }
    
    @staticmethod
    def validate_hls_input(hls_url):
        """Validate HLS input stream"""
        if not hls_url.endswith(".m3u8"):
            raise ValueError("HLS URL must end with .m3u8")
        
        return {
            "type": "hls_input",
            "url": hls_url,
            "protocol": "hls"
        }
    
    @staticmethod
    def write_concat_file(video_files, output_path):
        """Write FFmpeg concat demuxer file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for video in video_files:
                abs_path = os.path.abspath(video).replace("\\", "/").replace("'", "'\\''")
                f.write(f"file '{abs_path}'\n")
        return str(output_path)
