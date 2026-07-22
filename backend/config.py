import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "LiveMagic Pro"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./livestream.db"
    
    # FFmpeg
    FFMPEG_PATH: str = "ffmpeg"
    FFPROBE_PATH: str = "ffprobe"
    FFMPEG_AUTO_DOWNLOAD: bool = True
    
    # Storage
    BASE_DIR: Path = Path(__file__).parent.parent
    LOGS_DIR: Path = BASE_DIR / "logs"
    CACHE_DIR: Path = BASE_DIR / ".cache"
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    FFMPEG_DIR: Path = CACHE_DIR / "ffmpeg"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Streaming
    MAX_CONCURRENT_STREAMS: int = 10
    DEFAULT_BITRATE: int = 3000
    DEFAULT_RESOLUTION: str = "1280x720"
    DEFAULT_FPS: int = 30
    
    # Scheduler
    SCHEDULER_TIMEZONE: str = "UTC"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create directories
for directory in [settings.LOGS_DIR, settings.CACHE_DIR, settings.UPLOAD_DIR, settings.FFMPEG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
