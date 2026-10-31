"""
Configurações do Django para o NextLearn.

Tudo que muda entre o computador da equipe e o servidor (senhas, banco, modo debug)
vem de variáveis de ambiente: localmente do arquivo `.env`, em produção do painel do Render.
A lista completa está em `.env.example`.
"""

import os
import sys
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Lê o arquivo .env (se existir) e coloca os valores em os.environ.
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "sim")


def env_list(name):
    return [item.strip() for item in os.environ.get(name, "").split(",") if item.strip()]


# --- Segurança -------------------------------------------------------------

DEBUG = env_bool("DEBUG", default=False)

SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError("Defina a variável de ambiente SECRET_KEY (veja .env.example).")
    SECRET_KEY = "chave-apenas-para-desenvolvimento-local"

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS") or ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host not in ("localhost", "127.0.0.1")]

# O Render informa sozinho o endereço público do serviço (ex.: nextlearn.onrender.com).
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# O Render recebe o HTTPS e repassa para o Django; este cabeçalho avisa que a conexão era segura.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


# --- Apps ------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps do NextLearn
    "apps.contas",
    "apps.turmas",
    "apps.perfis",
    "apps.aulas",
    "apps.painel",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.perfis.context_processors.preferencias",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- Banco de dados --------------------------------------------------------
# Sem DATABASE_URL, usa SQLite local (arquivo db.sqlite3).
# Em produção, DATABASE_URL é a connection string do Postgres no Neon.

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# --- Login -----------------------------------------------------------------

AUTH_USER_MODEL = "contas.Usuario"

LOGIN_URL = "contas:entrar"
LOGIN_REDIRECT_URL = "contas:inicio"
LOGOUT_REDIRECT_URL = "contas:entrar"

# Nos testes automáticos, um hash de senha rápido (e inseguro) deixa a suíte bem mais rápida.
# Nunca vale para o site de verdade: só quando o comando é `manage.py test`.
if len(sys.argv) > 1 and sys.argv[1] == "test":
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Idioma e fuso ---------------------------------------------------------

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# --- Arquivos estáticos (CSS, JS, fontes) ----------------------------------
# Em produção, o WhiteNoise serve os arquivos juntados pelo `collectstatic` em staticfiles/.

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- IA (usado a partir da Fatia 2, em ia/cliente.py) ----------------------

# Provedor: "gemini" (padrão) ou "openai" (DeepSeek, Groq, OpenAI, etc.)
IA_PROVEDOR = os.environ.get("IA_PROVEDOR", "gemini")

# Gemini (Google AI Studio)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

# OpenAI-compatible (DeepSeek, Groq, OpenAI, etc.)
IA_API_KEY = os.environ.get("IA_API_KEY", "")
IA_BASE_URL = os.environ.get("IA_BASE_URL", "")
IA_MODEL = os.environ.get("IA_MODEL", "deepseek-chat")
