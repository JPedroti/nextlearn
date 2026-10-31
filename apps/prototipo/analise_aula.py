"""Análise da aula para o professor: aponta o que deixaria a aula mais acessível para alunos neurodivergentes.

Junta duas fontes, sempre como SUGESTÃO (o professor decide; Parecer CNE/CP 15/2026):
1. O texto da aula e das questões (antes de dar a aula).
2. O que os alunos fizeram (acerto por questão, por versão, tempo, aula online: pausas e trechos repetidos).

Parâmetros e de onde vêm (docs/PERFIS_E_METRICAS.md, docs/METRICAS_ENSINO.md):
- Frases longas (> 20 palavras) e média de palavras por frase → P1/P2 leitura e linguagem (Filderman 2021; linguagem simples).
- Legibilidade (Flesch adaptado ao português, Martins et al. 1996) → P1/P2. Valor de produto: alvo >= 50 no 6º ano.
- Blocos grandes (> 120 palavras sem quebra) e duração estimada > 10 min → P3 atenção/memória de trabalho (Kofler 2020).
- Mais de uma instrução por enunciado ("e depois", "em seguida", vários verbos de comando) → P3.
- Negação e "exceto/incorreta" no enunciado → P2/P3 (carga de memória de trabalho; itens negativos confundem).
- Expressões figuradas → P2/P4 (leitura literal no TEA).
- Falta de exemplo concreto → P5/P7 (concreto, Benavides-Varela 2020) e P2.
- Falta de roteiro ("hoje vamos", "primeiro", "depois") → P4 previsibilidade (NCAEP 2020: apoios visuais e rotina).
- Questão com acerto < 50% → revisar enunciado; versão adaptada com acerto bem diferente da original → ver se a adaptação mudou a exigência.
Os limites numéricos são valor de produto, a calibrar com uso real.
"""

import re
import statistics

FIGURADAS = ["pé da letra", "quebrar o gelo", "num piscar de olhos", "pegar o jeito", "matar a charada", "dar uma mão",
             "ficar de olho", "chover no molhado", "bater na mesma tecla", "de cabeça", "acertar em cheio", "é mamão com açúcar",
             "cair a ficha", "faca de dois gumes", "custar os olhos da cara"]
NEGACOES = ["não", "exceto", "incorreta", "incorreto", "falsa", "falso", "nenhuma", "nenhum", "menos"]
EXEMPLO = ["por exemplo", "exemplo", "imagine", "pense em", "como uma", "como um", "no dia a dia", "pizza", "chocolate"]
ROTEIRO = ["hoje vamos", "hoje você", "primeiro", "depois", "por fim", "passo 1", "passo"]
COMANDOS = ["calcule", "explique", "marque", "escreva", "responda", "compare", "desenhe", "justifique", "identifique", "complete", "some"]


def _frases(texto):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+|\n+", texto) if len(f.strip().split()) >= 2]


def _silabas(palavra):
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõàü]+", palavra.lower())))


def legibilidade(texto):
    """Flesch adaptado ao português (Martins et al., 1996): 248,835 − 1,015·(palavras/frase) − 84,6·(sílabas/palavra)."""
    frases = _frases(texto)
    palavras = re.findall(r"[A-Za-zÀ-ÿ]+", texto)
    if not frases or not palavras:
        return None
    ip = 248.835 - 1.015 * (len(palavras) / len(frases)) - 84.6 * (sum(_silabas(p) for p in palavras) / len(palavras))
    return max(0, min(100, round(ip)))


def analisar(aula, questoes, respostas_por_questao=None, por_versao=None, online=None):
    texto = aula.conteudo
    t = texto.lower()
    frases = _frases(texto)
    palavras = len(re.findall(r"\w+", texto))
    tam = [len(f.split()) for f in frases] or [0]
    longas = [f for f in frases if len(f.split()) > 20]
    blocos = [b for b in re.split(r"\n\s*\n", texto) if b.strip()]
    bloco_max = max((len(b.split()) for b in blocos), default=0)
    minutos = round(palavras / 110 + 1.5 * len(questoes), 1)   # 110 palavras/min no 6º ano (valor de produto) + 1,5 min por questão
    leg = legibilidade(texto)
    figuradas = [f for f in FIGURADAS if f in t]
    tem_exemplo = any(e in t for e in EXEMPLO)
    tem_roteiro = any(r in t for r in ROTEIRO)
    q_negativas, q_multiplas, q_longas = [], [], []
    for i, q in enumerate(questoes, 1):
        e = q.enunciado.lower()
        if any(re.search(rf"\b{n}\b", e) for n in NEGACOES):
            q_negativas.append(i)
        if sum(1 for c in COMANDOS if c in e) >= 2 or " e depois " in e or "em seguida" in e:
            q_multiplas.append(i)
        if len(e.split()) > 25:
            q_longas.append(i)

    checagens = [
        # (ok?, peso, nome, valor mostrado, sugestão, perfis que ganham)
        (statistics.mean(tam) <= 15, 15, "Frases curtas", f"{statistics.mean(tam):.0f} palavras por frase em média; {len(longas)} frase(s) com mais de 20",
         "Quebre as frases longas em duas. Uma ideia por frase.", "Leitura e linguagem (P1, P2)"),
        (leg is None or leg >= 50, 10, "Legibilidade", f"índice {leg if leg is not None else '–'} (alvo ≥ 50 no 6º ano)",
         "Troque palavras longas ou raras por palavras do dia a dia.", "Leitura e linguagem (P1, P2)"),
        (bloco_max <= 120, 15, "Blocos curtos", f"maior bloco com {bloco_max} palavras (alvo ≤ 120)",
         "Divida o texto em blocos curtos com um subtítulo cada.", "Atenção e memória de trabalho (P3)"),
        (minutos <= 12, 10, "Duração", f"cerca de {minutos} min (alvo ≤ 12 min por bloco de estudo)",
         "Separe em duas aulas ou ponha uma pausa no meio.", "Atenção (P3)"),
        (not q_multiplas, 15, "Uma instrução por questão", f"{len(q_multiplas)} questão(ões) com mais de um comando" + (f" (nº {', '.join(map(str, q_multiplas))})" if q_multiplas else ""),
         "Deixe um comando por enunciado; se precisar de dois, vire duas questões.", "Atenção e memória de trabalho (P3)"),
        (not q_negativas, 10, "Enunciados sem negação", f"{len(q_negativas)} questão(ões) com 'não/exceto/incorreta'" + (f" (nº {', '.join(map(str, q_negativas))})" if q_negativas else ""),
         "Pergunte na forma positiva ('qual está certa?'). Se a negação for necessária, destaque a palavra.", "Linguagem e atenção (P2, P3)"),
        (not figuradas, 5, "Linguagem literal", ", ".join(figuradas) if figuradas else "nenhuma expressão figurada encontrada",
         "Troque expressões figuradas por frases literais.", "Linguagem e TEA (P2, P4)"),
        (tem_exemplo, 10, "Exemplo concreto", "tem exemplo" if tem_exemplo else "nenhum exemplo do dia a dia encontrado",
         "Inclua um exemplo concreto (pizza, dinheiro, régua) ou uma figura simples.", "Matemática e ritmo (P5, P7)"),
        (tem_roteiro, 10, "Roteiro no início", "tem roteiro" if tem_roteiro else "sem 'hoje vamos… primeiro… depois…'",
         "Abra a aula dizendo o que vai acontecer: 'Hoje vamos… Primeiro… Depois…'.", "Previsibilidade e TEA (P4)"),
    ]
    pontos = sum(peso for ok, peso, *_ in checagens if ok)
    total = sum(peso for _, peso, *_ in checagens)
    indice = round(100 * pontos / total)

    dados = []
    if respostas_por_questao:
        for i, (q, rs) in enumerate(respostas_por_questao, 1):
            if rs:
                ac = round(100 * sum(rs) / len(rs))
                dados.append({"q": i, "acerto": ac, "n": len(rs), "alerta": ac < 50, "enunciado": q.enunciado})
    sugestoes_dados = []
    for d in dados:
        if d["alerta"]:
            sugestoes_dados.append(f"Questão {d['q']}: só {d['acerto']}% de acerto. Revise o enunciado ou retome o conceito antes.")
    if por_versao:
        orig = por_versao.get(0)
        for m, ac in por_versao.items():
            if m and orig is not None and abs(ac - orig) >= 30:
                sugestoes_dados.append(f"A versão adaptada (combinação {m}) teve {ac}% contra {orig}% da original: confira se a adaptação manteve a mesma exigência.")
    if online:
        if online.get("repeticoes"):
            trecho, n = max(online["repeticoes"].items(), key=lambda kv: kv[1])
            sugestoes_dados.append(f"Aula online: o trecho {int(trecho) + 1} foi repetido {n} vez(es). Pode estar confuso ou rápido demais.")
        if online.get("pausas", 0) >= 3:
            sugestoes_dados.append(f"Aula online: {online['pausas']} pausas. Considere blocos menores.")
    return {
        "indice": indice, "checagens": [{"ok": ok, "peso": peso, "nome": n, "valor": v, "sugestao": s, "perfis": p} for ok, peso, n, v, s, p in checagens],
        "palavras": palavras, "frases": len(frases), "minutos": minutos, "legibilidade": leg, "longas": longas[:3],
        "dados": dados, "sugestoes_dados": sugestoes_dados, "online": online or {},
    }
