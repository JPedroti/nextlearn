@echo off
REM Cria uma tarefa do Windows que envia a branch do prototipo para o GitHub a cada 10 minutos.
REM Para desligar: rode desativar_envio_automatico.bat
cd /d "%~dp0"
echo Testando o envio uma vez (pode pedir login do GitHub na primeira vez)...
call enviar_git.bat
if errorlevel 1 exit /b 1
schtasks /Create /F /SC MINUTE /MO 10 /TN "NextLearn envio git" /TR "wscript.exe \"%~dp0enviar_git_oculto.vbs\""
if errorlevel 1 ( echo Nao consegui criar a tarefa. & pause & exit /b 1 )
echo.
echo Pronto: a cada 10 minutos os commits novos vao para o GitHub sozinhos.
echo O historico fica em envio_git.log.
pause
