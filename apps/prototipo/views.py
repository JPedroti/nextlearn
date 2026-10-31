"""Views do protótipo de design. Sem login e sem banco: tudo vem de dados.py, para desenhar a estrutura."""

from django.shortcuts import render

from apps.perfis.models import APOIOS, nomes_da_mascara

from . import dados
from .temas import TEMAS, tema_para

PRESETS = [
    (0, "Original"),
    (4, "Foco"),
    (2, "Textual"),
    (1, "Concreto"),
    (6, "Foco + Textual"),
    (7, "Os três"),
]

# Máscara sem versão escrita → usa a mais próxima que existe no exemplo
FALLBACK = {3: 2, 5: 4}


def _contexto(request):
    try:
        mascara = int(request.GET.get("perfil", 0))
    except ValueError:
        mascara = 0
    mascara = mascara if 0 <= mascara <= 7 else 0
    limpo = request.GET.get("limpo") == "1"
    tema = tema_para(mascara, limpo)
    return {
        "mascara": mascara,
        "foco": bool(mascara & 4),
        "textual": bool(mascara & 2),
        "concreto": bool(mascara & 1),
        "apoios": nomes_da_mascara(mascara),
        "limpo": limpo,
        "tema_id": tema,
        "tema": TEMAS[tema],
        "presets": PRESETS,
        "qs": f"perfil={mascara}" + ("&limpo=1" if limpo else ""),
    }


def inicio(request):
    ctx = _contexto(request)
    ctx["area"] = "inicio"
    ctx["temas"] = TEMAS
    return render(request, "prototipo/inicio.html", ctx)


def aluno(request):
    ctx = _contexto(request)
    ctx["area"] = "aluno"
    ctx["aulas"] = dados.AULAS_ALUNO
    return render(request, "prototipo/aluno.html", ctx)


def aula(request):
    ctx = _contexto(request)
    ctx["area"] = "aluno"
    m = ctx["mascara"]
    versao = dados.VERSOES.get(FALLBACK.get(m, m))
    ctx["aula"] = dados.AULA
    ctx["passos"] = versao.get("passos") if versao else None
    ctx["paragrafos"] = (versao.get("paragrafos") if versao else None) or (None if ctx["passos"] else dados.AULA["original"])
    visual = versao.get("visual") if versao else None
    if visual:
        for barra in visual:
            barra["celulas"] = [i < barra["marcadas"] for i in range(barra["partes"])]
    ctx["visual"] = visual
    usar_simples = ctx["textual"]
    ctx["questoes"] = [
        {"n": i + 1, "enunciado": q["simples"] if usar_simples else q["original"], "alternativas": q["alternativas"], "correta": q["correta"]}
        for i, q in enumerate(dados.QUESTOES)
    ]
    return render(request, "prototipo/aula.html", ctx)


def professor(request):
    ctx = _contexto(request)
    ctx["area"] = "professor"
    alunos = []
    for a in dados.ALUNOS:
        alunos.append({**a, "apoios": nomes_da_mascara(a["mascara"]), "tema": TEMAS[tema_para(a["mascara"])]})
    ctx["alunos"] = alunos
    ctx["sugestoes"] = dados.SUGESTOES
    respondidos = [a["acertos"] for a in dados.ALUNOS if a["acertos"] is not None]
    ctx["media"] = round(sum(respondidos) / len(respondidos)) if respondidos else None
    ctx["respondidos"] = len(respondidos)
    combinacoes = sorted({a["mascara"] for a in dados.ALUNOS if a["mascara"]})
    ctx["versoes"] = [
        {"mascara": c, "nomes": nomes_da_mascara(c), "status": "Aprovada" if c in (2, 4) else "Aguardando revisão"}
        for c in combinacoes
    ]
    ctx["apoios_def"] = APOIOS
    return render(request, "prototipo/professor.html", ctx)


def familia(request):
    ctx = _contexto(request)
    ctx["area"] = "familia"
    chaves = [k for k, ligado in (("foco", ctx["foco"]), ("textual", ctx["textual"]), ("concreto", ctx["concreto"])) if ligado] or ["base"]
    ctx["dicas"] = [dados.DICAS_FAMILIA[k] for k in chaves]
    return render(request, "prototipo/familia.html", ctx)
