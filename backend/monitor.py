import psutil
import logging
import threading
from datetime import datetime
from database import SessionLocal
import models
from config import settings

logger = logging.getLogger(__name__)

class StreamMonitor:
    """Monitor system resources and stream statistics"""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self, stream_id: int, interval: int = 5):
        """Start monitoring a stream"""
        try:
            db = SessionLocal()
            stream = db.query(models.Stream).filter(models.Stream.id == stream_id).first()
            
            if not stream:
                logger.error(f"Stream {stream_id} not found")
                return False
            
            db.close()
            
            self.monitoring = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                args=(stream_id, interval),
                daemon=True
            )
            self.monitor_thread.start()
            logger.info(f"Started monitoring stream {stream_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting monitoring: {e}")
            return False
    
    def _monitor_loop(self, stream_id: int, interval: int):
        """Main monitoring loop"""
        import time
        
        while self.monitoring:
            try:
                # Get system stats
                cpu_usage = psutil.cpu_percent(interval=1)
                ram_usage = psutil.virtual_memory().percent
                
                # Get network stats (approximation)
                net_io = psutil.net_io_counters()
                network_speed = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)  # MB
                
                # Get process-specific info
                db = SessionLocal()
                stream = db.query(models.Stream).filter(models.Stream.id == stream_id).first()
                
                if not stream or not stream.process_id:
                    db.close()
                    break
                
                try:
                    process = psutil.Process(stream.process_id)
                    process_cpu = process.cpu_percent(interval=0.1)
                    process_ram = process.memory_percent()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    process_cpu = 0
                    process_ram = 0
                
                # Calculate bitrate and FPS (placeholder)
                bitrate = stream.bitrate
                fps = stream.fps
                
                # Store monitoring data
                monitor_entry = models.StreamMonitor(
                    stream_id=stream_id,
                    cpu_usage=process_cpu,
                    ram_usage=process_ram,
                    network_speed=network_speed,
                    fps=float(fps),
                    bitrate=float(bitrate)
                )
                db.add(monitor_entry)
                db.commit()
                db.close()
                
                logger.debug(f"Stream {stream_id} - CPU: {process_cpu}%, RAM: {process_ram}%, Bitrate: {bitrate}kbps, FPS: {fps}")
                
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Monitoring stopped")
    
    @staticmethod
    def get_stream_stats(stream_id: int, hours: int = 1):
        """Get stream statistics for the last N hours"""
        try:
            from datetime import datetime, timedelta
            
            db = SessionLocal()
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            stats = db.query(models.StreamMonitor).filter(
                models.StreamMonitor.stream_id == stream_id,
                models.StreamMonitor.timestamp >= cutoff_time
            ).all()
            db.close()
            
            if not stats:
                return None
            
            avg_cpu = sum(s.cpu_usage for s in stats) / len(stats)
            avg_ram = sum(s.ram_usage for s in stats) / len(stats)
            avg_bitrate = sum(s.bitrate for s in stats) / len(stats)
            avg_fps = sum(s.fps for s in stats) / len(stats)
            avg_network = sum(s.network_speed for s in stats) / len(stats)
            
            return {
                "stream_id": stream_id,
                "period_hours": hours,
                "cpu_usage_avg": round(avg_cpu, 2),
                "ram_usage_avg": round(avg_ram, 2),
                "bitrate_avg": round(avg_bitrate, 2),
                "fps_avg": round(avg_fps, 2),
                "network_speed_avg": round(avg_network, 2),
                "samples": len(stats)
            }
            
        except Exception as e:
            logger.error(f"Error getting stream stats: {e}")
            return None
    
    @staticmethod
    def get_system_stats():
        """Get overall system statistics"""
        try:
            return {
                "cpu_usage": psutil.cpu_percent(interval=1),
                "cpu_count": psutil.cpu_count(),
                "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "ram_usage_percent": psutil.virtual_memory().percent,
                "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
                "disk_free_gb": round(psutil.disk_usage('/').free / (1024**3), 2),
                "disk_usage_percent": psutil.disk_usage('/').percent,
                "network_sent_mb": round(psutil.net_io_counters().bytes_sent / (1024**2), 2),
                "network_recv_mb": round(psutil.net_io_counters().bytes_recv / (1024**2), 2),
                "uptime_seconds": int(datetime.utcnow().timestamp() - psutil.boot_time())
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {}
