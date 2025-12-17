# 📊 Stundenzettel-Automatisierung

Vollautomatisiertes Python-System zur Digitalisierung von gescannten Stundenzetteln und Servicescheinen mit professioneller GUI für Kundenpräsentationen.

## ✨ Hauptfunktionen

- 🖥️ **Moderne GUI** mit tkinter - intuitive Bedienung
- 🔍 **Intelligente OCR** mit Google Gemini 2.0 Flash AI
- 📊 **Automatischer Excel-Export** mit professioneller Formatierung
- 📁 **Automatische Dateiüberwachung** mit Watchdog
- ⚙️ **Intelligente Pausenberechnung** (nur Pausen > 30 Min werden abgezogen)
- 🗃️ **Automatische Archivierung** erfolgreich verarbeiteter Dateien
- ❌ **Fehlerbehandlung** mit detailliertem Logging

## 🎯 Unterstützte Formate

- JPG / JPEG
- PNG
- PDF (erste Seite wird verarbeitet)

## 📋 Voraussetzungen

- Python 3.10 oder höher
- Google Gemini API-Key (kostenlos erhältlich)
- Windows 10/11, macOS oder Linux

## 🚀 Installation

### 1. Repository klonen

```bash
git clone https://github.com/phil061191/Stundenzettel-Automatisierung.git
cd Stundenzettel-Automatisierung
```

### 2. Python-Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. API-Key konfigurieren

#### 3.1 Google Gemini API-Key erstellen

1. Besuche: https://aistudio.google.com/app/apikey
2. Melde dich mit deinem Google-Konto an
3. Klicke auf "Create API Key"
4. Kopiere den generierten Key

#### 3.2 .env Datei erstellen

```bash
# Kopiere die Beispiel-Datei
cp .env.example .env
```

Öffne `.env` mit einem Texteditor und trage deinen API-Key ein:

```env
GEMINI_API_KEY=dein_api_key_hier
```

**⚠️ WICHTIG:** Teile deinen API-Key niemals mit anderen! Die `.env` Datei ist in `.gitignore` und wird NICHT ins Repository hochgeladen.

### 4. Programm starten

```bash
python main.py
```

## 📖 Bedienung

### Schnellstart

1. **Start** - Klicke auf den grünen "Start" Button
2. **Scannen** - Lege Stundenzettel in den `scans/` Ordner
3. **Automatisch** - Dateien werden automatisch verarbeitet
4. **Excel öffnen** - Klicke auf "Excel öffnen" Button

### Detaillierte Anleitung

#### 1. GUI-Übersicht

- **▶ Start**: Startet die automatische Überwachung
- **■ Stop**: Stoppt die Überwachung
- **📊 Excel öffnen**: Öffnet die generierte Excel-Datei
- **📁 Ordner öffnen**: Öffnet den Scan-Ordner
- **Live-Log**: Zeigt Verarbeitungsstatus in Echtzeit
  - 🟢 Grün = Erfolg
  - 🔴 Rot = Fehler
  - 🔵 Blau = Info

#### 2. Stundenzettel scannen

- Lege gescannte Dateien in den `scans/` Ordner
- Unterstützte Formate: JPG, PNG, PDF
- Das System erkennt neue Dateien automatisch

#### 3. Verarbeitung

Das System extrahiert automatisch:
- ✅ Mitarbeitername
- ✅ Datum (DD.MM.YYYY)
- ✅ Startzeit (HH:MM)
- ✅ Endzeit (HH:MM)
- ✅ Pausenzeit (in Minuten)

#### 4. Arbeitszeitberechnung

**Pausenlogik:**
- Pausen ≤ 30 Minuten: Werden NICHT abgezogen
- Pausen > 30 Minuten: Werden abgezogen

**Beispiele:**
```
08:00 - 17:00 Uhr, 30 Min Pause  →  9,0 Stunden (Pause nicht abgezogen)
08:00 - 17:00 Uhr, 45 Min Pause  →  8,25 Stunden (45 Min abgezogen)
07:30 - 16:00 Uhr, 60 Min Pause  →  7,5 Stunden (60 Min abgezogen)
```

#### 5. Excel-Export

Die Excel-Datei wird automatisch erstellt mit:
- ✨ Professioneller Formatierung
- 📊 Automatischer Sortierung (Datum, Name)
- 🎨 Farbigen Überschriften
- 📏 Automatischer Spaltenbreite
- 🔢 Korrekten Datumsformaten

**Dateiname:** `stundenzettel_export_YYYY-MM-DD.xlsx`

**Spalten:**
- Name
- Datum
- Startzeit
- Endzeit
- Pause (Min)
- Netto-Stunden

## 📁 Projektstruktur

```
Stundenzettel-Automatisierung/
├── main.py                          # Hauptprogramm mit GUI
├── .env                             # Konfiguration (NICHT im Git!)
├── .env.example                     # Template für .env
├── .gitignore                       # Git Ignore-Regeln
├── requirements.txt                 # Python-Dependencies
├── README.md                        # Diese Datei
├── ANLEITUNG_KUNDE.txt             # Einfache Kundenanleitung
├── build_exe.bat                   # Windows EXE-Builder
├── modules/
│   ├── __init__.py
│   ├── ocr_processor.py            # Gemini API Integration
│   ├── time_calculator.py          # Arbeitszeitberechnung
│   ├── excel_exporter.py           # Excel-Export
│   ├── file_handler.py             # Datei-Operationen
│   └── gui.py                      # GUI-Komponenten
├── templates/
│   └── stundenzettel_prompt.txt    # Gemini API Prompt
├── scans/                          # Input-Ordner (leer)
├── output/                         # Excel-Dateien (generiert)
├── archive/                        # Archivierte Scans (generiert)
└── errors/                         # Fehlerhafte Dateien (generiert)
```

## 🔧 Konfiguration (.env)

```env
# Google Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Ordner-Konfiguration
SCAN_FOLDER=./scans
OUTPUT_FOLDER=./output
ARCHIVE_FOLDER=./archive
ERROR_FOLDER=./errors

# Optionale Einstellungen
WATCH_MODE=true          # Kontinuierliche Überwachung (true/false)
LOG_LEVEL=INFO          # Logging-Level (DEBUG/INFO/WARNING/ERROR)
```

## 🎁 EXE-Erstellung (für Kunden ohne Python)

### Windows

1. Führe `build_exe.bat` aus
2. Die `.exe` findest du in `dist/StundenzettelScanner.exe`
3. Kopiere folgende Dateien/Ordner ins `dist/` Verzeichnis:
   - `.env` (mit deinem API-Key)
   - `templates/` Ordner
   - `scans/`, `output/`, `archive/`, `errors/` Ordner (leer)

### Distribution

Die `.exe` kann ohne Python-Installation ausgeführt werden:
1. Erstelle einen Ordner für den Kunden
2. Kopiere alle Dateien aus `dist/`
3. Stelle sicher, dass `.env` mit gültigem API-Key vorhanden ist
4. Füge `ANLEITUNG_KUNDE.txt` hinzu

## 🐛 Troubleshooting

### Problem: "API-Key nicht gefunden"

**Lösung:**
1. Prüfe ob `.env` Datei existiert
2. Öffne `.env` und prüfe `GEMINI_API_KEY`
3. Stelle sicher, dass kein Platzhalter-Text enthalten ist

### Problem: "Keine Dateien gefunden"

**Lösung:**
1. Prüfe ob Dateien im `scans/` Ordner sind
2. Prüfe Dateiformat (JPG, PNG, PDF)
3. Prüfe Ordner-Pfade in `.env`

### Problem: "PDF-Fehler"

**Lösung:**
- Windows: Installiere [Poppler](http://blog.alivate.com.au/poppler-windows/)
- Linux: `sudo apt-get install poppler-utils`
- macOS: `brew install poppler`

### Problem: "OCR erkennt keine Daten"

**Lösung:**
1. Prüfe Scan-Qualität (mindestens 300 DPI empfohlen)
2. Stelle sicher, dass Text gut lesbar ist
3. Prüfe Log für Details

### Problem: "Excel öffnet nicht"

**Lösung:**
1. Prüfe ob Excel-Datei existiert in `output/`
2. Installiere Microsoft Excel oder LibreOffice
3. Öffne Datei manuell aus dem `output/` Ordner

## 📊 Logging

Das System erstellt folgende Log-Dateien:

- **process.log**: Alle Verarbeitungsschritte
- **errors/errors.log**: Detaillierte Fehlerbeschreibungen

## 🔒 Sicherheit

**WICHTIG - API-Key Sicherheit:**

- ✅ API-Key wird NUR in `.env` gespeichert
- ✅ `.env` ist in `.gitignore` (wird nicht ins Git hochgeladen)
- ✅ `.env.example` enthält nur Platzhalter
- ❌ Niemals API-Key im Code hardcoden
- ❌ Niemals `.env` mit anderen teilen
- ❌ Niemals API-Key ins Repository hochladen

## 🚀 Erweiterungen

Das System ist modular aufgebaut und kann einfach erweitert werden:

- 📄 **Servicescheine**: Template in `templates/serviceschein_prompt.txt` vorbereitet
- 📋 **Andere Dokumenttypen**: Einfach neue Templates hinzufügen
- 🎨 **Custom Styling**: GUI in `modules/gui.py` anpassbar
- 📊 **Export-Formate**: Excel-Modul erweiterbar

## 📝 Lizenz

Dieses Projekt ist für den privaten und kommerziellen Gebrauch freigegeben.

## 🤝 Support

Bei Problemen oder Fragen:
1. Prüfe diese README
2. Prüfe Log-Dateien
3. Erstelle ein Issue auf GitHub

## 🎉 Credits

- **OCR**: Google Gemini 2.0 Flash AI
- **GUI**: Python tkinter
- **Excel**: openpyxl
- **Dateiüberwachung**: watchdog

---

**Version:** 1.0  
**Erstellt:** 2024  
**Python:** 3.10+