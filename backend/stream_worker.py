import subprocess
import threading
import logging
from datetime import datetime
from pathlib import Path
from config import settings
from ffmpeg_manager import FFmpegManager
from database import SessionLocal
import models

logger = logging.getLogger(__name__)

class StreamWorker:
    """Handle individual stream processing and FFmpeg execution"""
    
    def __init__(self, stream_id: int):
        self.stream_id = stream_id
        self.process = None
        self.is_running = False
        self.monitoring_thread = None
    
    def start_stream(self, playlist_path: str, output_url: str, bitrate: int = 3000,
                    resolution: str = "1280x720", fps: int = 30, audio_bitrate: int = 192):
        """Start streaming with FFmpeg"""
        try:
            db = SessionLocal()
            stream = db.query(models.Stream).filter(models.Stream.id == self.stream_id).first()
            
            if not stream:
                logger.error(f"Stream {self.stream_id} not found")
                return False
            
            # Build FFmpeg command
            cmd = FFmpegManager.build_ffmpeg_command(
                playlist_file=playlist_path,
                output_url=output_url,
                bitrate=bitrate,
                resolution=resolution,
                fps=fps,
                audio_bitrate=audio_bitrate
            )
            
            logger.info(f"Starting stream {self.stream_id} with command: {' '.join(cmd)}")
            
            # Start FFmpeg process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            self.is_running = True
            stream.status = "running"
            stream.is_live = True
            stream.process_id = self.process.pid
            stream.started_at = datetime.utcnow()
            db.commit()
            db.close()
            
            # Start monitoring thread
            self.monitoring_thread = threading.Thread(
                target=self._monitor_process,
                daemon=True
            )
            self.monitoring_thread.start()
            
            logger.info(f"Stream {self.stream_id} started with PID {self.process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting stream {self.stream_id}: {e}")
            self._update_stream_status("error", str(e))
            return False
    
    def stop_stream(self):
        """Stop streaming"""
        try:
            if self.process and self.is_running:
                logger.info(f"Stopping stream {self.stream_id}")
                self.process.terminate()
                self.process.wait(timeout=10)
                self.is_running = False
                
                db = SessionLocal()
                stream = db.query(models.Stream).filter(models.Stream.id == self.stream_id).first()
                if stream:
                    stream.status = "stopped"
                    stream.is_live = False
                    stream.ended_at = datetime.utcnow()
                    db.commit()
                db.close()
                
                return True
        except Exception as e:
            logger.error(f"Error stopping stream {self.stream_id}: {e}")
            if self.process:
                self.process.kill()
        
        return False
    
    def _monitor_process(self):
        """Monitor FFmpeg process and capture logs"""
        try:
            while self.is_running and self.process:
                line = self.process.stderr.readline()
                if line:
                    self._log_stream_message(line.strip())
                
                if self.process.poll() is not None:
                    self.is_running = False
                    self._update_stream_status("stopped")
                    break
        except Exception as e:
            logger.error(f"Error monitoring stream {self.stream_id}: {e}")
    
    def _log_stream_message(self, message: str):
        """Log stream message to database"""
        try:
            db = SessionLocal()
            
            level = "INFO"
            if "error" in message.lower():
                level = "ERROR"
            elif "warning" in message.lower():
                level = "WARNING"
            
            log_entry = models.StreamLog(
                stream_id=self.stream_id,
                message=message,
                level=level
            )
            db.add(log_entry)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Error logging message: {e}")
    
    def _update_stream_status(self, status: str, error_msg: str = None):
        """Update stream status in database"""
        try:
            db = SessionLocal()
            stream = db.query(models.Stream).filter(models.Stream.id == self.stream_id).first()
            if stream:
                stream.status = status
                stream.is_live = (status == "running")
                if error_msg:
                    log_entry = models.StreamLog(
                        stream_id=self.stream_id,
                        message=error_msg,
                        level="ERROR"
                    )
                    db.add(log_entry)
                db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Error updating stream status: {e}")
