@echo off
REM Envia para o GitHub os commits da branch do prototipo (usa o seu login do Git no Windows).
REM Nunca faz force push e nao mexe na main.
cd /d "%~dp0"
set BRANCH=thiago/prototipo-neuro
echo [%date% %time%] enviando %BRANCH% >> envio_git.log
git push origin %BRANCH% >> envio_git.log 2>&1
if errorlevel 1 (
  echo [%date% %time%] ERRO no envio, veja acima >> envio_git.log
  if not "%1"=="silencioso" ( echo Deu erro no envio. Abra o arquivo envio_git.log e mande para o Claude. & pause )
  exit /b 1
)
echo [%date% %time%] ok >> envio_git.log
if not "%1"=="silencioso" ( echo Enviado para o GitHub. & timeout /t 3 >nul )
