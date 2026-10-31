@echo off
schtasks /Delete /F /TN "NextLearn envio git"
schtasks /Delete /F /TN "NextLearn servidor"
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*manage.py runserver*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
echo Modo automatico desligado e site local parado.
pause
