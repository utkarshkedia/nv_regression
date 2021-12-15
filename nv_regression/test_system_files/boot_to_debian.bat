@echo off
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
c:
cd C:\Users\lab\Automation
.\boot_to_debian.pl

