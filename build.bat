@echo off
cd /d "%~dp0"
D:\works\SD\py\python.exe -m PyInstaller --onefile --windowed --icon=delta.ico --name="DeltaGunTool" main.py
echo 打包完成！程序位于: dist\DeltaGunTool.exe
pause