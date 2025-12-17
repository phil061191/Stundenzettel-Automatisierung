# Stundenzettel Scanner - Schnellreferenz

## 🚀 Schnellstart

### Ersteinrichtung (Nur einmal)

1. **Python installieren** (falls noch nicht vorhanden)
   - Download: https://www.python.org/downloads/
   - Mindestens Version 3.10

2. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

3. **API-Key erstellen**
   - Besuche: https://aistudio.google.com/app/apikey
   - Klicke "Create API Key"
   - Kopiere den Key

4. **.env Datei erstellen**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```
   
5. **API-Key eintragen**
   - Öffne `.env` mit einem Texteditor
   - Ersetze `your_api_key_here` mit deinem echten API-Key
   - Speichern

### Tägliche Nutzung

1. **Programm starten**
   ```bash
   python main.py
   ```

2. **Start klicken**
   - Grüner "Start" Button in der GUI

3. **Stundenzettel scannen**
   - Dateien in `scans/` Ordner legen
   - System erkennt automatisch neue Dateien

4. **Excel öffnen**
   - "Excel öffnen" Button klicken
   - Oder manuell: `output/stundenzettel_export_*.xlsx`

## 📁 Ordnerstruktur

```
scans/      → Hier Scans ablegen (JPG, PNG, PDF)
output/     → Hier werden Excel-Dateien erstellt
archive/    → Erfolgreich verarbeitete Dateien
errors/     → Fehlerhafte Dateien
```

## 🎯 Unterstützte Formate

- ✅ JPG / JPEG
- ✅ PNG
- ✅ PDF (erste Seite)

## ⚙️ Pausenberechnung

**Regel:** Nur Pausen > 30 Minuten werden abgezogen

| Arbeitszeit | Pause | Netto-Stunden |
|-------------|-------|---------------|
| 08:00-17:00 | 30min | 9,0h          |
| 08:00-17:00 | 45min | 8,25h         |
| 07:30-16:00 | 60min | 7,5h          |

## 🔧 Häufige Probleme

### "API-Key nicht gefunden"
→ Prüfe `.env` Datei, stelle sicher dass kein Platzhalter drin steht

### "Keine Dateien gefunden"
→ Lege Dateien in den `scans/` Ordner

### "OCR erkennt nichts"
→ Scan-Qualität erhöhen (mindestens 300 DPI)

### "Excel öffnet nicht"
→ Microsoft Excel oder LibreOffice installieren

## 📊 Logs

- **Live-Log**: Im GUI-Fenster
  - 🟢 Grün = Erfolg
  - 🔴 Rot = Fehler
  - 🔵 Blau = Info

- **Datei-Logs**:
  - `process.log` - Alle Schritte
  - `errors/errors.log` - Fehlerdetails

## 🎁 EXE erstellen (Windows)

```batch
build_exe.bat
```

→ Fertige .exe in `dist/` Ordner

## 🔒 Sicherheit

⚠️ **WICHTIG:**
- API-Key NIEMALS teilen
- `.env` Datei NICHT ins Git hochladen
- `.env` NICHT per E-Mail versenden

## 📞 Support

1. Prüfe diese Referenz
2. Lies `README.md`
3. Prüfe Log-Dateien
4. Erstelle GitHub Issue

## 🎨 GUI-Bedienung

### Buttons

- **▶ Start** - Startet Überwachung
- **■ Stop** - Stoppt Überwachung
- **📊 Excel öffnen** - Öffnet neueste Excel-Datei
- **📁 Ordner öffnen** - Öffnet Scan-Ordner

### Menü

- **Datei → Excel öffnen** - Excel direkt öffnen
- **Datei → Ordner öffnen** - Scan-Ordner öffnen
- **Hilfe → Anleitung** - Kurze Hilfe anzeigen

### Status-Anzeige

- ⚫ Bereit - Warten auf Start
- 🟢 Aktiv - System läuft
- 🔴 Fehler - Etwas ist schief gelaufen

## 💡 Tipps & Tricks

### Bessere OCR-Erkennung
- Scan-Auflösung: mindestens 300 DPI
- Farbe: Schwarz-Weiß oder Graustufen
- Kontrast: Hoch
- Ausrichtung: Gerade

### Performance
- Große PDF-Dateien: Nur erste Seite wird verarbeitet
- Mehrere Dateien: Werden nacheinander verarbeitet
- Watchdog: Erkennt neue Dateien in ~1 Sekunde

### Batch-Verarbeitung
- Einfach alle Scans auf einmal in `scans/` legen
- System verarbeitet automatisch alle
- Status wird im Log angezeigt

## 📝 Beispiel-Workflow

1. Stundenzettel scannen → als JPG speichern
2. Datei in `scans/` Ordner kopieren
3. Automatische Verarbeitung startet
4. Grüne Meldung im Log = Erfolgreich
5. Excel-Datei wird aktualisiert
6. Original wird archiviert
7. Bei Fehler → Datei landet in `errors/`

## 🔄 Updates

### Python-Pakete aktualisieren
```bash
pip install -r requirements.txt --upgrade
```

### Projekt aktualisieren
```bash
git pull
pip install -r requirements.txt
```

## 📦 Backup

**Wichtige Dateien für Backup:**
- `.env` (enthält API-Key!)
- `output/*.xlsx` (Excel-Dateien)
- `archive/*` (Archiv)
- `process.log` (Historie)

**NICHT ins Backup:**
- `scans/` (wird geleert)
- `__pycache__/` (Temp-Dateien)
- `.git/` (Git-Daten)

---

**Version:** 1.0  
**Letzte Aktualisierung:** Dezember 2024
