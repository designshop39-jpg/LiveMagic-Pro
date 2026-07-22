import os
import shutil
import logging
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)

class FileManager:
    """Manage file operations for uploads and storage"""
    
    @staticmethod
    def upload_file(file_path: str, destination_folder: str = "uploads"):
        """Move uploaded file to destination"""
        try:
            dest_dir = settings.UPLOAD_DIR / destination_folder
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            src_path = Path(file_path)
            dest_path = dest_dir / src_path.name
            
            shutil.move(str(src_path), str(dest_path))
            logger.info(f"File uploaded: {dest_path}")
            return str(dest_path)
            
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise
    
    @staticmethod
    def delete_file(file_path: str):
        """Delete a file"""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
        
        return False
    
    @staticmethod
    def rename_file(old_path: str, new_name: str):
        """Rename a file"""
        try:
            old = Path(old_path)
            new = old.parent / new_name
            old.rename(new)
            logger.info(f"File renamed: {old_path} -> {new}")
            return str(new)
        except Exception as e:
            logger.error(f"Error renaming file: {e}")
        
        return None
    
    @staticmethod
    def list_files(folder_path: str = "uploads"):
        """List all files in a folder"""
        try:
            folder = settings.UPLOAD_DIR / folder_path
            if not folder.exists():
                return []
            
            files = []
            for item in folder.iterdir():
                if item.is_file():
                    files.append({
                        "name": item.name,
                        "path": str(item),
                        "size": item.stat().st_size,
                        "created": item.stat().st_ctime
                    })
            
            return sorted(files, key=lambda x: x['created'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    @staticmethod
    def search_files(pattern: str, folder_path: str = "uploads"):
        """Search files by pattern"""
        try:
            from pathlib import Path
            folder = settings.UPLOAD_DIR / folder_path
            
            if not folder.exists():
                return []
            
            results = []
            for item in folder.rglob(f"*{pattern}*"):
                if item.is_file():
                    results.append({
                        "name": item.name,
                        "path": str(item),
                        "size": item.stat().st_size
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []
    
    @staticmethod
    def create_folder(folder_name: str, parent_folder: str = "uploads"):
        """Create a new folder"""
        try:
            parent = settings.UPLOAD_DIR / parent_folder
            new_folder = parent / folder_name
            new_folder.mkdir(parents=True, exist_ok=True)
            logger.info(f"Folder created: {new_folder}")
            return str(new_folder)
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
        
        return None
    
    @staticmethod
    def get_folder_size(folder_path: str = "uploads"):
        """Get total size of folder in MB"""
        try:
            folder = settings.UPLOAD_DIR / folder_path
            total_size = sum(f.stat().st_size for f in folder.rglob('*') if f.is_file())
            return round(total_size / (1024**2), 2)  # Convert to MB
        except Exception as e:
            logger.error(f"Error getting folder size: {e}")
        
        return 0
