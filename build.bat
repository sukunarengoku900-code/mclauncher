@echo off
cd /d "%~dp0"
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m PyInstaller --noconfirm --onefile --windowed --name mcLauncher mc_launcher.py
echo.
echo EXE criado em: dist\mcLauncher.exe
pause
