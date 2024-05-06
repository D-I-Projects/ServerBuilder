@echo off
REM Minimiere das aktuelle Fenster
start /min "" cmd /c "cd /d %~dp0Files && start /min "" python GUIStart.py"
