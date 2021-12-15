Echo Y | SCHTASKS /CREATE /SC MONTHLY /D 15 /TN "MyTasks\Run_autochar" /TR "C:\Users\lab\Automation\run_autochar.bat" /ST 11:00
SCHTASKS.EXE /RUN /TN "MyTasks\Run_autochar"