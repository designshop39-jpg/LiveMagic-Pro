import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from database import SessionLocal
import models
from stream_worker import StreamWorker
from source_manager import SourceManager

logger = logging.getLogger(__name__)

class StreamScheduler:
    """Manage scheduled streaming tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.stream_workers = {}  # stream_id -> StreamWorker
        self.scheduler.start()
        logger.info("Stream Scheduler started")
    
    def schedule_stream(self, schedule_id: int):
        """Schedule a stream based on schedule settings"""
        try:
            db = SessionLocal()
            schedule = db.query(models.StreamSchedule).filter(
                models.StreamSchedule.id == schedule_id
            ).first()
            
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return False
            
            stream = db.query(models.Stream).filter(
                models.Stream.id == schedule.stream_id
            ).first()
            
            if not stream:
                logger.error(f"Stream {schedule.stream_id} not found")
                return False
            
            job_id = f"stream_{schedule.stream_id}_{schedule.id}"
            
            if schedule.frequency == models.ScheduleFrequency.ONCE:
                trigger = CronTrigger.from_crontab(f"{schedule.start_time.split(':')[1]} {schedule.start_time.split(':')[0]} * * *")
            elif schedule.frequency == models.ScheduleFrequency.DAILY:
                trigger = CronTrigger.from_crontab(f"{schedule.start_time.split(':')[1]} {schedule.start_time.split(':')[0]} * * *")
            elif schedule.frequency == models.ScheduleFrequency.WEEKLY:
                trigger = CronTrigger.from_crontab(f"{schedule.start_time.split(':')[1]} {schedule.start_time.split(':')[0]} * * 0")  # Sunday
            elif schedule.frequency == models.ScheduleFrequency.MONTHLY:
                trigger = CronTrigger.from_crontab(f"{schedule.start_time.split(':')[1]} {schedule.start_time.split(':')[0]} 1 * *")
            
            self.scheduler.add_job(
                self._start_stream_job,
                trigger=trigger,
                id=job_id,
                args=[stream.id, schedule.duration_hours, schedule.duration_minutes, schedule.auto_restart],
                replace_existing=True
            )
            
            schedule.next_run = self.scheduler.get_job(job_id).next_run_time
            db.commit()
            db.close()
            
            logger.info(f"Stream {stream.id} scheduled with frequency {schedule.frequency}")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling stream: {e}")
            return False
    
    def _start_stream_job(self, stream_id: int, duration_hours: int, duration_minutes: int, auto_restart: bool):
        """Job to start a stream"""
        try:
            db = SessionLocal()
            stream = db.query(models.Stream).filter(models.Stream.id == stream_id).first()
            
            if not stream:
                logger.error(f"Stream {stream_id} not found")
                return
            
            playlist = stream.playlist
            output = stream.output
            
            if not playlist or not output:
                logger.error(f"Playlist or output not found for stream {stream_id}")
                return
            
            # Create worker and start stream
            worker = StreamWorker(stream_id)
            self.stream_workers[stream_id] = worker
            
            # Get playlist files
            source = playlist.source
            playlist_files = source.metadata.get('videos', [])
            
            if not playlist_files:
                logger.error(f"No videos in playlist for stream {stream_id}")
                return
            
            # Create concat file
            concat_file = f"/tmp/playlist_{stream_id}.txt"
            video_paths = [v['path'] for v in playlist_files]
            SourceManager.write_concat_file(video_paths, concat_file)
            
            # Build output URL
            if output.platform == models.OutputPlatform.YOUTUBE:
                output_url = f"rtmp://a.rtmp.youtube.com/live2/{output.stream_key}"
            elif output.platform == models.OutputPlatform.TWITCH:
                output_url = f"rtmp://live-{output.metadata.get('region', 'ams')}.twitch.tv/live/{output.stream_key}"
            elif output.platform == models.OutputPlatform.FACEBOOK:
                output_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{output.stream_key}"
            elif output.platform == models.OutputPlatform.CUSTOM_RTMP:
                output_url = output.rtmp_url
            
            # Start stream
            worker.start_stream(
                playlist_path=concat_file,
                output_url=output_url,
                bitrate=stream.bitrate,
                resolution=stream.resolution,
                fps=stream.fps,
                audio_bitrate=stream.audio_bitrate
            )
            
            # Schedule stop if duration is specified
            stop_duration = (duration_hours * 60) + duration_minutes
            if stop_duration > 0:
                self.scheduler.add_job(
                    self._stop_stream_job,
                    trigger='date',
                    run_date=datetime.now() + timedelta(minutes=stop_duration),
                    id=f"stop_stream_{stream_id}",
                    args=[stream_id, auto_restart]
                )
            
            stream.status = "running"
            stream.is_live = True
            db.commit()
            db.close()
            
        except Exception as e:
            logger.error(f"Error in start stream job: {e}")
    
    def _stop_stream_job(self, stream_id: int, auto_restart: bool):
        """Job to stop a stream"""
        try:
            if stream_id in self.stream_workers:
                worker = self.stream_workers[stream_id]
                worker.stop_stream()
            
            if auto_restart:
                # Restart the stream
                logger.info(f"Auto-restarting stream {stream_id}")
                self._start_stream_job(stream_id, 2, 0, auto_restart)
        
        except Exception as e:
            logger.error(f"Error in stop stream job: {e}")
    
    def cancel_stream(self, stream_id: int):
        """Cancel scheduled stream"""
        try:
            job_id = f"stream_{stream_id}"
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                logger.info(f"Stream {stream_id} schedule cancelled")
                return True
        except Exception as e:
            logger.error(f"Error cancelling stream: {e}")
        
        return False
    
    def shutdown(self):
        """Shutdown scheduler"""
        try:
            # Stop all running streams
            for worker in self.stream_workers.values():
                worker.stop_stream()
            
            self.scheduler.shutdown()
            logger.info("Stream Scheduler shutdown")
        except Exception as e:
            logger.error(f"Error shutting down scheduler: {e}")
