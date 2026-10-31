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

    def get_success_url(self):
        url = self.get_redirect_url()
        if not url and self.request.user.papel == "aluno":
            from django.urls import reverse

            return reverse("prototipo:painel_aluno")
        return url or super().get_success_url()

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        chave = self.request.GET.get("perfil") or self.request.POST.get("perfil") or "aluno"
        contexto["perfil_chave"] = chave if chave in PERFIS_LOGIN else "aluno"
        contexto["perfil"] = PERFIS_LOGIN[contexto["perfil_chave"]]
        contexto["perfis"] = PERFIS_LOGIN
        return contexto


# ---------------------------------------------------------------------------
# Painel do aluno (dados reais do banco; no teste local, o aluno fictício do `contas_teste`)
# ---------------------------------------------------------------------------
# Parâmetros seguidos (docs/METRICAS_ENSINO.md e docs/PERFIS_E_METRICAS.md):
# - o aluno se compara só com ele mesmo (nada de ranking); certo/errado sempre com texto;
# - ofensiva SEMANAL e sem perda (semana parada só pausa); meta mínima pequena;
# - tempo de estudo mostrado junto do limite combinado com a família (ECA Digital);
# - apoio de foco (P3): uma ação principal por vez, listas recolhidas, sem animação;
# - treino curto, uma questão por tela, com confirmação antes de enviar.

META_SEMANAL = 2          # aulas por semana (combinada com professor e família)
PRAZO_DIAS = 7            # valor de produto, a calibrar: o backend ainda não tem prazo; usamos publicação + 7 dias
LIMITE_DIARIO_MIN = 40    # minutos por dia combinados com a família


def _materia(titulo):
    return titulo.split(":", 1)[0].strip() if ":" in titulo else "Geral"


def _assunto(titulo):
    return titulo.split(":", 1)[1].strip() if ":" in titulo else titulo


def _dados_aluno(aluno):
    from datetime import timedelta

    from django.utils import timezone

    from apps.aulas.models import Resposta

    agora = timezone.localtime()
    respostas = list(Resposta.objects.filter(aluno=aluno).select_related("questao__aula"))
    por_aula = {}
    for r in respostas:
        d = por_aula.setdefault(r.questao.aula_id, {"acertos": 0, "total": 0, "quando": r.criado_em, "ms": r.tempo_ms or 0})
        d["total"] += 1
        d["acertos"] += r.correta
        d["quando"] = min(d["quando"], r.criado_em)

    feitas, pendentes = [], []
    for aula in aluno.turma.aulas.filter(publicada=True).order_by("pk"):
        item = {"aula": aula, "materia": _materia(aula.titulo), "assunto": _assunto(aula.titulo), "n_questoes": aula.questoes.count()}
        if aula.pk in por_aula:
            d = por_aula[aula.pk]
            item.update(acertos=d["acertos"], total=d["total"], quando=timezone.localtime(d["quando"]), ms=d["ms"],
                        nota=round(10 * d["acertos"] / d["total"], 1))
            feitas.append(item)
        else:
            pendentes.append(item)
    feitas.sort(key=lambda i: i["quando"])

    def media(itens):
        return round(sum(i["nota"] for i in itens) / len(itens), 1) if itens else None

    # Notas por matéria e evolução (as últimas 6, para ver o próprio progresso)
    materias = {}
    for i in feitas:
        materias.setdefault(i["materia"], []).append(i)
    por_materia = [{"nome": m, "media": media(its), "n": len(its), "pct": int(media(its) * 10)} for m, its in sorted(materias.items())]
    evolucao = [{"nota": i["nota"], "rotulo": i["assunto"], "altura": max(6, int(i["nota"] * 12))} for i in feitas[-6:]]

    corte = agora - timedelta(days=30)
    recentes = [i for i in feitas if i["quando"] >= corte]
    antigas = [i for i in feitas if i["quando"] < corte]
    m_rec, m_ant = media(recentes), media(antigas)

    # Ofensiva semanal: semanas seguidas com a meta mínima. A semana atual ainda em andamento não quebra.
    def semana(dt):
        return (dt.date() - timedelta(days=dt.weekday()))

    contagem = {}
    for i in feitas:
        contagem[semana(i["quando"])] = contagem.get(semana(i["quando"]), 0) + 1
    esta = semana(agora)
    feitas_semana = contagem.get(esta, 0)
    ofensiva, s = (1 if feitas_semana >= META_SEMANAL else 0), esta - timedelta(days=7)
    while contagem.get(s, 0) >= META_SEMANAL:
        ofensiva += 1
        s -= timedelta(days=7)

    min_semana = sum(i["ms"] for i in feitas if semana(i["quando"]) == esta) // 60000
    min_hoje = sum(i["ms"] for i in feitas if i["quando"].date() == agora.date()) // 60000

    # Habilidades: cada aula é uma habilidade (por enquanto). Dominada = 100%; revisar = abaixo de 60%.
    dominadas = [i for i in feitas if i["nota"] >= 10]
    revisar = [i for i in feitas if i["nota"] < 6]
    erradas = [r for r in respostas if not r.correta]
    revisao_7d = [i for i in feitas if (agora - i["quando"]).days >= 7]

    return {
        "feitas": list(reversed(feitas)), "pendentes": pendentes, "proxima": pendentes[0] if pendentes else None,
        "media_geral": media(feitas), "media_recente": m_rec, "media_antiga": m_ant,
        "delta": round(m_rec - m_ant, 1) if m_rec is not None and m_ant is not None else None,
        "delta_abs": abs(round(m_rec - m_ant, 1)) if m_rec is not None and m_ant is not None else None,
        "por_materia": por_materia, "evolucao": evolucao,
        "ofensiva": ofensiva, "feitas_semana": feitas_semana, "meta_semanal": META_SEMANAL,
        "meta_bolinhas": [n < feitas_semana for n in range(META_SEMANAL)],
        "min_semana": min_semana, "min_hoje": min_hoje, "limite_diario": LIMITE_DIARIO_MIN,
        "pct_hoje": min(100, int(100 * min_hoje / LIMITE_DIARIO_MIN)),
        "dominadas": dominadas, "revisar": revisar, "n_erradas": len(erradas), "n_revisao": len(revisao_7d),
        "respostas": respostas,
    }


def _aluno_logado(request):
    from apps.turmas.models import Aluno

    return Aluno.objects.select_related("turma", "perfil", "usuario").filter(usuario=request.user).first()


from apps.contas.decorators import papel_requerido  # noqa: E402


@papel_requerido("aluno")
def painel_aluno(request):
    import json
    from datetime import timedelta

    from django.urls import reverse
    from django.utils import timezone

    aluno = _aluno_logado(request)
    if not aluno:
        return render(request, "prototipo/painel_aluno.html", {"sem_turma": True})
    perfil = getattr(aluno, "perfil", None)
    contexto = _dados_aluno(aluno)
    hoje = timezone.localtime()

    # Dados dos painéis interativos e do calendário (o JS monta os gráficos a partir daqui)
    def prazo(item):
        return (timezone.localtime(item["aula"].criada_em) + timedelta(days=PRAZO_DIAS)).date()

    eventos, minutos = [], {}
    for i in contexto["pendentes"]:
        p = prazo(i)
        i["prazo"] = p
        i["dias_para_prazo"] = (p - hoje.date()).days
        eventos.append({"data": p.isoformat(), "tipo": "prazo", "titulo": i["assunto"], "materia": i["materia"],
                        "detalhe": "Prazo da tarefa", "url": reverse("aulas:ver", args=[i["aula"].pk])})
    for i in contexto["feitas"]:
        d = i["quando"].date().isoformat()
        eventos.append({"data": d, "tipo": "feita", "titulo": i["assunto"], "materia": i["materia"],
                        "detalhe": f"{i['acertos']} de {i['total']} certas", "url": reverse("aulas:ver", args=[i["aula"].pk])})
        minutos[d] = minutos.get(d, 0) + i["ms"] // 60000
    notas = [{"materia": i["materia"], "assunto": i["assunto"], "nota": i["nota"], "data": i["quando"].date().isoformat()}
             for i in reversed(contexto["feitas"])]
    pendentes_js = [{"titulo": i["assunto"], "materia": i["materia"], "prazo": i["prazo"].isoformat(),
                     "url": reverse("aulas:ver", args=[i["aula"].pk])} for i in contexto["pendentes"]]
    feitas_js = [{"titulo": i["assunto"], "materia": i["materia"], "data": i["quando"].date().isoformat(),
                  "detalhe": f"{i['acertos']} de {i['total']} certas", "url": reverse("aulas:ver", args=[i["aula"].pk])}
                 for i in contexto["feitas"]]
    dados = {"hoje": hoje.date().isoformat(), "eventos": eventos, "minutos": minutos, "notas": notas,
             "pendentes": pendentes_js, "feitas": feitas_js, "limite": LIMITE_DIARIO_MIN, "meta": META_SEMANAL}

    contexto.update(aluno=aluno, perfil=perfil, apoios=perfil.nomes_apoios() if perfil else [],
                    foco=bool(perfil and perfil.foco), hoje=hoje, materias=sorted({n["materia"] for n in notas}),
                    dados_json=json.dumps(dados, ensure_ascii=False))
    return render(request, "prototipo/painel_aluno.html", contexto)


TREINOS = {
    "erros": ("Revisar o que errei", "As questões que você errou, uma de cada vez."),
    "rapido": ("Treino rápido", "3 questões, uns 3 minutos."),
    "revisao": ("Revisão da semana passada", "Para não esquecer o que já aprendeu."),
}


@papel_requerido("aluno")
def treino(request, tipo):
    import json
    import random

    from django.http import Http404

    if tipo not in TREINOS:
        raise Http404
    aluno = _aluno_logado(request)
    if not aluno:
        raise Http404
    dados = _dados_aluno(aluno)
    if tipo == "erros":
        questoes = [r.questao for r in dados["respostas"] if not r.correta]
    elif tipo == "revisao":
        from django.utils import timezone

        agora = timezone.localtime()
        ids = {i["aula"].pk for i in dados["feitas"] if (agora - i["quando"]).days >= 7}
        questoes = [r.questao for r in dados["respostas"] if r.questao.aula_id in ids]
        random.shuffle(questoes)
        questoes = questoes[:5]
    else:
        questoes = [r.questao for r in dados["respostas"]]
        random.shuffle(questoes)
        questoes = questoes[:3]
    itens = [{"enunciado": q.enunciado, "alternativas": q.alternativas, "correta": q.indice_correto,
              "assunto": _assunto(q.aula.titulo)} for q in questoes]
    perfil = getattr(aluno, "perfil", None)
    return render(request, "prototipo/treino.html", {
        "titulo": TREINOS[tipo][0], "descricao": TREINOS[tipo][1], "itens_json": json.dumps(itens, ensure_ascii=False),
        "n": len(itens), "foco": bool(perfil and perfil.foco), "aluno": aluno,
    })
