@echo off
echo ========================================
echo  Stundenzettel Scanner - EXE Builder
echo ========================================
echo.
echo Installiere PyInstaller...
pip install pyinstaller

echo.
echo Erstelle .exe-Datei...
pyinstaller --onefile --windowed --name="StundenzettelScanner" main.py

echo.
echo ========================================
echo  Fertig!
echo ========================================
echo Die .exe findest du in: dist\StundenzettelScanner.exe
echo.
echo WICHTIG: Kopiere folgende Dateien ins dist\ Verzeichnis:
echo  - .env (mit deinem API-Key)
echo  - templates\ Ordner
echo  - scans\, output\, archive\, errors\ Ordner
echo.
pause
