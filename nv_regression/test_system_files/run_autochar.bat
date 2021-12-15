@echo off
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
D:
cd d:\tmp\PowerScripts\Autochar
python .\Run_Automation1.py
