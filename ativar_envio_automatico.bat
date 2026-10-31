@echo off
REM Liga o modo automatico:
REM  1) a cada 5 minutos salva e envia as mudancas do prototipo para o GitHub;
REM  2) o site local fica sempre ligado (liga sozinho quando voce entra no Windows).
REM Para desligar: desativar_envio_automatico.bat
cd /d "%~dp0"
if not exist venv\Scripts\python.exe ( echo Rode primeiro o rodar_prototipo.bat uma vez, para instalar o ambiente. & pause & exit /b 1 )
echo Testando o envio uma vez (pode pedir login do GitHub na primeira vez)...
call enviar_git.bat
if errorlevel 1 exit /b 1
schtasks /Create /F /SC MINUTE /MO 5 /TN "NextLearn envio git" /TR "wscript.exe \"%~dp0enviar_git_oculto.vbs\""
REM Site ligado ao entrar no Windows: atalho na pasta Inicializar (nao precisa de administrador)
echo CreateObject("WScript.Shell").Run "wscript.exe ""%~dp0servidor_oculto.vbs""", 0, False> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\NextLearn servidor.vbs"
wscript.exe "%~dp0servidor_oculto.vbs"
timeout /t 4 >nul
start "" http://127.0.0.1:8000/prototipo/entrar/
echo.
echo Pronto! O site fica em http://127.0.0.1:8000/prototipo/entrar/ e recarrega sozinho quando um arquivo muda.
echo As mudancas vao para o GitHub a cada 5 minutos. Historico: envio_git.log e servidor.log
pause
