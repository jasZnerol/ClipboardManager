@echo off
:: Create venv folder and venv if it does not exists already
goto init_venv

:: Setup virtual python enviroment
:init_venv
echo Creating Venv
echo.
rmdir /S /Q .\env
md env
python -m venv %cd%/env
goto start_venv

:: Start virtual python enviroment
:start_venv
set flag=build
.\env\Scripts\activate & .\scripts\startCBM.bat build


