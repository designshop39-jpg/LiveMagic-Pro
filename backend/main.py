from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from config import settings
import models
import schemas
from ffmpeg_manager import FFmpegManager
from source_manager import SourceManager
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================== STREAM SOURCES ======================

@app.post("/api/v1/sources", response_model=schemas.StreamSourceResponse)
async def create_stream_source(source: schemas.StreamSourceCreate, db: Session = Depends(get_db)):
    """Create a new stream source"""
    # Validate source
    metadata = {}
    
    try:
        if source.source_type == models.SourceType.LOCAL_VIDEO:
            metadata = SourceManager.parse_local_video(source.path_or_url)
        elif source.source_type == models.SourceType.FOLDER_PLAYLIST:
            metadata = SourceManager.parse_folder_playlist(source.path_or_url)
        elif source.source_type == models.SourceType.IPTV:
            metadata = SourceManager.parse_iptv_m3u(source.path_or_url)
        elif source.source_type == models.SourceType.HTTP_URL:
            metadata = SourceManager.validate_http_url(source.path_or_url)
        elif source.source_type == models.SourceType.RTMP_INPUT:
            metadata = SourceManager.validate_rtmp_input(source.path_or_url)
        elif source.source_type == models.SourceType.HLS_INPUT:
            metadata = SourceManager.validate_hls_input(source.path_or_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    db_source = models.StreamSource(
        name=source.name,
        source_type=source.source_type,
        path_or_url=source.path_or_url,
        metadata=metadata
    )
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@app.get("/api/v1/sources", response_model=list[schemas.StreamSourceResponse])
async def list_stream_sources(db: Session = Depends(get_db)):
    """List all stream sources"""
    return db.query(models.StreamSource).all()

@app.get("/api/v1/sources/{source_id}", response_model=schemas.StreamSourceResponse)
async def get_stream_source(source_id: int, db: Session = Depends(get_db)):
    """Get a specific stream source"""
    source = db.query(models.StreamSource).filter(models.StreamSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

@app.delete("/api/v1/sources/{source_id}")
async def delete_stream_source(source_id: int, db: Session = Depends(get_db)):
    """Delete a stream source"""
    source = db.query(models.StreamSource).filter(models.StreamSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(source)
    db.commit()
    return {"message": "Source deleted successfully"}

# ====================== STREAM OUTPUTS ======================

@app.post("/api/v1/outputs", response_model=schemas.StreamOutputResponse)
async def create_stream_output(output: schemas.StreamOutputCreate, db: Session = Depends(get_db)):
    """Create a new stream output"""
    db_output = models.StreamOutput(
        name=output.name,
        platform=output.platform,
        stream_key=output.stream_key,
        stream_url=output.stream_url,
        rtmp_url=output.rtmp_url,
        metadata=output.metadata
    )
    db.add(db_output)
    db.commit()
    db.refresh(db_output)
    return db_output

@app.get("/api/v1/outputs", response_model=list[schemas.StreamOutputResponse])
async def list_stream_outputs(db: Session = Depends(get_db)):
    """List all stream outputs"""
    return db.query(models.StreamOutput).all()

@app.get("/api/v1/outputs/{output_id}", response_model=schemas.StreamOutputResponse)
async def get_stream_output(output_id: int, db: Session = Depends(get_db)):
    """Get a specific stream output"""
    output = db.query(models.StreamOutput).filter(models.StreamOutput.id == output_id).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")
    return output

@app.delete("/api/v1/outputs/{output_id}")
async def delete_stream_output(output_id: int, db: Session = Depends(get_db)):
    """Delete a stream output"""
    output = db.query(models.StreamOutput).filter(models.StreamOutput.id == output_id).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")
    db.delete(output)
    db.commit()
    return {"message": "Output deleted successfully"}

# ====================== PLAYLISTS ======================

@app.post("/api/v1/playlists", response_model=schemas.PlaylistResponse)
async def create_playlist(playlist: schemas.PlaylistCreate, db: Session = Depends(get_db)):
    """Create a new playlist"""
    db_playlist = models.Playlist(
        name=playlist.name,
        source_id=playlist.source_id,
        loop_enabled=playlist.loop_enabled,
        shuffle_enabled=playlist.shuffle_enabled,
        auto_next=playlist.auto_next
    )
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@app.get("/api/v1/playlists", response_model=list[schemas.PlaylistResponse])
async def list_playlists(db: Session = Depends(get_db)):
    """List all playlists"""
    return db.query(models.Playlist).all()

# ====================== STREAMS ======================

@app.post("/api/v1/streams", response_model=schemas.StreamResponse)
async def create_stream(stream: schemas.StreamCreate, db: Session = Depends(get_db)):
    """Create a new stream"""
    db_stream = models.Stream(
        name=stream.name,
        playlist_id=stream.playlist_id,
        output_id=stream.output_id,
        bitrate=stream.bitrate,
        resolution=stream.resolution,
        fps=stream.fps,
        audio_bitrate=stream.audio_bitrate
    )
    db.add(db_stream)
    db.commit()
    db.refresh(db_stream)
    return db_stream

@app.get("/api/v1/streams", response_model=list[schemas.StreamResponse])
async def list_streams(db: Session = Depends(get_db)):
    """List all streams"""
    return db.query(models.Stream).all()

@app.post("/api/v1/streams/{stream_id}/start")
async def start_stream(stream_id: int, db: Session = Depends(get_db)):
    """Start a stream"""
    stream = db.query(models.Stream).filter(models.Stream.id == stream_id).first()
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    stream.status = "starting"
    db.commit()
    return {"message": "Stream starting", "stream_id": stream_id}

@app.post("/api/v1/streams/{stream_id}/stop")
async def stop_stream(stream_id: int, db: Session = Depends(get_db)):
    """Stop a stream"""
    stream = db.query(models.Stream).filter(models.Stream.id == stream_id).first()
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    stream.status = "stopped"
    db.commit()
    return {"message": "Stream stopped", "stream_id": stream_id}

# ====================== FFmpeg ======================

@app.get("/api/v1/ffmpeg/status")
async def check_ffmpeg_status():
    """Check FFmpeg installation status"""
    try:
        is_installed = FFmpegManager.detect_ffmpeg()
        return {
            "installed": is_installed,
            "path": settings.FFMPEG_PATH if is_installed else None
        }
    except Exception as e:
        return {"installed": False, "error": str(e)}

@app.post("/api/v1/ffmpeg/download")
async def download_ffmpeg():
    """Download FFmpeg (Windows only)"""
    try:
        path = FFmpegManager.download_ffmpeg()
        return {"message": "FFmpeg downloaded successfully", "path": path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ====================== HEALTH CHECK ======================

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
