"""
Stundenzettel Scanner - Main Application
Automated timesheet digitization system with GUI
"""

import os
import sys
import logging
import threading
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import modules
from modules.ocr_processor import OCRProcessor
from modules.time_calculator import TimeCalculator
from modules.excel_exporter import ExcelExporter
from modules.file_handler import FileHandler
from modules.gui import StundenzettelGUI


class TimesheetHandler(FileSystemEventHandler):
    """File system event handler for automatic file processing"""
    
    def __init__(self, processor):
        self.processor = processor
        super().__init__()
    
    def on_created(self, event):
        """Handle new file creation"""
        if not event.is_directory and FileHandler.is_supported_file(event.src_path):
            # Wait a bit to ensure file is fully written
            time.sleep(1)
            self.processor.process_file(event.src_path)


class StundenzettelScanner:
    """Main application class"""
    
    def __init__(self):
        """Initialize the scanner application"""
        self._setup_logging()
        self._load_config()
        self._initialize_components()
        self.observer = None
        self.is_running = False
        
        logger.info("="*60)
        logger.info("Stundenzettel Scanner initialized")
        logger.info("="*60)
    
    def _setup_logging(self):
        """Configure logging system"""
        # Create logs directory
        log_dir = Path(".")
        
        # Configure root logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'process.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        global logger
        logger = logging.getLogger(__name__)
    
    def _load_config(self):
        """Load configuration from .env file"""
        # Load .env file
        env_path = Path('.env')
        
        if not env_path.exists():
            logger.error("="*60)
            logger.error("FEHLER: .env Datei nicht gefunden!")
            logger.error("="*60)
            logger.error("Bitte erstellen Sie eine .env Datei:")
            logger.error("1. Kopieren Sie .env.example zu .env")
            logger.error("2. Tragen Sie Ihren Gemini API-Key ein")
            logger.error("3. Erstellen Sie einen API-Key unter:")
            logger.error("   https://aistudio.google.com/app/apikey")
            logger.error("="*60)
            raise FileNotFoundError(".env Datei nicht gefunden. Siehe .env.example für Template.")
        
        load_dotenv()
        
        # Load configuration
        self.config = {
            'api_key': os.getenv('GEMINI_API_KEY'),
            'scan_folder': os.getenv('SCAN_FOLDER', './scans'),
            'output_folder': os.getenv('OUTPUT_FOLDER', './output'),
            'archive_folder': os.getenv('ARCHIVE_FOLDER', './archive'),
            'error_folder': os.getenv('ERROR_FOLDER', './errors'),
            'watch_mode': os.getenv('WATCH_MODE', 'true').lower() == 'true',
            'log_level': os.getenv('LOG_LEVEL', 'INFO')
        }
        
        # Validate API key
        if not self.config['api_key'] or self.config['api_key'] == 'your_api_key_here':
            logger.error("="*60)
            logger.error("FEHLER: Kein gültiger API-Key konfiguriert!")
            logger.error("="*60)
            logger.error("Bitte tragen Sie einen gültigen Gemini API-Key in die .env Datei ein.")
            logger.error("Erstellen Sie einen Key unter:")
            logger.error("https://aistudio.google.com/app/apikey")
            logger.error("="*60)
            raise ValueError("Kein gültiger API-Key konfiguriert")
        
        logger.info("Konfiguration geladen:")
        logger.info(f"  Scan-Ordner: {self.config['scan_folder']}")
        logger.info(f"  Output-Ordner: {self.config['output_folder']}")
        logger.info(f"  Überwachungsmodus: {self.config['watch_mode']}")
    
    def _initialize_components(self):
        """Initialize all components"""
        try:
            # Initialize OCR processor
            self.ocr_processor = OCRProcessor(self.config['api_key'])
            
            # Initialize file handler
            self.file_handler = FileHandler(
                self.config['archive_folder'],
                self.config['error_folder']
            )
            
            # Initialize Excel exporter
            self.excel_exporter = ExcelExporter(self.config['output_folder'])
            
            # Initialize GUI
            self.gui = StundenzettelGUI(
                on_start_callback=self.start_monitoring,
                on_stop_callback=self.stop_monitoring,
                scan_folder=self.config['scan_folder'],
                output_folder=self.config['output_folder']
            )
            
            # Redirect logging to GUI
            self._setup_gui_logging()
            
            logger.info("Alle Komponenten initialisiert")
            
        except Exception as e:
            logger.error(f"Fehler bei der Initialisierung: {e}")
            raise
    
    def _setup_gui_logging(self):
        """Setup logging to GUI"""
        class GUIHandler(logging.Handler):
            def __init__(self, gui):
                super().__init__()
                self.gui = gui
            
            def emit(self, record):
                msg = self.format(record)
                level_map = {
                    'ERROR': 'error',
                    'WARNING': 'warning',
                    'INFO': 'info',
                    'DEBUG': 'info'
                }
                level = level_map.get(record.levelname, 'info')
                
                # Remove timestamp from message (GUI adds its own)
                if ' - ' in msg:
                    parts = msg.split(' - ', 3)
                    if len(parts) >= 4:
                        msg = parts[3]
                
                try:
                    self.gui.log_message(msg, level)
                except:
                    pass
        
        gui_handler = GUIHandler(self.gui)
        gui_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(gui_handler)
    
    def process_file(self, filepath):
        """
        Process a single timesheet file
        
        Args:
            filepath: Path to file to process
        """
        try:
            filepath = Path(filepath)
            logger.info(f"Verarbeite Datei: {filepath.name}")
            
            # Extract data using OCR
            if filepath.suffix.lower() == '.pdf':
                data = self.ocr_processor.process_pdf(filepath)
            else:
                data = self.ocr_processor.process_image(filepath)
            
            if not data:
                logger.error(f"Keine Daten extrahiert aus {filepath.name}")
                self.file_handler.move_to_error(filepath, "OCR extraction failed")
                return False
            
            # Calculate net hours
            net_hours = TimeCalculator.calculate_net_hours(
                data['startzeit'],
                data['endzeit'],
                data['pause_minuten']
            )
            
            # Add to Excel export data
            export_data = {
                'name': data['name'],
                'datum': data['datum'],
                'startzeit': data['startzeit'],
                'endzeit': data['endzeit'],
                'pause_minuten': data['pause_minuten'],
                'netto_stunden': net_hours
            }
            
            self.excel_exporter.add_entry(export_data)
            
            # Export to Excel (will update existing file or create new one)
            excel_path = self.excel_exporter.export()
            
            if excel_path:
                logger.info(f"✓ Erfolgreich verarbeitet: {filepath.name}")
                logger.info(f"  → {data['name']}, {data['datum']}, {net_hours}h")
                
                # Archive the file
                self.file_handler.archive_file(filepath)
                
                return True
            else:
                logger.error(f"Excel-Export fehlgeschlagen für {filepath.name}")
                self.file_handler.move_to_error(filepath, "Excel export failed")
                return False
                
        except Exception as e:
            logger.error(f"Fehler bei Verarbeitung von {filepath}: {e}")
            self.file_handler.move_to_error(filepath, str(e))
            return False
    
    def process_existing_files(self):
        """Process all existing files in scan folder"""
        scan_folder = Path(self.config['scan_folder'])
        files = self.file_handler.get_scan_files(scan_folder)
        
        if not files:
            logger.info("Keine Dateien zum Verarbeiten gefunden")
            return
        
        logger.info(f"Verarbeite {len(files)} Datei(en)...")
        
        success_count = 0
        for filepath in files:
            if self.process_file(filepath):
                success_count += 1
        
        logger.info(f"Verarbeitung abgeschlossen: {success_count}/{len(files)} erfolgreich")
        self.gui.update_statusbar(f"Verarbeitet: {success_count}/{len(files)} | Bereit")
    
    def start_monitoring(self):
        """Start file system monitoring"""
        if self.is_running:
            logger.warning("Überwachung läuft bereits")
            return
        
        self.is_running = True
        
        # First, process existing files
        threading.Thread(target=self.process_existing_files, daemon=True).start()
        
        if self.config['watch_mode']:
            # Start watchdog observer
            event_handler = TimesheetHandler(self)
            self.observer = Observer()
            self.observer.schedule(
                event_handler,
                self.config['scan_folder'],
                recursive=False
            )
            self.observer.start()
            logger.info("Dateiüberwachung gestartet")
        else:
            logger.info("Einmalige Verarbeitung (Watch-Modus deaktiviert)")
    
    def stop_monitoring(self):
        """Stop file system monitoring"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            logger.info("Dateiüberwachung gestoppt")
    
    def run(self):
        """Run the application"""
        try:
            logger.info("Starte GUI...")
            self.gui.run()
        except KeyboardInterrupt:
            logger.info("Programm durch Benutzer beendet")
        finally:
            self.stop_monitoring()
            logger.info("Programm beendet")


def main():
    """Main entry point"""
    try:
        app = StundenzettelScanner()
        app.run()
    except Exception as e:
        logging.error(f"Kritischer Fehler: {e}")
        import traceback
        traceback.print_exc()
        input("Drücken Sie Enter zum Beenden...")
        sys.exit(1)


if __name__ == "__main__":
    main()
