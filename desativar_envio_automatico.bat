@echo off
schtasks /Delete /F /TN "NextLearn envio git"
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\NextLearn servidor.vbs" >nul 2>&1
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*manage.py runserver*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
echo Modo automatico desligado e site local parado.
pause
