from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from models import SourceType, OutputPlatform, ScheduleFrequency

# Stream Source Schemas
class StreamSourceBase(BaseModel):
    name: str
    source_type: SourceType
    path_or_url: str
    metadata: Optional[Dict[str, Any]] = {}

class StreamSourceCreate(StreamSourceBase):
    pass

class StreamSourceUpdate(BaseModel):
    name: Optional[str] = None
    path_or_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class StreamSourceResponse(StreamSourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Stream Output Schemas
class StreamOutputBase(BaseModel):
    name: str
    platform: OutputPlatform
    stream_key: str
    stream_url: Optional[str] = None
    rtmp_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class StreamOutputCreate(StreamOutputBase):
    pass

class StreamOutputUpdate(BaseModel):
    name: Optional[str] = None
    stream_key: Optional[str] = None
    is_active: Optional[bool] = None

class StreamOutputResponse(StreamOutputBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Playlist Schemas
class PlaylistBase(BaseModel):
    name: str
    source_id: int
    loop_enabled: bool = True
    shuffle_enabled: bool = False
    auto_next: bool = True

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    loop_enabled: Optional[bool] = None
    shuffle_enabled: Optional[bool] = None
    auto_next: Optional[bool] = None

class PlaylistResponse(PlaylistBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Stream Schemas
class StreamBase(BaseModel):
    name: str
    playlist_id: int
    output_id: int
    bitrate: int = 3000
    resolution: str = "1280x720"
    fps: int = 30
    audio_bitrate: int = 192

class StreamCreate(StreamBase):
    pass

class StreamUpdate(BaseModel):
    name: Optional[str] = None
    bitrate: Optional[int] = None
    resolution: Optional[str] = None
    fps: Optional[int] = None

class StreamResponse(StreamBase):
    id: int
    status: str
    is_live: bool
    total_duration: float
    current_position: float
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Stream Schedule Schemas
class StreamScheduleBase(BaseModel):
    stream_id: int
    name: str
    frequency: ScheduleFrequency = ScheduleFrequency.ONCE
    start_time: str  # HH:MM
    duration_hours: int = 2
    duration_minutes: int = 0
    auto_restart: bool = True

class StreamScheduleCreate(StreamScheduleBase):
    pass

class StreamScheduleUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[ScheduleFrequency] = None
    start_time: Optional[str] = None
    is_enabled: Optional[bool] = None

class StreamScheduleResponse(StreamScheduleBase):
    id: int
    is_enabled: bool
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Stream Log Schemas
class StreamLogResponse(BaseModel):
    id: int
    stream_id: int
    message: str
    level: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Stream Monitor Schemas
class StreamMonitorResponse(BaseModel):
    id: int
    stream_id: int
    cpu_usage: float
    ram_usage: float
    network_speed: float
    fps: float
    bitrate: float
    timestamp: datetime
    
    class Config:
        from_attributes = True
