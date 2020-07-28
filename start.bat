@echo off
:: Create venv folder and venv if it does not exists already
if exist ./env goto start_venv
if not exist ./env goto init_venv

:: Setup virtual python enviroment
:init_venv
echo Creating Venv
echo.
md env
python -m venv %cd%/env
goto start_venv

:: Start virtual python enviroment
:start_venv
.\env\Scripts\activate & .\scripts\startCBM.bat


