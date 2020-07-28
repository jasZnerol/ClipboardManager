@echo off
set is_build=%1

:: %1 is defined if the program should be (re)build entirely and false if it should only start 
if "%is_build%"=="build" goto init_ClipboardManager
if not "%is_build%"=="build" goto start_ClipboardManager

:: Kill the virtual enviroment after the python script was terminated and enter has been pressed
:deactivate_venv
.\scripts\killVenv.bat

:: Init ClipboardManager by installing requirements/updating pip
:init_ClipboardManager
echo Installing requirements
echo.
python -m pip install --upgrade pip
pip install -r .\requirements.txt
goto start_ClipboardManager

:: Start python inside virtual python enviroment
:start_ClipboardManager
echo ClipboardManager is now running. Press ESC to quit.
echo.
.\src\app.py
goto deactivate_venv