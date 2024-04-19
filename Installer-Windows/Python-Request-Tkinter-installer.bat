@echo off

REM Das aktuelle Verzeichnis auf das Verzeichnis der Batch-Datei setzen
cd /d "%~dp0"

REM PowerShell-Befehle ausführen
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Requests und Tkinter werden ueber pip installiert.', 'Installation', 'OK', 'Information')"
powershell -Command "pip install requests tk"

REM Überprüfen, ob die Installation erfolgreich war
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python ist nicht installiert.
) else (
    echo Python ist bereits installiert.
)

REM Überprüfen, ob Requests installiert ist
pip show requests > nul 2>&1
if %errorlevel% neq 0 (
    echo Requests ist nicht installiert.
) else (
    echo Requests ist bereits installiert.
)

REM Überprüfen, ob Tkinter installiert ist
pip show tk > nul 2>&1
if %errorlevel% neq 0 (
    echo Tkinter ist nicht installiert.
) else (
    echo Tkinter ist bereits installiert.
)


REM Aufforderung zum Drücken einer Taste, um das Fenster offen zu halten
pause

