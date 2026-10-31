@echo off
REM Salva e envia para o GitHub as suas mudancas do prototipo (usa o seu login do Git no Windows).
REM So entram as pastas do prototipo e os docs do Thiago. Nunca faz force push e nao mexe na main.
cd /d "%~dp0"
set BRANCH=thiago/prototipo-neuro
for /f %%b in ('git rev-parse --abbrev-ref HEAD') do set ATUAL=%%b
if not "%ATUAL%"=="%BRANCH%" (
  echo [%date% %time%] pulado: a pasta esta na branch %ATUAL% >> envio_git.log
  exit /b 0
)
git add -- apps/prototipo templates/prototipo static/prototipo docs/historico_prompts/thiago.md docs/area_do_aluno.md docs/design_neuro.md >> envio_git.log 2>&1
git diff --cached --quiet
if errorlevel 1 git commit -q -m "Atualizacao automatica do prototipo" >> envio_git.log 2>&1
echo [%date% %time%] enviando %BRANCH% >> envio_git.log
git push -q origin %BRANCH% >> envio_git.log 2>&1
if errorlevel 1 (
  echo [%date% %time%] ERRO no envio, veja acima >> envio_git.log
  if not "%1"=="silencioso" ( echo Deu erro no envio. Abra o arquivo envio_git.log e mande para o Claude. & pause )
  exit /b 1
)
echo [%date% %time%] ok >> envio_git.log
if not "%1"=="silencioso" ( echo Enviado para o GitHub. & timeout /t 3 >nul )
