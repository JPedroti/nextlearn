"""Questões de rascunho geradas SEM IA, quando a IA não está configurada neste computador.

Servem para o fluxo nunca travar: o professor sempre revisa, corrige e aprova antes de publicar.
Com a IA configurada (IA_PROVEDOR/IA_API_KEY/IA_BASE_URL ou GEMINI_API_KEY), usamos ia/gerar_questoes.py (Cauã).
"""

import random
import re

PARADAS = set("""a o as os um uma uns umas de do da dos das em no na nos nas por para com sem sobre entre que quando
como porque pois mas ou e é são ser foi era há ter tem têm seu sua seus suas este esta isso isto aquele aquela muito
mais menos também já ainda cada todo toda todos todas mesmo outro outra outros outras qual quais onde então assim
hoje vamos parte sobre""".split())


def _palavras_chave(texto):
    palavras = re.findall(r"[A-Za-zÀ-ÿ]{6,}", texto)
    contagem = {}
    for p in palavras:
        k = p.lower()
        if k not in PARADAS:
            contagem[k] = contagem.get(k, 0) + 1
    return sorted(contagem, key=lambda k: (-contagem[k], -len(k)))


def gerar_rascunho(texto_fase, texto_material, semente=0):
    rnd = random.Random(semente)
    frases = [f.strip() for f in re.split(r"(?<=[.!?])\s+", texto_fase) if 8 <= len(f.split()) <= 40 and not f.lower().startswith("hoje vamos")]
    chaves_mat = _palavras_chave(texto_material)
    questoes = []
    usadas = set()
    for frase in frases:
        candidatas = [k for k in _palavras_chave(frase) if k not in usadas]
        if not candidatas:
            continue
        alvo = candidatas[0]
        usadas.add(alvo)
        lacuna = re.sub(rf"\b{re.escape(alvo)}\b", "_____", frase, count=1, flags=re.IGNORECASE)
        distratores = [k for k in chaves_mat if k != alvo][:8]
        rnd.shuffle(distratores)
        alts = [alvo] + distratores[:3]
        while len(alts) < 3:
            alts.append({0: "nenhuma das anteriores", 1: "não sei"}.get(len(alts) - 1, "outra"))
        rnd.shuffle(alts)
        questoes.append({"tipo": "multipla", "enunciado": f"Complete a frase: {lacuna}", "alternativas": alts,
                         "indice_correto": alts.index(alvo), "resposta_referencia": ""})
        if len(questoes) == 2:
            break
    if frases:
        questoes.append({"tipo": "flashcard", "enunciado": "Explique com suas palavras a ideia principal deste trecho.",
                         "alternativas": [], "indice_correto": None, "resposta_referencia": frases[0]})
    return questoes
