#!/usr/bin/env bash
# Roda no Render a cada deploy (veja render.yaml). Para no primeiro erro.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Cria o primeiro administrador se as variáveis DJANGO_SUPERUSER_* estiverem no painel do Render.
# Nos deploys seguintes ele já existe; o erro é ignorado e o build continua.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || echo "Administrador não foi criado (provavelmente já existe); seguindo."
fi
