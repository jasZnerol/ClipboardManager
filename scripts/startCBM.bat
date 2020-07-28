@echo off
goto init_ClipboardManager

:: Kill the virtual start_ClipboardManager after the python script was terminated and enter has been pressed
:deactivate_venv
.\scripts\killVenv.bat

:: Init ClipboardManager by installing requirements/updating pip
:init_ClipboardManager
echo Installing requirements
echo.
python -m pip install --upgrade pip
pip install -r ./requirements.txt
goto start_ClipboardManager

:: Start python inside virtual python enviroment
:start_ClipboardManager
echo ClipboardManager is now running. Press ESC to quit.
echo.
.\src\clipboard\clipboardManager.py
goto deactivate_venv