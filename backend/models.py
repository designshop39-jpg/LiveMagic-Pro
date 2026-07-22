from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class SourceType(str, enum.Enum):
    LOCAL_VIDEO = "local_video"
    FOLDER_PLAYLIST = "folder_playlist"
    IPTV = "iptv"
    HTTP_URL = "http_url"
    RTMP_INPUT = "rtmp_input"
    HLS_INPUT = "hls_input"

class OutputPlatform(str, enum.Enum):
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    TWITCH = "twitch"
    CUSTOM_RTMP = "custom_rtmp"

class ScheduleFrequency(str, enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class StreamSource(Base):
    __tablename__ = "stream_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    source_type = Column(Enum(SourceType))
    path_or_url = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    playlists = relationship("Playlist", back_populates="source")

class StreamOutput(Base):
    __tablename__ = "stream_outputs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    platform = Column(Enum(OutputPlatform))
    stream_key = Column(String(255))
    stream_url = Column(Text, nullable=True)
    rtmp_url = Column(Text, nullable=True)
    metadata = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    streams = relationship("Stream", back_populates="output")

class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    source_id = Column(Integer, ForeignKey("stream_sources.id"))
    loop_enabled = Column(Boolean, default=True)
    shuffle_enabled = Column(Boolean, default=False)
    auto_next = Column(Boolean, default=True)
    items_order = Column(JSON)  # Store order of items
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    source = relationship("StreamSource", back_populates="playlists")
    streams = relationship("Stream", back_populates="playlist")

class Stream(Base):
    __tablename__ = "streams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    output_id = Column(Integer, ForeignKey("stream_outputs.id"))
    status = Column(String(50), default="idle")  # idle, running, paused, stopped, error
    is_live = Column(Boolean, default=False)
    process_id = Column(Integer, nullable=True)
    total_duration = Column(Float, default=0.0)
    current_position = Column(Float, default=0.0)
    bitrate = Column(Integer)
    resolution = Column(String(50))
    fps = Column(Integer)
    audio_bitrate = Column(Integer)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    
    playlist = relationship("Playlist", back_populates="streams")
    output = relationship("StreamOutput", back_populates="streams")
    schedules = relationship("StreamSchedule", back_populates="stream")
    logs = relationship("StreamLog", back_populates="stream")
    monitors = relationship("StreamMonitor", back_populates="stream")

class StreamSchedule(Base):
    __tablename__ = "stream_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"))
    name = Column(String(255))
    frequency = Column(Enum(ScheduleFrequency), default=ScheduleFrequency.ONCE)
    start_time = Column(String(5))  # HH:MM format
    duration_hours = Column(Integer, default=2)
    duration_minutes = Column(Integer, default=0)
    is_enabled = Column(Boolean, default=True)
    auto_restart = Column(Boolean, default=True)
    metadata = Column(JSON)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    stream = relationship("Stream", back_populates="schedules")

class StreamLog(Base):
    __tablename__ = "stream_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"))
    message = Column(Text)
    level = Column(String(20))  # INFO, WARNING, ERROR
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    stream = relationship("Stream", back_populates="logs")

class StreamMonitor(Base):
    __tablename__ = "stream_monitors"
    
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"))
    cpu_usage = Column(Float)
    ram_usage = Column(Float)
    network_speed = Column(Float)
    fps = Column(Float)
    bitrate = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    stream = relationship("Stream", back_populates="monitors")
