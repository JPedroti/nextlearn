"""Views do protótipo de design. Sem login e sem banco: tudo vem de dados.py, para desenhar a estrutura."""

from django.contrib.auth.views import LoginView
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


CENAS = [
    {"id": "laranja", "pose": "passos", "nome": "Passos curtos", "fala": "Aula longa demais? Eu divido em passos curtos, um de cada vez."},
    {"id": "azul", "pose": "livro", "nome": "Texto simples", "fala": "Texto difícil? Eu deixo as frases curtas, simples e diretas."},
    {"id": "verde", "pose": "pizza", "nome": "Exemplo concreto", "fala": "Ideia abstrata? Eu trago um exemplo do dia a dia para você enxergar."},
    {"id": "lilas", "pose": "fone", "nome": "Ouvir a aula", "fala": "Prefere ouvir? Eu leio a aula em voz alta para você."},
]


def entrada(request):
    """Tela de entrada com o mascote Next. Os botões levam ao login real (contas:entrar)."""
    return render(request, "prototipo/entrada.html", {"cenas": CENAS})


# Login real no visual do protótipo: autentica no Usuario do time e manda para contas:inicio,
# que redireciona pelo papel (professor -> painel, aluno -> aulas, família -> perfis).
PERFIS_LOGIN = {
    "professor": {"nome": "Professor(a)", "cor": "azul", "pose": "livro", "fala": "Bem-vindo de volta! Suas turmas estão te esperando."},
    "aluno": {"nome": "Aluno(a)", "cor": "laranja", "pose": "fone", "fala": "Oi! Bora aprender do seu jeito?"},
    "familia": {"nome": "Família", "cor": "lilas", "pose": "pizza", "fala": "Que bom ter vocês aqui. A família faz parte."},
}


class Login(LoginView):
    template_name = "prototipo/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        chave = self.request.GET.get("perfil") or self.request.POST.get("perfil") or "aluno"
        contexto["perfil_chave"] = chave if chave in PERFIS_LOGIN else "aluno"
        contexto["perfil"] = PERFIS_LOGIN[contexto["perfil_chave"]]
        contexto["perfis"] = PERFIS_LOGIN
        return contexto
