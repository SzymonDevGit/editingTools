@echo off
rem Drag one or more video files onto this file. An .srt appears next to each video.
setlocal
if "%~1"=="" (
    echo Drag one or more video files onto Subtitle.bat.
    pause
    exit /b 1
)
python "%~dp0autosubs.py" %*
echo.
pause
