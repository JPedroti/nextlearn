"""Números do painel da turma, calculados na hora a partir das respostas e dos registros de uso reais."""

from collections import defaultdict

from django.db.models import Count

from apps.aulas.models import EventoUso, Resposta
from apps.perfis.models import PREFERENCIAS, Perfil, SugestaoPerfil


def porcentagem(parte, total):
    return round(100 * parte / total) if total else None


def placar(respostas):
    """{"acertos", "total", "pct"} de uma lista de respostas."""
    acertos = sum(1 for resposta in respostas if resposta.correta)
    return {"acertos": acertos, "total": len(respostas), "pct": porcentagem(acertos, len(respostas))}


def _perfil(aluno):
    try:
        return aluno.perfil
    except Perfil.DoesNotExist:
        return None


def montar_painel(turma):
    alunos = list(turma.alunos.select_related("usuario", "perfil"))
    aulas = list(turma.aulas.filter(publicada=True).prefetch_related("questoes"))
    respostas = list(Resposta.objects.filter(aluno__turma=turma).select_related("questao"))

    respostas_por_aluno = defaultdict(list)
    respostas_por_aula = defaultdict(list)
    respostas_por_questao = defaultdict(list)
    for resposta in respostas:
        respostas_por_aluno[resposta.aluno_id].append(resposta)
        respostas_por_aula[resposta.questao.aula_id].append(resposta)
        respostas_por_questao[resposta.questao_id].append(resposta)

    usos = {
        (linha["aluno_id"], linha["tipo"]): linha["vezes"]
        for linha in EventoUso.objects.filter(aluno__turma=turma)
        .values("aluno_id", "tipo")
        .annotate(vezes=Count("id"))
    }
    rotulos = {campo: Perfil._meta.get_field(campo).verbose_name for campo in PREFERENCIAS}

    linhas_alunos = []
    for aluno in alunos:
        suas = respostas_por_aluno[aluno.pk]
        perfil = _perfil(aluno)
        linhas_alunos.append({
            "aluno": aluno,
            "apoios": perfil.nomes_apoios() if perfil else [],
            "aulas_respondidas": len({r.questao.aula_id for r in suas}),
            "aulas_com_versao_adaptada": len({r.questao.aula_id for r in suas if r.versao_mascara}),
            "placar": placar(suas),
            "usos": [
                {"rotulo": rotulos[campo], "vezes": usos[(aluno.pk, f"ativou_{campo}")]}
                for campo in PREFERENCIAS
                if usos.get((aluno.pk, f"ativou_{campo}"))
            ],
        })

    linhas_aulas = []
    for aula in aulas:
        suas = respostas_por_aula[aula.pk]
        linhas_aulas.append({
            "aula": aula,
            "alunos_responderam": len({r.aluno_id for r in suas}),
            "placar": placar(suas),
            "placar_original": placar([r for r in suas if r.versao_mascara == 0]),
            "placar_adaptada": placar([r for r in suas if r.versao_mascara != 0]),
            "questoes": [
                {"questao": questao, "placar": placar(respostas_por_questao[questao.pk])}
                for questao in aula.questoes.all()
            ],
        })

    sugestoes = SugestaoPerfil.objects.filter(
        aluno__turma=turma, status=SugestaoPerfil.Status.PENDENTE
    ).select_related("aluno__usuario")

    return {
        "linhas_alunos": linhas_alunos,
        "linhas_aulas": linhas_aulas,
        "total_aulas": len(aulas),
        "total_alunos": len(alunos),
        "sugestoes": sugestoes,
    }
