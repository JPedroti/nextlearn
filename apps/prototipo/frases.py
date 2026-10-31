"""Falas do Next geradas pela IA (endpoint compatível com OpenAI), com cache e frases de reserva.

Privacidade (LGPD/ECA Digital): a API recebe apenas matéria e assunto da aula, com regras de estilo derivadas dos apoios. Não enviamos nome, turma, nota ou progresso do aluno; o nome é incluído depois, no servidor. A chave fica no .env (IA_API_KEY) e nunca vai para o navegador nem para o Git.

import hashlib
import json
import os
import random
import urllib.request

from django.core.cache import cache

RESERVA = {
    "comecar": ["Bora para a próxima fase? Eu vou junto.", "Uma fase de cada vez. Começa quando quiser.",
                "Hoje tem {assunto}. Vamos descobrir juntos?"],
    "bom": ["Mandou bem na última! Vamos manter o ritmo.", "Sua última fase foi ótima. Próxima?"],
    "revisar": ["Errar faz parte. Vamos tentar de novo, com calma.", "Que tal revisar antes? Eu te ajudo."],
    "mundo": ["Bem-vindo ao {ambiente}! Cada fase aqui é um passo.", "Olha onde a gente chegou: {ambiente}!"],
}


def _estilo(apoios):
    regras = ["no máximo 14 palavras", "uma frase só", "português do Brasil", "tom gentil e animado",
              "sem emoji", "sem pressão de tempo", "sem comparar com outras pessoas", "não prometa prêmios"]
    if apoios.get("textual") or apoios.get("foco"):
        regras += ["linguagem literal: nada de ironia, metáfora ou expressão figurada", "palavras simples"]
    if apoios.get("foco"):
        regras += ["fale de uma coisa só"]
    if apoios.get("concreto"):
        regras += ["pode citar um exemplo do dia a dia"]
    return "; ".join(regras)


def _chamar_ia(contexto, apoios):
    chave = os.environ.get("IA_API_KEY") or os.environ.get("API_KEY")
    base = os.environ.get("IA_BASE_URL") or os.environ.get("API_BASE_URL", "")
    modelo = os.environ.get("IA_MODELO") or "gpt-4o-mini"
    if not chave or not base:
        return None, "sem endpoint (API_BASE_URL vazio no .env)"
    corpo = {
        "model": modelo, "temperature": 0.9, "max_tokens": 60,
        "messages": [
            {"role": "system", "content": "Você é o Next, um camaleão mascote de uma plataforma escolar para crianças e "
             "adolescentes. Escreva UMA fala curta para o aluno, a partir do contexto. Regras: " + _estilo(apoios) +
             ". Responda só com a fala, sem aspas."},
            {"role": "user", "content": json.dumps(contexto, ensure_ascii=False)},
        ],
    }
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=json.dumps(corpo).encode(),
                                 headers={"Authorization": f"Bearer {chave}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            dados = json.load(r)
        texto = dados["choices"][0]["message"]["content"].strip().strip('"').strip()
        return (texto[:140] if texto else None), "ia"
    except Exception as e:  # rede, chave, formato: cai na reserva sem quebrar a página
        return None, f"erro da IA: {type(e).__name__}"


def fala_do_next(aluno_id, contexto, apoios, nome=""):
    """Devolve (fala, origem). Cache de 1 hora por aluno + contexto, para não chamar a IA a cada recarga."""
    chave_cache = "next-fala-" + hashlib.sha1(f"{aluno_id}|{json.dumps(contexto, sort_keys=True)}|{sorted(apoios.items())}".encode()).hexdigest()
    salvo = cache.get(chave_cache)
    if salvo:
        return salvo
    texto, origem = _chamar_ia(contexto, apoios)
    if not texto:
        tipo = contexto.get("situacao", "comecar")
        texto = random.choice(RESERVA.get(tipo, RESERVA["comecar"])).format(**{k: contexto.get(k, "") for k in ("assunto", "ambiente")})
        origem = "reserva · " + origem
    if nome and random.random() < .5:
        texto = f"{nome}, " + texto[0].lower() + texto[1:]
    cache.set(chave_cache, (texto, origem), 3600)
    return texto, origem


def status_ia():
    base = os.environ.get("IA_BASE_URL") or os.environ.get("API_BASE_URL", "")
    chave = os.environ.get("IA_API_KEY") or os.environ.get("API_KEY")
    return {"chave": bool(chave), "endpoint": bool(base)}
