@echo off
cd /d "%~dp0"
echo Jetpack Compose Masterclass - serving at http://localhost:8000
echo Press Ctrl+C to stop.
python build-site.py
python -m http.server 8000
