"""Detecta padrões de erro nas respostas do aluno e gera sugestões automáticas para o professor.

Cada padrão detectado vira uma SugestaoPerfil com origem PADRAO_ERRO, que aparece
na fila de sugestões do painel do professor. O professor decide se aceita ou recusa.
"""

from collections import defaultdict
from datetime import datetime

from apps.aulas.models import Resposta

from .models import Perfil, SugestaoPerfil


def detectar_padroes(aluno):
    """Analisa as respostas do aluno e retorna uma lista de dicionários {campo, valor, motivo}.

    Chamado após o aluno enviar respostas de uma aula (no fluxo da view). As sugestões
    são criadas como SugestaoPerfil pendentes para o professor revisar.
    """
    respostas = list(
        Resposta.objects.filter(aluno=aluno)
        .select_related("questao__aula")
        .order_by("questao__ordem")
    )
    if len(respostas) < 3:
        return []  # poucas respostas para detectar padrão

    sugestoes = []
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)

    # Padrão 1: acertos caem ao longo da aula → sugere foco
    if len(respostas) >= 5:
        primeira_metade = respostas[: len(respostas) // 2]
        segunda_metade = respostas[len(respostas) // 2 :]
        pct_inicio = sum(1 for r in primeira_metade if r.correta) / len(primeira_metade)
        pct_fim = sum(1 for r in segunda_metade if r.correta) / len(segunda_metade)

        if pct_inicio >= 0.7 and pct_fim <= 0.4 and not perfil.foco:
            sugestoes.append({
                "campo": "foco",
                "valor": True,
                "motivo": (
                    f"Acertos caíram de {pct_inicio:.0%} no início para {pct_fim:.0%} no final da aula. "
                    "A atenção pode estar se esgotando ao longo da sessão. "
                    "Sugestão: ativar Atenção e foco (passos curtos, uma ideia por vez)."
                ),
            })

    # Padrão 2: aluno errou consistentemente → verifica se acerta mais com versão adaptada
    respostas_por_aula = defaultdict(list)
    for r in respostas:
        respostas_por_aula[r.questao.aula_id].append(r)

    for aula_id, suas in respostas_por_aula.items():
        originais = [r for r in suas if r.versao_mascara == 0]
        adaptadas = [r for r in suas if r.versao_mascara != 0]

        if originais and adaptadas:
            pct_original = sum(1 for r in originais if r.correta) / len(originais)
            pct_adaptada = sum(1 for r in adaptadas if r.correta) / len(adaptadas)

            # Melhora significativa com versão adaptada → sugere manter apoios ativos
            if pct_adaptada - pct_original >= 0.3 and not perfil.revisado_pelo_professor:
                nomes = perfil.nomes_apoios()
                if nomes:
                    sugestoes.append({
                        "campo": "foco",
                        "valor": perfil.foco,
                        "motivo": (
                            f"Acertos: {pct_original:.0%} na aula original, {pct_adaptada:.0%} na versão adaptada "
                            f"({', '.join(nomes)}). As adaptações estão funcionando. "
                            "Considere manter os apoios ativos."
                        ),
                    })

    # Padrão 3: se o aluno tem muitas respostas e acertos baixos, sugere textual
    if len(respostas) >= 6:
        pct_total = sum(1 for r in respostas if r.correta) / len(respostas)
        if pct_total < 0.5 and not perfil.textual and not perfil.foco:
            sugestoes.append({
                "campo": "textual",
                "valor": True,
                "motivo": (
                    f"Apenas {pct_total:.0%} de acertos em {len(respostas)} questões. "
                    "Sugestão: ativar Acessibilidade textual (linguagem simples, frases curtas) "
                    "ou Atenção e foco (passos curtos) para verificar se a dificuldade é com o texto."
                ),
            })

    return sugestoes


def criar_sugestoes_por_padrao(aluno):
    """Detecta padrões de erro e cria SugestaoPerfil pendentes, sem duplicar."""
    sugestoes = detectar_padroes(aluno)
    criadas = []
    agora = datetime.now().strftime("%d/%m %H:%M")
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)

    for sugestao in sugestoes:
        campo = sugestao["campo"]
        valor = sugestao["valor"]
        # Evita duplicar sugestão pendente igual
        ja_existe = SugestaoPerfil.objects.filter(
            aluno=aluno,
            campo=campo,
            valor_sugerido=valor,
            origem=SugestaoPerfil.Origem.PADRAO_ERRO,
            status=SugestaoPerfil.Status.PENDENTE,
        ).exists()
        if ja_existe:
            continue

        criadas.append(
            SugestaoPerfil.objects.create(
                aluno=aluno,
                campo=campo,
                valor_sugerido=valor,
                motivo=sugestao["motivo"],
                origem=SugestaoPerfil.Origem.PADRAO_ERRO,
            )
        )

        # Registra no histórico da IA
        acao = "ativar" if valor else "desativar"
        nome_campo = dict(SugestaoPerfil.CAMPOS).get(campo, campo)
        perfil.acrescentar_ao_historico(
            f"[{agora}] Sistema detectou padrão de erro e sugeriu {acao} \"{nome_campo}\": "
            f"{sugestao['motivo']}"
        )

    return criadas