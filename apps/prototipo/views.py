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

    from django.conf import settings

    from .frases import status_ia
    from .perfis_dev import PERFIS_DEV

    perfil_dev = request.GET.get("perfil_dev", "") if settings.DEBUG else ""
    a, tema, intensidade = _apoios_visuais(perfil, perfil_dev)
    ambiente_dev = request.GET.get("ambiente", "") if settings.DEBUG else ""
    trilha = _trilha(contexto, aluno, a, intensidade, ambiente_dev)
    for u in trilha:
        for no in u["nos"]:
            if no["url"] == "treino:revisao":
                no["url"] = reverse("prototipo:treino", args=["revisao"])
    mundo_atual = next((u for u in trilha if u["atual"]), trilha[0] if trilha else None)
    cartoes = [dict(i, faixa=faixa_nota(i["nota"])) for i in contexto["feitas"]]  # mais recentes primeiro
    contexto.update(aluno=aluno, perfil=perfil, apoios=perfil.nomes_apoios() if perfil else [],
                    foco=a["foco"], textual=a["textual"], concreto=a["concreto"], limpo=a["limpo"], voz=a["voz"],
                    letras=a["letras"], alvos=a["alvos"], tema=tema, tema_nome=TEMAS_ALUNO[tema],
                    dev=settings.DEBUG, perfil_dev=perfil_dev, ambiente_dev=ambiente_dev, ambientes=AMBIENTES_LISTA(), perfis_dev=PERFIS_DEV, ia=status_ia(),
                    trilha=trilha, mundo_atual=mundo_atual, cartoes=cartoes,
                    faixas=[faixa_nota(n) for n in (10, 9, 7.5, 6, 3)],
                    hoje=hoje, materias=sorted({n["materia"] for n in notas}),
                    dados_json=json.dumps(dados, ensure_ascii=False))
    return render(request, "prototipo/painel_aluno.html", contexto)


# Escala de notas: vermelho → verde, SEMPRE com texto e forma junto (nunca só cor; daltonismo).
FAIXAS_NOTA = [  # (nota mínima, classe, rótulo, símbolo)
    (10, "g5", "Dominado!", "★"),
    (8.5, "g4", "Muito bom", "▲"),
    (7, "g3", "Bom", "●"),
    (5, "g2", "Quase lá", "◆"),
    (0, "g1", "Vamos revisar", "↺"),
]


def faixa_nota(nota):
    for minimo, classe, rotulo, simbolo in FAIXAS_NOTA:
        if nota >= minimo:
            return {"classe": classe, "rotulo": rotulo, "simbolo": simbolo}


# Tema visual por apoio (docs/design_neuro.md). Prioridade: limpo > foco+textual (brisa) > foco > textual > concreto > base.
TEMAS_ALUNO = {
    "base": "Aurora", "foco": "Oceano", "brisa": "Brisa", "textual": "Pergaminho", "concreto": "Parque", "limpo": "Limpo",
}


def _apoios_visuais(perfil, perfil_dev):
    """Apoios que valem na tela. Com a ferramenta do desenvolvedor, simula um perfil; senão, usa o do banco."""
    from .perfis_dev import POR_ID, intensidade_por_apoios

    a = {"foco": False, "textual": False, "concreto": False, "limpo": False, "voz": False, "letras": False, "alvos": False}
    dev = POR_ID.get(perfil_dev) if perfil_dev else None
    if dev and "apoios" in dev:
        a.update(dev["apoios"])
        a.update(dev.get("prefs", {}))
        return a, dev["tema"], dev["int"]
    if perfil:
        a.update(foco=perfil.foco, textual=perfil.textual, concreto=perfil.concreto, limpo=perfil.modo_limpo,
                 voz=perfil.leitura_voz, letras=perfil.fonte_dislexia)
    if a["limpo"]:
        tema = "limpo"
    elif a["foco"] and a["textual"]:
        tema = "brisa"
    else:
        tema = next((t for t in ("foco", "textual", "concreto") if a[t]), "base")
    return a, tema, intensidade_por_apoios(a)


ICONE_MATERIA = {"Matemática": "fracao", "Português": "livro", "Ciências": "gota"}
ROMANOS = ["", " II", " III", " IV", " V", " VI"]


def _trilha(contexto, aluno, apoios, intensidade, ambiente_forcado=""):
    """Trilha estilo jogo. Cada mundo (ambiente) tem no máximo 10 fases; depois começa outro mundo,
    mesmo que a matéria seja a mesma (Matemática → Matemática II). O cenário é gerado por ambiente + semente."""
    from .ambientes import AMBIENTES, FASES_POR_AMBIENTE, mapa

    foco = apoios["foco"]
    proxima = contexto["proxima"]
    por_materia = {}
    for i in sorted(contexto["feitas"], key=lambda x: x["quando"]):
        por_materia.setdefault(i["materia"], []).append(("feita", i))
    for i in contexto["pendentes"]:
        por_materia.setdefault(i["materia"], []).append(("nova", i))

    mundos, n_mundo = [], 0
    zigue = [0, 56, 84, 56, 0, -56, -84, -56]
    for materia in sorted(por_materia):
        itens = por_materia[materia]
        for k in range(0, len(itens), FASES_POR_AMBIENTE):
            bloco = itens[k:k + FASES_POR_AMBIENTE]
            parte = k // FASES_POR_AMBIENTE
            amb = AMBIENTES[(n_mundo + aluno.pk) % len(AMBIENTES)]
            n_mundo += 1
            nos, feitas_m = [], 0
            for estado, i in bloco:
                no = {"titulo": i["assunto"], "url": reverse_aula(i["aula"].pk), "icone": ICONE_MATERIA.get(materia, "estrela")}
                if estado == "feita":
                    feitas_m += 1
                    no.update(estado="feita", nota=i["nota"], estrelas=range(i["acertos"]), vazias=range(i["total"] - i["acertos"]),
                              faixa=faixa_nota(i["nota"]), detalhe=f"{i['acertos']} de {i['total']} certas")
                elif proxima and i["aula"].pk == proxima["aula"].pk:
                    no.update(estado="atual")
                else:
                    no.update(estado="bloqueada")
                nos.append(no)
                if estado == "feita" and feitas_m % 3 == 0:
                    nos.append({"estado": "revisao", "titulo": "Revisão", "url": "treino:revisao", "icone": "revisao"})
            n_ocultas, vistas = 0, 0
            for j, no in enumerate(nos):
                no["deslocamento"] = zigue[j % len(zigue)]
                if foco and no["estado"] == "bloqueada":
                    vistas += 1
                    if vistas > 2:
                        no["oculta"] = True
                        n_ocultas += 1
            atual = any(n["estado"] == "atual" for n in nos)
            if atual and ambiente_forcado:  # ferramenta do desenvolvedor: ver o mundo atual em outro ambiente
                amb = next((x for x in AMBIENTES if x["id"] == ambiente_forcado), amb)
            visiveis = [n for n in nos if not n.get("oculta")]
            m = mapa(amb["id"], f"{aluno.pk}-{materia}-{parte}", visiveis, intensidade)
            fase = 0
            for no, (x, y) in zip(visiveis, m["pos"]):
                no["x"], no["y"], no["lado"] = x, y, ("esq" if x > m["largura"] / 2 else "dir")
                if no["estado"] != "revisao":
                    fase += 1
                    no["fase"] = fase
            concluido = feitas_m == len(bloco)
            mundos.append({
                "materia": materia, "nome": materia + ROMANOS[min(parte, len(ROMANOS) - 1)], "numero": n_mundo,
                "nos": visiveis, "feitas": feitas_m, "total": len(bloco), "pct": int(100 * feitas_m / len(bloco)),
                "atual": atual, "concluido": concluido, "icone": ICONE_MATERIA.get(materia, "estrela"), "n_ocultas": n_ocultas,
                "mapa": m, "cenario": {"nome": amb["nome"], "escuro": m["escuro"]},
                "cor_a": amb["a"], "cor_c": amb["c"],
            })
    # Ordem: o mundo atual primeiro; com foco, só ele aberto
    mundos.sort(key=lambda m: (not m["atual"], m["concluido"], m["materia"], m["numero"]))
    for m in mundos:
        m["aberta"] = m["atual"] or not foco
    return mundos


def AMBIENTES_LISTA():
    from .ambientes import AMBIENTES

    return [(a["id"], a["nome"]) for a in AMBIENTES]


def reverse_aula(pk):
    from django.urls import reverse

    return reverse("aulas:ver", args=[pk])


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


def versao(request):
    """Ao vivo (só em DEBUG): devolve a data da última mudança nos arquivos do protótipo.
    O ao_vivo.js consulta isto e recarrega a página quando muda."""
    from pathlib import Path

    from django.conf import settings
    from django.http import Http404, JsonResponse

    if not settings.DEBUG:
        raise Http404
    base = Path(settings.BASE_DIR)
    maior = 0.0
    for pasta in ("templates/prototipo", "static/prototipo", "apps/prototipo"):
        for arq in (base / pasta).rglob("*"):
            if arq.is_file() and arq.suffix in (".html", ".css", ".js", ".py"):
                maior = max(maior, arq.stat().st_mtime)
    return JsonResponse({"v": maior})


@papel_requerido("aluno")
def fala(request):
    """Fala do Next para a fase atual. A API recebe só assunto da aula e apoios, sem dados de desempenho."""
    from django.conf import settings
    from django.http import JsonResponse

    from .frases import fala_do_next

    aluno = _aluno_logado(request)
    if not aluno:
        return JsonResponse({"fala": "Oi! Eu sou o Next.", "origem": "reserva"})
    perfil = getattr(aluno, "perfil", None)
    perfil_dev = request.GET.get("perfil_dev", "") if settings.DEBUG else ""
    a, _, _ = _apoios_visuais(perfil, perfil_dev)
    dados_aluno = _dados_aluno(aluno)
    proxima = dados_aluno["proxima"]
    contexto = {
        "materia": proxima["materia"] if proxima else "",
        "assunto": proxima["assunto"] if proxima else "",
    }
    texto, origem = fala_do_next(
        aluno.pk, contexto, {k: a[k] for k in ("foco", "textual", "concreto")},
        nome=aluno.usuario.first_name,
    )
    return JsonResponse({"fala": texto, "origem": origem})


# ---------------------------------------------------------------------------
# Progresso do aluno ao longo do tempo (métricas de docs/METRICAS_ENSINO.md e docs/PERFIS_E_METRICAS.md)
# Tudo sai das respostas guardadas no banco (Resposta: acerto, tempo e data de cada questão, de cada aluno).
# ---------------------------------------------------------------------------
def _grafico_linha(valores, rotulos, maximo=None, sufixo="", altura=150, cor="var(--destaque)"):
    """SVG simples de linha com pontos e rótulos (sem biblioteca)."""
    W, H, m = 520, altura, 28
    vals = [v for v in valores if v is not None]
    if not vals:
        return '<p class="mini">Ainda sem dados.</p>'
    top = maximo or max(vals) or 1
    n = len(valores)
    xs = [m + (W - 2 * m) * (i / max(1, n - 1)) for i in range(n)]
    pts = [(x, H - m - (H - 2 * m) * (v / top)) for x, v in zip(xs, valores) if v is not None]
    linha = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    area = f"M{pts[0][0]:.0f},{H - m} L" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + f" L{pts[-1][0]:.0f},{H - m}Z"
    s = [f'<svg class="graf" viewBox="0 0 {W} {H}" role="img" aria-label="' + ", ".join(f"{r}: {v if v is not None else '-'}{sufixo}" for r, v in zip(rotulos, valores)) + '">',
         f'<line x1="{m}" y1="{H - m}" x2="{W - m}" y2="{H - m}" stroke="var(--borda)" stroke-width="2"/>',
         f'<path d="{area}" fill="{cor}" opacity=".12"/><polyline points="{linha}" fill="none" stroke="{cor}" stroke-width="3" stroke-linejoin="round"/>']
    for (x, y), v in zip(pts, vals):
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="#FFFFFF" stroke="{cor}" stroke-width="3"/><text x="{x:.0f}" y="{y - 10:.0f}" text-anchor="middle" class="graf-v">{v:g}{sufixo}</text>')
    for x, r in zip(xs, rotulos):
        s.append(f'<text x="{x:.0f}" y="{H - 8}" text-anchor="middle" class="graf-r">{r}</text>')
    return "".join(s) + "</svg>"


def _grafico_barras(valores, rotulos, sufixo="", altura=150, cor="#0F9D6E", linha=None):
    W, H, m = 520, altura, 28
    top = max([v for v in valores] + [linha or 0, 1])
    n = len(valores)
    larg = (W - 2 * m) / max(1, n)
    s = [f'<svg class="graf" viewBox="0 0 {W} {H}" role="img" aria-label="' + ", ".join(f"{r}: {v}{sufixo}" for r, v in zip(rotulos, valores)) + '">']
    if linha:
        y = H - m - (H - 2 * m) * linha / top
        s.append(f'<line x1="{m}" y1="{y:.0f}" x2="{W - m}" y2="{y:.0f}" stroke="{cor}" stroke-dasharray="6 6" opacity=".6"/>')
    for i, (v, r) in enumerate(zip(valores, rotulos)):
        h = (H - 2 * m) * v / top
        x = m + i * larg + larg * .18
        s.append(f'<rect x="{x:.0f}" y="{H - m - h:.0f}" width="{larg * .64:.0f}" height="{max(2, h):.0f}" rx="5" fill="{cor}"/>')
        s.append(f'<text x="{x + larg * .32:.0f}" y="{H - m - h - 6:.0f}" text-anchor="middle" class="graf-v">{v:g}{sufixo}</text>')
        s.append(f'<text x="{x + larg * .32:.0f}" y="{H - 8}" text-anchor="middle" class="graf-r">{r}</text>')
    return "".join(s) + "</svg>"


@papel_requerido("aluno")
def progresso(request):
    import statistics
    from datetime import timedelta

    from django.conf import settings
    from django.utils import timezone

    from apps.aulas.models import Resposta

    aluno = _aluno_logado(request)
    if not aluno:
        return render(request, "prototipo/painel_aluno.html", {"sem_turma": True})
    perfil = getattr(aluno, "perfil", None)
    perfil_dev = request.GET.get("perfil_dev", "") if settings.DEBUG else ""
    a, tema, _ = _apoios_visuais(perfil, perfil_dev)
    hoje = timezone.localtime()
    resp = list(Resposta.objects.filter(aluno=aluno).select_related("questao__aula").order_by("criado_em", "questao__ordem"))

    def seg(dt):
        d = timezone.localtime(dt).date()
        return d - timedelta(days=d.weekday())

    semana_atual = hoje.date() - timedelta(days=hoje.weekday())
    semanas = [semana_atual - timedelta(days=7 * k) for k in range(9, -1, -1)]   # últimas 10 semanas
    rot = [s.strftime("%d/%m") for s in semanas]
    por_sem = {s: [] for s in semanas}
    sessoes = {}
    for r in resp:
        s = seg(r.criado_em)
        if s in por_sem:
            por_sem[s].append(r)
        sessoes.setdefault(r.questao.aula_id, []).append(r)

    acerto = [round(100 * sum(r.correta for r in por_sem[s]) / len(por_sem[s])) if por_sem[s] else None for s in semanas]
    minutos, n_sessoes = [], []
    for s in semanas:
        aulas = {r.questao.aula_id: (r.tempo_ms or 0) for r in por_sem[s]}
        minutos.append(sum(aulas.values()) // 60000)
        n_sessoes.append(len(aulas))
    # Métrica-norte: assuntos dominados (100%) acumulados por semana
    dominio = {}
    for aula_id, rs in sessoes.items():
        if all(r.correta for r in rs):
            dominio[aula_id] = seg(rs[0].criado_em)
    dominadas = [sum(1 for d in dominio.values() if d <= s) for s in semanas]
    # Ofensiva semanal (meta mínima de 2 aulas)
    metas = [n >= META_SEMANAL for n in n_sessoes]
    # Estado do aluno (ciclo semanal, versão escolar dos estados do Duolingo)
    ultima = timezone.localtime(resp[-1].criado_em) if resp else None
    dias = (hoje - ultima).days if ultima else None
    estado = "Ativo na semana" if dias is not None and dias < 7 else ("Em risco (7+ dias sem estudar)" if dias is not None and dias < 14 else "Dormente (14+ dias)")
    # P3: queda de acerto ao longo da sessão (acerto por posição da questão)
    pos = {}
    for rs in sessoes.values():
        for r in rs:
            pos.setdefault(r.questao.ordem, []).append(r.correta)
    acerto_pos = [round(100 * sum(v) / len(v)) for _, v in sorted(pos.items())]
    # P3: variabilidade do tempo entre sessões (coeficiente de variação) — só para ajustar pausas, não diagnostica
    tempos = [rs[0].tempo_ms / 60000 for rs in sessoes.values() if rs[0].tempo_ms]
    cv = round(100 * statistics.pstdev(tempos) / statistics.mean(tempos)) if len(tempos) > 2 else None
    # Erros consecutivos (3 seguidos na mesma matéria → mudar a estratégia)
    seq, alertas = {}, 0
    for r in resp:
        mat = _materia(r.questao.aula.titulo)
        seq[mat] = 0 if r.correta else seq.get(mat, 0) + 1
        if seq[mat] == 3:
            alertas += 1
    # Média por matéria ao longo do tempo (sessões em ordem)
    por_materia = {}
    for aula_id, rs in sorted(sessoes.items(), key=lambda kv: kv[1][0].criado_em):
        mat = _materia(rs[0].questao.aula.titulo)
        por_materia.setdefault(mat, []).append(round(10 * sum(r.correta for r in rs) / len(rs), 1))

    cartoes = [
        {"titulo": "Assuntos dominados (acumulado)", "valor": dominadas[-1], "unid": "assuntos", "tema": "notas",
         "graf": _grafico_linha(dominadas, rot, cor="#1E7B4A"),
         "porque": "Métrica-norte: aprendizagem que fica, não tempo de tela. Dominado = 100% de acerto no assunto (meta do estudo: domínio ≥ 0,95).",
         "fonte": "METRICAS_ENSINO §3 · adaptado de Duolingo/HLR"},
        {"titulo": "Acerto por semana", "valor": f"{next((v for v in reversed(acerto) if v is not None), '–')}%", "unid": "na última semana com aula", "tema": "notas",
         "graf": _grafico_linha(acerto, rot, maximo=100, sufixo="%"),
         "porque": "Comparar o aluno com ele mesmo. Zona-alvo de prática: acertar a maioria sem ser fácil demais.",
         "fonte": "METRICAS_ENSINO camada C"},
        {"titulo": "Minutos e aulas por semana", "valor": minutos[-1], "unid": "min nesta semana", "tema": "tempo",
         "graf": _grafico_barras(minutos, rot, linha=None),
         "porque": "Hábito, sem premiar tempo de uso. O limite diário é combinado com a família (ECA Digital).",
         "fonte": "METRICAS_ENSINO camadas D e E"},
        {"titulo": "Queda de acerto ao longo da aula", "valor": f"{acerto_pos[0] if acerto_pos else '–'}% → {acerto_pos[-1] if acerto_pos else '–'}%", "unid": "1ª questão → última", "tema": "foco",
         "graf": _grafico_barras(acerto_pos, [f"{i + 1}ª" for i in range(len(acerto_pos))], sufixo="%", cor="#35557F"),
         "porque": "Para quem tem apoio de foco: se o acerto cai no fim, a aula deve ser mais curta ou ter pausa.",
         "fonte": "PERFIS_E_METRICAS P3 · [PRODUTO]"},
    ]
    contexto = {
        "aluno": aluno, "perfil": perfil, "tema": tema, "foco": a["foco"], "textual": a["textual"], "concreto": a["concreto"],
        "limpo": a["limpo"], "voz": a["voz"], "letras": a["letras"], "perfil_dev": perfil_dev, "dev": settings.DEBUG,
        "cartoes": cartoes, "metas": list(zip(rot, metas, n_sessoes)), "estado": estado, "dias": dias, "cv": cv,
        "alertas": alertas, "por_materia": [(m, _grafico_linha(v, [str(i + 1) for i in range(len(v))], maximo=10)) for m, v in sorted(por_materia.items())],
        "n_respostas": len(resp), "n_sessoes": len(sessoes), "hoje": hoje,
    }
    return render(request, "prototipo/progresso.html", contexto)


def comparar(request):
    """Ferramenta do desenvolvedor: dois perfis lado a lado (iframes da área do aluno). Só com DEBUG."""
    from django.conf import settings
    from django.http import Http404

    from .ambientes import AMBIENTES
    from .perfis_dev import PERFIS_DEV

    if not settings.DEBUG:
        raise Http404
    pagina = request.GET.get("pagina", "inicio")
    return render(request, "prototipo/comparar.html", {
        "a": request.GET.get("a", "tdah"), "b": request.GET.get("b", "tea"), "amb": request.GET.get("ambiente", ""),
        "pagina": pagina if pagina in ("inicio", "progresso") else "inicio",
        "perfis": [p for p in PERFIS_DEV if p["id"]], "ambientes": [(x["id"], x["nome"]) for x in AMBIENTES],
    })
