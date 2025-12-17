"""
File Handler Module
Handles file operations (move, archive, error handling)
"""

import os
import shutil
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class FileHandler:
    """Manages file operations for the timesheet scanner"""
    
    def __init__(self, archive_folder, error_folder):
        """Initialize file handler with archive and error folders"""
        self.archive_folder = Path(archive_folder)
        self.error_folder = Path(error_folder)
        
        # Create folders if they don't exist
        self.archive_folder.mkdir(parents=True, exist_ok=True)
        self.error_folder.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"File Handler initialized - Archive: {archive_folder}, Error: {error_folder}")
    
    def archive_file(self, filepath):
        """
        Move successfully processed file to archive folder with timestamp
        
        Args:
            filepath: Path to file to archive
            
        Returns:
            str: New file path or None if failed
        """
        try:
            filepath = Path(filepath)
            
            if not filepath.exists():
                logger.error(f"File not found: {filepath}")
                return None
            
            # Generate new filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_{filepath.name}"
            new_path = self.archive_folder / new_filename
            
            # Move file
            shutil.move(str(filepath), str(new_path))
            logger.info(f"Archived: {filepath.name} → {new_path}")
            
            return str(new_path)
            
        except Exception as e:
            logger.error(f"Error archiving file {filepath}: {e}")
            return None
    
    def move_to_error(self, filepath, error_message=""):
        """
        Move failed file to error folder
        
        Args:
            filepath: Path to file to move
            error_message: Optional error description
            
        Returns:
            str: New file path or None if failed
        """
        try:
            filepath = Path(filepath)
            
            if not filepath.exists():
                logger.error(f"File not found: {filepath}")
                return None
            
            # Generate new filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_ERROR_{filepath.name}"
            new_path = self.error_folder / new_filename
            
            # Move file
            shutil.move(str(filepath), str(new_path))
            logger.error(f"Moved to errors: {filepath.name} → {new_path}")
            
            # Write error log
            if error_message:
                self._write_error_log(new_path, error_message)
            
            return str(new_path)
            
        except Exception as e:
            logger.error(f"Error moving file to error folder {filepath}: {e}")
            return None
    
    def _write_error_log(self, filepath, error_message):
        """Write error details to log file"""
        try:
            log_path = self.error_folder / "errors.log"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"File: {Path(filepath).name}\n")
                f.write(f"Error: {error_message}\n")
                f.write(f"{'='*60}\n")
            
            logger.debug(f"Error logged to {log_path}")
            
        except Exception as e:
            logger.error(f"Failed to write error log: {e}")
    
    @staticmethod
    def is_supported_file(filepath):
        """
        Check if file is a supported format
        
        Args:
            filepath: Path to check
            
        Returns:
            bool: True if supported format
        """
        supported_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
        ext = Path(filepath).suffix.lower()
        return ext in supported_extensions
    
    @staticmethod
    def get_scan_files(scan_folder):
        """
        Get all supported scan files from folder
        
        Args:
            scan_folder: Folder to scan
            
        Returns:
            list: List of file paths
        """
        scan_folder = Path(scan_folder)
        
        if not scan_folder.exists():
            logger.warning(f"Scan folder not found: {scan_folder}")
            return []
        
        files = []
        for ext in ['.jpg', '.jpeg', '.png', '.pdf']:
            files.extend(scan_folder.glob(f"*{ext}"))
            files.extend(scan_folder.glob(f"*{ext.upper()}"))
        
        logger.debug(f"Found {len(files)} scan files in {scan_folder}")
        return [str(f) for f in files]
