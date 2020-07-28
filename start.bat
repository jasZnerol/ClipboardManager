@echo off
if exist %cd%\env .\env\Scripts\activate & .\scripts\startCBM.bat
if not exist  %cd%\env echo No enviroment created yet. Building project ... & .\build.bat
