@echo off
rem Starts AutoSubtitler on this PC at http://127.0.0.1:8000/
cd /d "%~dp0"
start "" http://127.0.0.1:8000/
python serve.py
pause
