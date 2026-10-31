"""Testa a chave da API lida do .env (endpoint compativel com OpenAI)."""
import json, os, sys, urllib.request
from pathlib import Path

def carregar_env(caminho=Path(__file__).resolve().parent.parent / ".env"):
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            k, v = linha.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

carregar_env()
chave, base = os.environ.get("API_KEY"), os.environ.get("API_BASE_URL", "").rstrip("/")
if not chave:
    sys.exit("API_KEY ausente no .env")
if not base:
    sys.exit("API_BASE_URL vazio no .env - informe o endpoint do servico")
req = urllib.request.Request(f"{base}/models", headers={"Authorization": f"Bearer {chave}"})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        dados = json.load(r)
    modelos = [m.get("id") for m in dados.get("data", [])]
    print(f"OK - chave valida. {len(modelos)} modelos:", ", ".join(modelos[:15]))
except urllib.error.HTTPError as e:
    print(f"Falhou: HTTP {e.code} - {e.read()[:300]!r}")
