@echo off
REM Default: preview. Example: setup.cmd -Profile full -Apply -WithSkills -WithTools
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1" %*
exit /b %ERRORLEVEL%
