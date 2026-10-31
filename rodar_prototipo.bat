@echo off
REM Sobe o NextLearn local e abre o prototipo no navegador (branch thiago/prototipo-neuro).
cd /d "%~dp0"
echo === 1/4 Ambiente Python ===
if not exist venv\Scripts\python.exe (
  py -3.12 -m venv venv 2>nul || python -m venv venv
)
if not exist venv\Scripts\python.exe (
  echo ERRO: nao achei o Python. Instale o Python 3.12 em python.org marcando "Add python.exe to PATH".
  pause
  exit /b 1
)
call venv\Scripts\activate.bat
echo === 2/4 Dependencias (demora so na primeira vez) ===
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
if errorlevel 1 (
  echo ERRO ao instalar dependencias. Copie a mensagem acima e mande para o Claude.
  pause
  exit /b 1
)
echo === 3/4 Banco de dados local ===
python manage.py migrate
echo === 4/4 Servidor: deixe esta janela aberta. Para parar, feche a janela. ===
start "" http://127.0.0.1:8000/prototipo/
python manage.py runserver
pause
