"""
GUI Module
Main GUI components for the Stundenzettel Scanner application
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import subprocess
import platform
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class StundenzettelGUI:
    """Main GUI for Stundenzettel Scanner application"""
    
    def __init__(self, on_start_callback, on_stop_callback, scan_folder, output_folder):
        """
        Initialize GUI
        
        Args:
            on_start_callback: Function to call when Start button is pressed
            on_stop_callback: Function to call when Stop button is pressed
            scan_folder: Path to scan folder
            output_folder: Path to output folder
        """
        self.on_start_callback = on_start_callback
        self.on_stop_callback = on_stop_callback
        self.scan_folder = scan_folder
        self.output_folder = output_folder
        self.is_running = False
        
        # Create main window
        self.window = tk.Tk()
        self.window.title("📊 Stundenzettel Scanner v1.0")
        self.window.geometry("900x650")
        self.window.configure(bg="#f0f0f0")
        
        # Create GUI components
        self._create_menu()
        self._create_toolbar()
        self._create_log_area()
        self._create_statusbar()
        
        logger.info("GUI initialized")
    
    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.window)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Scan-Ordner öffnen", command=self._open_scan_folder)
        file_menu.add_command(label="Output-Ordner öffnen", command=self._open_output_folder)
        file_menu.add_command(label="Excel öffnen", command=self._open_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self._on_close)
        menubar.add_cascade(label="Datei", menu=file_menu)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Ordner konfigurieren", command=self._configure_folders)
        settings_menu.add_command(label="API-Key ändern", command=self._configure_api_key)
        menubar.add_cascade(label="Einstellungen", menu=settings_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Anleitung", command=self._show_help)
        help_menu.add_command(label="Über", command=self._show_about)
        menubar.add_cascade(label="Hilfe", menu=help_menu)
        
        self.window.config(menu=menubar)
    
    def _create_toolbar(self):
        """Create toolbar with control buttons"""
        toolbar_frame = tk.Frame(self.window, bg="#ffffff", relief=tk.RAISED, bd=2)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Start button
        self.start_button = tk.Button(
            toolbar_frame,
            text="▶ Start",
            command=self._on_start,
            bg="#28a745",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Stop button
        self.stop_button = tk.Button(
            toolbar_frame,
            text="■ Stop",
            command=self._on_stop,
            bg="#dc3545",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Separator
        separator = ttk.Separator(toolbar_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        # Excel button
        excel_button = tk.Button(
            toolbar_frame,
            text="📊 Excel öffnen",
            command=self._open_excel,
            bg="#007bff",
            fg="white",
            font=("Arial", 11),
            padx=15,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        excel_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Folder button
        folder_button = tk.Button(
            toolbar_frame,
            text="📁 Ordner öffnen",
            command=self._open_scan_folder,
            bg="#17a2b8",
            fg="white",
            font=("Arial", 11),
            padx=15,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        folder_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Status label
        self.status_label = tk.Label(
            toolbar_frame,
            text="⚫ Bereit",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#6c757d"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def _create_log_area(self):
        """Create log display area"""
        log_frame = tk.Frame(self.window, bg="#f0f0f0")
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log label
        log_label = tk.Label(
            log_frame,
            text="📋 Live-Log",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            anchor=tk.W
        )
        log_label.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            relief=tk.SUNKEN,
            bd=2
        )
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Configure tags for colored output
        self.log_text.tag_config("success", foreground="#28a745")
        self.log_text.tag_config("error", foreground="#dc3545")
        self.log_text.tag_config("info", foreground="#17a2b8")
        self.log_text.tag_config("warning", foreground="#ffc107")
    
    def _create_statusbar(self):
        """Create status bar"""
        statusbar = tk.Frame(self.window, bg="#343a40", relief=tk.SUNKEN, bd=1)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status text
        self.statusbar_label = tk.Label(
            statusbar,
            text="Bereit | Scan-Ordner: Leer | Verarbeitet: 0",
            font=("Arial", 9),
            bg="#343a40",
            fg="white",
            anchor=tk.W,
            padx=10
        )
        self.statusbar_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _on_start(self):
        """Handle Start button click"""
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="🟢 Aktiv", fg="#28a745")
        self.log_message("System gestartet - Überwachung aktiv", "success")
        
        if self.on_start_callback:
            self.on_start_callback()
    
    def _on_stop(self):
        """Handle Stop button click"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="⚫ Gestoppt", fg="#6c757d")
        self.log_message("System gestoppt", "warning")
        
        if self.on_stop_callback:
            self.on_stop_callback()
    
    def _on_close(self):
        """Handle window close"""
        if self.is_running:
            if messagebox.askyesno("Beenden", "System läuft noch. Wirklich beenden?"):
                self._on_stop()
                self.window.destroy()
        else:
            self.window.destroy()
    
    def _open_scan_folder(self):
        """Open scan folder in file explorer"""
        self._open_folder(self.scan_folder)
    
    def _open_output_folder(self):
        """Open output folder in file explorer"""
        self._open_folder(self.output_folder)
    
    def _open_folder(self, folder_path):
        """Open folder in system file explorer"""
        try:
            folder_path = Path(folder_path)
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
            
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(folder_path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(folder_path)])
            
            self.log_message(f"Ordner geöffnet: {folder_path}", "info")
        except Exception as e:
            self.log_message(f"Fehler beim Öffnen des Ordners: {e}", "error")
    
    def _open_excel(self):
        """Open latest Excel file"""
        try:
            output_path = Path(self.output_folder)
            excel_files = list(output_path.glob("stundenzettel_export_*.xlsx"))
            
            if not excel_files:
                messagebox.showwarning("Keine Datei", "Noch keine Excel-Datei erstellt.")
                return
            
            # Get latest file
            latest_file = max(excel_files, key=lambda x: x.stat().st_mtime)
            
            if platform.system() == "Windows":
                os.startfile(latest_file)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(latest_file)])
            else:  # Linux
                subprocess.run(["xdg-open", str(latest_file)])
            
            self.log_message(f"Excel geöffnet: {latest_file.name}", "success")
        except Exception as e:
            self.log_message(f"Fehler beim Öffnen von Excel: {e}", "error")
    
    def _configure_folders(self):
        """Configure folder paths"""
        messagebox.showinfo("Hinweis", "Ordner werden in der .env Datei konfiguriert.")
    
    def _configure_api_key(self):
        """Configure API key"""
        messagebox.showinfo("Hinweis", "API-Key wird in der .env Datei konfiguriert.")
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """
STUNDENZETTEL SCANNER - Hilfe

1. SCANNEN:
   - Legen Sie gescannte Stundenzettel in den 'scans' Ordner
   - Unterstützte Formate: JPG, PNG, PDF

2. STARTEN:
   - Klicken Sie auf 'Start' Button
   - System überwacht automatisch den Ordner

3. VERARBEITUNG:
   - Erfolgreiche Dateien: Grün ✓
   - Fehlerhafte Dateien: Rot ✗

4. EXCEL:
   - Klicken Sie auf 'Excel öffnen'
   - Oder öffnen Sie die Datei im 'output' Ordner

Weitere Informationen: README.md
        """
        messagebox.showinfo("Hilfe", help_text)
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """
Stundenzettel Scanner v1.0

Automatisiertes System zur Digitalisierung
von gescannten Stundenzetteln.

© 2024 - Mit Google Gemini AI
        """
        messagebox.showinfo("Über", about_text)
    
    def log_message(self, message, level="info"):
        """
        Add message to log display
        
        Args:
            message: Message text
            level: Log level (info, success, error, warning)
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add message with timestamp
        self.log_text.insert(tk.END, f"[{timestamp}] ", "info")
        self.log_text.insert(tk.END, f"{message}\n", level)
        self.log_text.see(tk.END)
        
        # Update display
        self.window.update_idletasks()
    
    def update_statusbar(self, message):
        """Update status bar text"""
        self.statusbar_label.config(text=message)
        self.window.update_idletasks()
    
    def run(self):
        """Start the GUI main loop"""
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self.window.mainloop()
