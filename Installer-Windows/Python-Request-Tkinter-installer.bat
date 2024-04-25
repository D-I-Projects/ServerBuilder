@echo off

REM Das aktuelle Verzeichnis auf das Verzeichnis der Batch-Datei setzen
cd /d "%~dp0"

REM Python Installation
echo Installing Python...
REM Download Python installer
bitsadmin /transfer "PythonInstaller" https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe "%CD%\python_installer.exe"
REM Install Python silently
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1
echo Python installed successfully.

REM Java 21 Installation
echo Installing Java 21...
REM Download Java 21 installer
bitsadmin /transfer "JavaInstaller" https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe "%CD%\java_installer.exe"
REM Install Java 21 silently
java_installer.exe /s INSTALL_SILENT=1 INSTALLDIR=C:\Java21
echo Java 21 installed successfully.

echo Installation complete.

REM PowerShell-Befehle ausführen
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Requests und Tkinter are getting installed.', 'Installation', 'Installed!', 'Information')"
powershell -Command "pip uninstall requests tk"
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

