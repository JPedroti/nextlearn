"""Métricas de eficácia dos apoios — calculadas a partir de respostas reais e feedback do professor.

Estas métricas alimentam o system prompt para que a IA ajuste sua abordagem com base
no que está funcionando ou não para cada perfil de aluno.
"""

from collections import defaultdict

from django.db.models import Avg, Count, Q

from apps.aulas.models import FeedbackVersao, Resposta, VersaoAdaptada
from apps.perfis.models import APOIOS, bits_da_mascara


def metricas_por_mascara():
    """Calcula eficácia de cada máscara (1-7) a partir das respostas dos alunos.

    Retorna dict: {mascara: {"acertos_pct": float|None, "total_questoes": int,
                              "nota_media": float|None, "num_feedbacks": int,
                              "apoios": [str]}}
    """
    metricas = {}
    for mascara in range(1, 8):
        foco, textual, concreto = bits_da_mascara(mascara)
        respostas = Resposta.objects.filter(versao_mascara=mascara)
        total = respostas.count()
        acertos = respostas.filter(correta=True).count() if total else 0

        # Nota média dos professores para versões com esta máscara
        notas = FeedbackVersao.objects.filter(versao__mascara=mascara).aggregate(
            media=Avg("nota"), total=Count("id"),
        )

        apoios = [nome for _, nome, _ in APOIOS if mascara & _]

        metricas[mascara] = {
            "acertos_pct": round(100 * acertos / total) if total else None,
            "total_questoes": total,
            "nota_media": round(notas["media"], 1) if notas["media"] else None,
            "num_feedbacks": notas["total"],
            "apoios": apoios,
        }
    return metricas


def resumo_eficacia_para_prompt(mascara):
    """Retorna uma string concisa (2-3 linhas) com as métricas da máscara para incluir no system prompt.

    Formato: "Perfil [apoios]: X% acertos em Y questões. Nota média dos professores: Z/5 (N avaliações)."
    """
    metricas = metricas_por_mascara().get(mascara, {})
    if not metricas or not metricas.get("total_questoes"):
        return None

    partes = [f"Perfil {', '.join(metricas['apoios'])}"]
    if metricas["acertos_pct"] is not None:
        partes.append(f"{metricas['acertos_pct']}% de acertos em {metricas['total_questoes']} questões respondidas")
    if metricas["nota_media"] is not None:
        partes.append(f"nota média dos professores: {metricas['nota_media']}/5 ({metricas['num_feedbacks']} avaliações)")

    linha = ". ".join(partes) + "."

    # Sugestão de ajuste com base nos dados
    if metricas["acertos_pct"] is not None and metricas["total_questoes"] >= 5:
        if metricas["acertos_pct"] >= 80:
            linha += " Este perfil está funcionando bem — mantenha a abordagem atual."
        elif metricas["acertos_pct"] < 50:
            linha += " Este perfil está com baixo desempenho — tente uma abordagem diferente, simplificando mais."

    return linha


def compilar_bloco_metricas():
    """Compila um resumo geral de todas as máscaras para incluir no system prompt como contexto de eficácia.

    Retorna string formatada ou None se não houver dados suficientes.
    """
    metricas = metricas_por_mascara()
    linhas = []
    for mascara, dados in sorted(metricas.items()):
        if dados["total_questoes"] >= 3:  # mínimo para ser significativo
            linha = resumo_eficacia_para_prompt(mascara)
            if linha:
                linhas.append(linha)

    if not linhas:
        return None

    return (
        "Dados de eficácia dos apoios (calculados a partir do uso real da plataforma):\n"
        + "\n".join(f"- {linha}" for linha in linhas)
    )