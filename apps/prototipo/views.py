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


from django.views.decorators.clickjacking import xframe_options_sameorigin  # noqa: E402

from apps.contas.decorators import papel_requerido  # noqa: E402


@xframe_options_sameorigin
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
    cartoes = [dict(i, faixa=faixa_nota(i["nota"]), pizza=_pizza(i["acertos"], i["total"], faixa_nota(i["nota"])["classe"])) for i in contexto["feitas"]]
    modo = modo_da_tela(a, perfil_dev)
    tres = sum(1 for i in contexto["feitas"] if i["acertos"] == i["total"])
    desafios = [
        {"nome": "Mestre das 3 estrelas", "desc": "Tire 3 estrelas em 5 fases", "feito": min(tres, 5), "meta": 5},
        {"nome": "Explorador", "desc": "Complete um mundo inteiro (10 fases)", "feito": max((u["feitas"] for u in trilha), default=0), "meta": 10},
        {"nome": "Memória de elefante", "desc": "Faça 3 revisões", "feito": 0, "meta": 3},
    ]
    for dsf in desafios:
        dsf["pct"] = int(100 * dsf["feito"] / dsf["meta"])
    contexto.update(aluno=aluno, perfil=perfil, apoios=perfil.nomes_apoios() if perfil else [],
                    modo=modo, modo_nome=MODO_NOME[modo], desafios=desafios,
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


# "Cara" da plataforma por perfil: muda a ESTRUTURA da página, não só as cores.
MODO_DEV = {"nenhum": "padrao", "tdah": "missao", "tea": "agenda", "tea_tdah": "agenda", "dislexia": "leitura",
            "discalculia": "visual", "tdl": "leitura", "di": "missao", "tdc": "padrao", "ah": "desafio", "limpo": "limpo"}
MODO_NOME = {"padrao": "Trilha completa", "missao": "Modo missão (uma coisa por vez)", "agenda": "Modo agenda (previsível)",
             "leitura": "Modo leitura (ouvir e ler fácil)", "visual": "Modo visual (números em figuras)",
             "desafio": "Modo desafio (painel completo)", "limpo": "Modo limpo"}


def modo_da_tela(apoios, perfil_dev):
    if perfil_dev in MODO_DEV:
        return MODO_DEV[perfil_dev]
    if apoios["limpo"]:
        return "limpo"
    if apoios["foco"] and apoios["textual"]:
        return "agenda"
    if apoios["foco"]:
        return "missao"
    if apoios["textual"]:
        return "leitura"
    if apoios["concreto"]:
        return "visual"
    return "padrao"


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


def _pizza(acertos, total, classe):
    """Figura de pizza (acertos/total) para o modo visual: número vira quantidade que se vê."""
    import math

    if not total:
        return ""
    fatias = []
    for k in range(total):
        a0, a1 = 2 * math.pi * k / total - math.pi / 2, 2 * math.pi * (k + 1) / total - math.pi / 2
        x0, y0, x1, y1 = 20 + 18 * math.cos(a0), 20 + 18 * math.sin(a0), 20 + 18 * math.cos(a1), 20 + 18 * math.sin(a1)
        cor = "var(--cor)" if k < acertos else "#FFFFFF"
        fatias.append(f'<path d="M20 20 L{x0:.1f} {y0:.1f} A18 18 0 0 1 {x1:.1f} {y1:.1f}Z" fill="{cor}" stroke="var(--tom)" stroke-width="1.5"/>')
    return f'<svg class="pizza" viewBox="0 0 40 40" role="img" aria-label="{acertos} de {total} certas">' + "".join(fatias) + "</svg>"


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
def _fmt(v):
    return str(round(v, 1)).replace(".", ",").removesuffix(",0")


def _grafico_linha(valores, rotulos, maximo=None, sufixo="", altura=190, cor="#4F46E5", id_="g", degrau=False):
    """Linha com área em degradê, grade, eixo e pontos com dica ao passar o mouse (SVG puro)."""
    W, H, ml, mr, mt, mb = 560, altura, 40, 16, 16, 30
    vals = [v for v in valores if v is not None]
    if not vals:
        return '<p class="vazio">Ainda sem dados suficientes.</p>'
    top = maximo or (max(vals) * 1.15 or 1)
    n = len(valores)
    X = lambda i: ml + (W - ml - mr) * (i / max(1, n - 1))  # noqa: E731
    Y = lambda v: mt + (H - mt - mb) * (1 - v / top)         # noqa: E731
    pts = [(X(i), Y(v), v, r) for i, (v, r) in enumerate(zip(valores, rotulos)) if v is not None]
    if degrau:
        d = f"M{pts[0][0]:.0f},{pts[0][1]:.0f}" + "".join(f" H{x:.0f} V{y:.0f}" for x, y, _, _ in pts[1:])
    else:
        d = f"M{pts[0][0]:.0f},{pts[0][1]:.0f}" + "".join(f" L{x:.0f},{y:.0f}" for x, y, _, _ in pts[1:])
    area = d + f" V{H - mb} H{pts[0][0]:.0f}Z"
    s = [f'<svg class="graf" viewBox="0 0 {W} {H}" role="img" aria-label="' + "; ".join(f"{r}: {_fmt(v)}{sufixo}" for _, _, v, r in pts) + '">',
         f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cor}" stop-opacity=".28"/><stop offset="1" stop-color="{cor}" stop-opacity="0"/></linearGradient></defs>']
    for k in range(5):
        v = top * k / 4
        y = Y(v)
        s.append(f'<line x1="{ml}" y1="{y:.0f}" x2="{W - mr}" y2="{y:.0f}" class="grade"/><text x="{ml - 8}" y="{y + 4:.0f}" text-anchor="end" class="graf-r">{_fmt(v)}{sufixo}</text>')
    s.append(f'<path d="{area}" fill="url(#{id_})"/><path d="{d}" fill="none" stroke="{cor}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
    passo_rot = max(1, n // 6)
    for i, r in enumerate(rotulos):
        if i % passo_rot == 0 or i == n - 1:
            s.append(f'<text x="{X(i):.0f}" y="{H - 8}" text-anchor="middle" class="graf-r">{r}</text>')
    for x, y, v, r in pts:
        s.append(f'<g class="pt" tabindex="0"><circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="transparent"/><circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="#FFFFFF" stroke="{cor}" stroke-width="3"/>'
                 f'<g class="dica"><rect x="{x - 44:.0f}" y="{y - 40:.0f}" width="88" height="26" rx="8"/><text x="{x:.0f}" y="{y - 22:.0f}" text-anchor="middle">{r}: {_fmt(v)}{sufixo}</text></g></g>')
    return "".join(s) + "</svg>"


def _grafico_barras(valores, rotulos, sufixo="", altura=190, cor="#0F9D6E", linha=None, rot_linha=""):
    W, H, ml, mr, mt, mb = 560, altura, 40, 16, 16, 30
    top = max([v for v in valores] + [linha or 0, 1]) * 1.15
    n = len(valores)
    larg = (W - ml - mr) / max(1, n)
    Y = lambda v: mt + (H - mt - mb) * (1 - v / top)  # noqa: E731
    s = [f'<svg class="graf" viewBox="0 0 {W} {H}" role="img" aria-label="' + "; ".join(f"{r}: {_fmt(v)}{sufixo}" for r, v in zip(rotulos, valores)) + '">']
    for k in range(5):
        v = top * k / 4
        s.append(f'<line x1="{ml}" y1="{Y(v):.0f}" x2="{W - mr}" y2="{Y(v):.0f}" class="grade"/><text x="{ml - 8}" y="{Y(v) + 4:.0f}" text-anchor="end" class="graf-r">{_fmt(v)}</text>')
    if linha:
        s.append(f'<line x1="{ml}" y1="{Y(linha):.0f}" x2="{W - mr}" y2="{Y(linha):.0f}" stroke="#B45309" stroke-dasharray="6 5" stroke-width="2"/><text x="{W - mr}" y="{Y(linha) - 6:.0f}" text-anchor="end" class="graf-r forte">{rot_linha}</text>')
    for i, (v, r) in enumerate(zip(valores, rotulos)):
        x = ml + i * larg + larg * .2
        s.append(f'<g class="pt" tabindex="0"><rect x="{x:.0f}" y="{Y(v):.0f}" width="{larg * .6:.0f}" height="{max(2, H - mb - Y(v)):.0f}" rx="6" fill="{cor}"/>'
                 f'<g class="dica"><rect x="{x + larg * .3 - 44:.0f}" y="{Y(v) - 34:.0f}" width="88" height="26" rx="8"/><text x="{x + larg * .3:.0f}" y="{Y(v) - 16:.0f}" text-anchor="middle">{r}: {_fmt(v)}{sufixo}</text></g></g>')
        s.append(f'<text x="{x + larg * .3:.0f}" y="{H - 8}" text-anchor="middle" class="graf-r">{r}</text>')
    return "".join(s) + "</svg>"


def _sparkline(valores, cor="#4F46E5"):
    vals = [v for v in valores if v is not None]
    if len(vals) < 2:
        return ""
    W, H = 120, 34
    top, base = max(vals), min(vals)
    rng = (top - base) or 1
    pts = [(W * i / (len(vals) - 1), H - 4 - (H - 8) * (v - base) / rng) for i, v in enumerate(vals)]
    return (f'<svg class="spark" viewBox="0 0 {W} {H}" aria-hidden="true"><polyline points="' + " ".join(f"{x:.0f},{y:.0f}" for x, y in pts) +
            f'" fill="none" stroke="{cor}" stroke-width="2.5" stroke-linejoin="round"/><circle cx="{pts[-1][0]:.0f}" cy="{pts[-1][1]:.0f}" r="3.5" fill="{cor}"/></svg>')


@xframe_options_sameorigin
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
    modo = modo_da_tela(a, perfil_dev)
    hoje = timezone.localtime()
    resp = list(Resposta.objects.filter(aluno=aluno).select_related("questao__aula").order_by("criado_em", "questao__ordem"))

    def seg(dt):
        d = timezone.localtime(dt).date()
        return d - timedelta(days=d.weekday())

    semana_atual = hoje.date() - timedelta(days=hoje.weekday())
    semanas = [semana_atual - timedelta(days=7 * k) for k in range(9, -1, -1)]
    rot = [s.strftime("%d/%m") for s in semanas]
    por_sem = {s: [] for s in semanas}
    sessoes, min_dia = {}, {}
    for r in resp:
        s = seg(r.criado_em)
        if s in por_sem:
            por_sem[s].append(r)
        sessoes.setdefault(r.questao.aula_id, []).append(r)
    for rs in sessoes.values():
        dia = timezone.localtime(rs[0].criado_em).date()
        min_dia[dia] = min_dia.get(dia, 0) + (rs[0].tempo_ms or 0) // 60000

    acerto = [round(100 * sum(r.correta for r in por_sem[s]) / len(por_sem[s])) if por_sem[s] else None for s in semanas]
    minutos, n_sessoes = [], []
    for s in semanas:
        aulas = {r.questao.aula_id: (r.tempo_ms or 0) for r in por_sem[s]}
        minutos.append(sum(aulas.values()) // 60000)
        n_sessoes.append(len(aulas))
    dominio = {}
    for aula_id, rs in sessoes.items():
        if all(r.correta for r in rs):
            dominio[aula_id] = seg(rs[0].criado_em)
    dominadas = [sum(1 for d in dominio.values() if d <= s) for s in semanas]
    metas = [n >= META_SEMANAL for n in n_sessoes]
    ofensiva = 0
    for ok in reversed(metas[:-1] if not metas[-1] else metas):
        if not ok:
            break
        ofensiva += 1

    def media(lst):
        lst = [v for v in lst if v is not None]
        return round(sum(lst) / len(lst)) if lst else None

    rec, ant = [v for v in acerto[-4:] if v is not None], [v for v in acerto[-8:-4] if v is not None]
    acerto_rec, acerto_ant = media(rec), media(ant)
    # Painel de especialistas: só mostrar variação quando há aulas suficientes nos dois períodos (evita ruído)
    delta = (acerto_rec - acerto_ant) if len(rec) >= 3 and len(ant) >= 3 else None

    ultima = timezone.localtime(resp[-1].criado_em) if resp else None
    dias = (hoje - ultima).days if ultima else None
    if dias is None:
        estado, estado_cls = "Ainda não começou", "neutro"
    elif dias < 7:
        estado, estado_cls = "Estudando com regularidade", "ok"
    elif dias < 14:
        estado, estado_cls = f"Sem estudar há {dias} dias", "atencao"
    else:
        estado, estado_cls = f"Sem estudar há {dias} dias", "alerta"

    pos = {}
    for rs in sessoes.values():
        for r in rs:
            pos.setdefault(r.questao.ordem, []).append(r.correta)
    acerto_pos = [round(100 * sum(v) / len(v)) for _, v in sorted(pos.items())]
    tempos = [rs[0].tempo_ms / 60000 for rs in sessoes.values() if rs[0].tempo_ms]
    cv = round(100 * statistics.pstdev(tempos) / statistics.mean(tempos)) if len(tempos) > 4 else None
    seq, alertas = {}, 0
    for r in resp:
        mat = _materia(r.questao.aula.titulo)
        seq[mat] = 0 if r.correta else seq.get(mat, 0) + 1
        if seq[mat] == 3:
            alertas += 1
    por_materia = {}
    for aula_id, rs in sorted(sessoes.items(), key=lambda kv: kv[1][0].criado_em):
        mat = _materia(rs[0].questao.aula.titulo)
        por_materia.setdefault(mat, []).append(round(10 * sum(r.correta for r in rs) / len(rs), 1))

    # Mapa de calor: 10 semanas x 7 dias (minutos por dia)
    calor = []
    for s in semanas:
        linha = []
        for k in range(7):
            d = s + timedelta(days=k)
            m = min_dia.get(d, 0)
            nivel = 0 if not m else (1 if m < 9 else (2 if m < 12 else 3))
            linha.append({"data": d.strftime("%d/%m"), "min": m, "nivel": nivel, "futuro": d > hoje.date()})
        calor.append({"rot": s.strftime("%d/%m"), "dias": linha})

    nome = aluno.usuario.first_name
    melhor = max(por_materia.items(), key=lambda kv: sum(kv[1][-3:]) / len(kv[1][-3:]))[0] if por_materia else None
    atencao = min(por_materia.items(), key=lambda kv: sum(kv[1][-3:]) / len(kv[1][-3:]))[0] if por_materia else None
    resumo = []
    if acerto_rec is not None:
        resumo.append(f"Nas últimas 4 semanas, {nome} acertou em média {acerto_rec}% das questões"
                      + (f" ({'+' if delta >= 0 else ''}{delta} pontos em relação às 4 semanas anteriores)." if delta is not None else "."))
    if melhor:
        resumo.append(f"Onde vai melhor agora: {melhor}. Onde vale um reforço em casa: {atencao}.")
    resumo.append(f"Cumpriu a meta combinada (2 aulas por semana) em {sum(metas)} das últimas 10 semanas.")

    sinais = [
        {"nome": "Regularidade", "cls": estado_cls, "txt": estado},
        {"nome": "3 erros seguidos na mesma matéria", "cls": "atencao" if alertas else "ok",
         "txt": f"{alertas} vez{'es' if alertas != 1 else ''}" + (" — vale mudar a estratégia (exemplo resolvido, pré-requisito)" if alertas else " — sem sinal")},
        {"nome": "Regularidade do tempo de aula", "cls": "neutro", "txt": (f"variação de {cv}% entre aulas" if cv is not None else "poucos dados")
         + ". Indicativo para pausas; não é diagnóstico (Kofler et al., 2013)."},
        {"nome": "Queda de acerto dentro da aula", "cls": "atencao" if acerto_pos and acerto_pos[0] - acerto_pos[-1] >= 30 else "ok",
         "txt": (f"{acerto_pos[0]}% na 1ª questão → {acerto_pos[-1]}% na última" if acerto_pos else "poucos dados")
         + ". Pode ser cansaço ou questões mais difíceis no fim: confira a ordem antes de concluir."},
    ]
    kpis = [
        {"rot": "Assuntos dominados", "val": dominadas[-1], "sub": "provisório: confirmar na revisão de 7 dias", "spark": _sparkline(dominadas, "#1E7B4A"), "cor": "verde"},
        {"rot": "Acerto (4 semanas)", "val": f"{acerto_rec}%" if acerto_rec is not None else "–",
         "sub": (f"{'▲' if delta >= 0 else '▼'} {abs(delta)} pontos vs. 4 semanas antes" if delta is not None else "precisa de mais aulas para comparar"), "spark": _sparkline(acerto, "#4F46E5"), "cor": "roxo"},
        {"rot": "Tempo por semana", "val": f"{round(sum(minutos[-4:]) / 4)} min", "sub": "média das 4 últimas semanas", "spark": _sparkline(minutos, "#0F9D6E"), "cor": "verde2"},
        {"rot": "Ofensiva semanal", "val": f"{ofensiva} sem.", "sub": "semanas seguidas com a meta combinada", "spark": "", "cor": "laranja"},
    ]
    contexto = {
        "aluno": aluno, "perfil": perfil, "tema": tema, "modo": modo, "foco": a["foco"], "textual": a["textual"], "concreto": a["concreto"],
        "limpo": a["limpo"], "voz": a["voz"], "letras": a["letras"], "perfil_dev": perfil_dev, "dev": settings.DEBUG,
        "kpis": kpis, "resumo": resumo, "sinais": sinais, "calor": calor, "dias_semana": ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"],
        "g_acerto": _grafico_linha(acerto, rot, maximo=100, sufixo="%", cor="#4F46E5", id_="ga"),
        "g_dominio": _grafico_linha(dominadas, rot, cor="#1E7B4A", id_="gd", degrau=True),
        "g_tempo": _grafico_barras(minutos, rot, cor="#10B981", linha=None),
        "g_pos": _grafico_barras(acerto_pos, [f"{i + 1}ª questão" for i in range(len(acerto_pos))], sufixo="%", cor="#6366F1"),
        "metas": list(zip(rot, metas, n_sessoes)),
        "por_materia": [(m, _grafico_linha(v, [f"aula {i + 1}" for i in range(len(v))], maximo=10, cor="#0EA5E9", id_=f"gm{k}"),
                         _fmt(sum(v[-3:]) / len(v[-3:]))) for k, (m, v) in enumerate(sorted(por_materia.items()))],
        "n_respostas": len(resp), "n_sessoes": len(sessoes), "hoje": hoje, "periodo": f"{rot[0]} a {hoje.strftime('%d/%m')}",
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


@papel_requerido("aluno")
def chat(request):
    """Chat do Next (POST). Guarda só as últimas mensagens na sessão do próprio aluno."""
    import json as _json

    from django.conf import settings
    from django.http import JsonResponse

    from .chat import HISTORICO, responder
    from .frases import chamar_chat

    if request.method != "POST":
        return JsonResponse({"erro": "use POST"}, status=405)
    aluno = _aluno_logado(request)
    if not aluno:
        return JsonResponse({"resposta": "Seu usuário ainda não está numa turma.", "origem": "erro"})
    try:
        pergunta = _json.loads(request.body or b"{}").get("pergunta", "")
    except ValueError:
        pergunta = ""
    perfil = getattr(aluno, "perfil", None)
    perfil_dev = request.GET.get("perfil_dev", "") if settings.DEBUG else ""
    a, _, _ = _apoios_visuais(perfil, perfil_dev)
    d = _dados_aluno(aluno)
    contexto = {"fase_atual": d["proxima"]["assunto"] if d["proxima"] else None,
                "materia": d["proxima"]["materia"] if d["proxima"] else None,
                "aulas_feitas": len(d["feitas"]), "ofensiva_semanas": d["ofensiva"]}
    historico = request.session.get("chat_next", [])
    resposta, origem = responder(aluno.pk, pergunta, historico, contexto,
                                 {k: a[k] for k in ("foco", "textual", "concreto")}, chamar_chat)
    historico = (historico + [{"role": "user", "content": pergunta[:400]}, {"role": "assistant", "content": resposta}])[-HISTORICO:]
    request.session["chat_next"] = historico
    return JsonResponse({"resposta": resposta, "origem": origem})
