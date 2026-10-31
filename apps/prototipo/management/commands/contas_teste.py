"""Cria contas de TESTE locais e um aluno fictício completo para simular a área do aluno.

Uso: python manage.py contas_teste

- Só para a máquina de desenvolvimento. NÃO é a demo oficial: todos os dados são inventados.
- As senhas são geradas na hora e gravadas em contas_teste_local.txt (ignorado pelo Git).
- Rodar de novo gera senhas novas e recria as aulas e respostas da turma de teste.

Aluno fictício: "Davi" (6º ano). Perfil de apoio P3 (atenção e memória de trabalho, o perfil típico do TDAH)
+ exemplos concretos para matemática. Foi montado a partir do questionário da família e revisado pelo professor;
nenhum laudo é pedido ou guardado.
"""

import secrets
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.aulas.models import Aula, Questao, Resposta, VersaoAdaptada
from apps.contas.models import Usuario
from apps.perfis.models import Perfil
from apps.turmas.models import Aluno, Turma

ARQUIVO = Path(settings.BASE_DIR) / "contas_teste_local.txt"
TURMA = "6º ano A (teste local)"

# (título "Matéria: assunto", texto, [(enunciado, alternativas, índice correto)], acertos do Davi, dias atrás, minutos)
# acertos=None → tarefa ainda não feita.
AULAS = [
    ("Matemática: O que é uma fração", "Uma fração mostra partes de um todo dividido em partes iguais. Em 3/4, o 4 (denominador) diz em quantas partes o todo foi dividido e o 3 (numerador) diz quantas foram pegas.",
     [("Em 3/4, quantas partes foram pegas?", ["4", "3", "7", "1"], 1),
      ("Uma pizza em 8 fatias iguais: 1 fatia é que fração?", ["1/8", "8/1", "1/4", "8/8"], 0),
      ("Qual número da fração é o denominador em 2/5?", ["2", "5", "7", "10"], 1)], 1, 33, 9),
    ("Português: Substantivo e adjetivo", "Substantivo dá nome às coisas (casa, Ana, alegria). Adjetivo dá uma característica ao substantivo (casa grande, dia frio).",
     [("Em 'gato preto', qual palavra é o adjetivo?", ["gato", "preto", "nenhuma", "as duas"], 1),
      ("Qual palavra é um substantivo?", ["bonito", "rápido", "escola", "feliz"], 2),
      ("Em 'menina alegre', 'menina' é:", ["adjetivo", "verbo", "substantivo", "advérbio"], 2)], 1, 31, 11),
    ("Ciências: Ciclo da água", "A água evapora com o calor do Sol, forma nuvens ao esfriar (condensação) e volta ao chão como chuva (precipitação).",
     [("O que faz a água evaporar?", ["O frio", "O calor do Sol", "O vento só", "A Lua"], 1),
      ("Quando o vapor esfria e vira nuvem, chamamos de:", ["condensação", "evaporação", "fusão", "infiltração"], 0),
      ("A chuva é a etapa de:", ["evaporação", "condensação", "precipitação", "solidificação"], 2)], 2, 26, 8),
    ("Matemática: Frações equivalentes", "Frações equivalentes representam a mesma quantidade: 1/2 = 2/4 = 4/8. Multiplique ou divida em cima e embaixo pelo mesmo número.",
     [("Qual fração é igual a 1/2?", ["2/3", "2/4", "1/4", "3/2"], 1),
      ("2/3 é equivalente a:", ["4/6", "4/5", "3/2", "2/6"], 0),
      ("Para achar uma equivalente, multiplicamos:", ["só o numerador", "só o denominador", "os dois pelo mesmo número", "por zero"], 2)], 1, 23, 14),
    ("Português: Pontuação", "O ponto final encerra a frase. O ponto de interrogação faz pergunta. A vírgula separa itens de uma lista.",
     [("Qual sinal usamos para perguntar?", [".", "?", ",", "!"], 1),
      ("Em 'Comprei maçã banana e uva', falta:", ["vírgula", "interrogação", "dois-pontos", "nada"], 0),
      ("O ponto final serve para:", ["perguntar", "encerrar a frase", "separar itens", "exclamar"], 1)], 2, 19, 10),
    ("Matemática: Comparar frações", "Com o mesmo denominador, é maior a fração com o maior numerador: 3/5 > 2/5. Pense em fatias da mesma pizza.",
     [("Qual é maior: 3/5 ou 2/5?", ["3/5", "2/5", "são iguais", "não dá para saber"], 0),
      ("Qual é menor: 1/8 ou 5/8?", ["5/8", "1/8", "iguais", "nenhuma"], 1),
      ("4/7 comparado a 4/7 é:", ["maior", "menor", "igual", "o dobro"], 2)], 2, 12, 9),
    ("Ciências: Estados físicos da água", "A água pode ser sólida (gelo), líquida ou gasosa (vapor). O calor e o frio mudam o estado.",
     [("Gelo é água no estado:", ["sólido", "líquido", "gasoso", "plasma"], 0),
      ("Gelo derretendo é a passagem de:", ["líquido para gás", "sólido para líquido", "gás para líquido", "líquido para sólido"], 1),
      ("Vapor é água no estado:", ["sólido", "líquido", "gasoso", "cristal"], 2)], 3, 9, 7),
    ("Matemática: Soma de frações", "Com o mesmo denominador, some só os numeradores e repita o denominador: 1/5 + 2/5 = 3/5.",
     [("1/5 + 2/5 =", ["3/10", "3/5", "2/5", "1/5"], 1),
      ("2/7 + 4/7 =", ["6/7", "6/14", "8/7", "2/7"], 0),
      ("Na soma com o mesmo denominador, o denominador:", ["dobra", "some", "se repete", "vira 1"], 2)], 3, 4, 8),
    ("Português: Interpretação de texto curto", "Leia: 'Lia levou o guarda-chuva porque o céu estava escuro.' Para entender, procure quem fez, o que fez e por quê.",
     [("Quem levou o guarda-chuva?", ["O céu", "Lia", "A mãe", "Ninguém"], 1),
      ("Por que ela levou?", ["Estava calor", "O céu estava escuro", "Era aniversário", "Estava com sono"], 1),
      ("O texto sugere que ia:", ["chover", "nevar", "fazer sol", "ventar só"], 0)], 2, 2, 12),
    ("Matemática: Frações na reta numérica", "Para marcar 3/4 na reta, divida o espaço entre 0 e 1 em 4 partes iguais e conte 3 partes a partir do 0.",
     [("Para marcar 1/3, dividimos o espaço entre 0 e 1 em:", ["2 partes", "3 partes", "4 partes", "1 parte"], 1),
      ("2/4 fica no mesmo ponto que:", ["1/2", "1/4", "3/4", "1"], 0),
      ("4/4 fica em cima do número:", ["0", "4", "1", "2"], 2)], None, 0, 0),
    ("Ciências: Cadeia alimentar", "Na cadeia alimentar, a energia passa de um ser vivo para outro: capim → gafanhoto → sapo → cobra. As plantas são produtoras.",
     [("Na cadeia capim → gafanhoto → sapo, quem é o produtor?", ["sapo", "gafanhoto", "capim", "nenhum"], 2),
      ("O gafanhoto come:", ["o sapo", "o capim", "a cobra", "nada"], 1),
      ("A seta mostra o caminho da:", ["água", "energia", "luz da Lua", "chuva"], 1)], None, 0, 0),
    ("Português: Verbos no passado", "Verbos no passado contam o que já aconteceu: eu brinquei, ela correu, nós partimos.",
     [("Qual verbo está no passado?", ["corro", "corri", "correrei", "correndo"], 1),
      ("'Ontem eu ___ bola.' Complete:", ["jogo", "joguei", "jogarei", "jogar"], 1),
      ("'Ela estudou' indica uma ação:", ["que vai acontecer", "que já aconteceu", "acontecendo agora", "impossível"], 1)], None, 0, 0),
]



# Versão aprovada (apoios foco + concreto = máscara 5) para a próxima tarefa do Davi
VERSAO_RETA = (
    "Passo 1. Pense numa régua de 0 até 1, como uma barra de chocolate.\n\n"
    "Passo 2. Para 3/4, quebre a barra em 4 pedaços iguais.\n\n"
    "Passo 3. Conte 3 pedaços a partir do 0. Onde parar, é o 3/4.",
    ["Para marcar 1/3, em quantos pedaços iguais você quebra a barra de 0 a 1?",
     "2 pedaços de 4 é o mesmo lugar que qual fração?",
     "Se você pegar 4 pedaços de 4, chega em qual número?"],
)


class Command(BaseCommand):
    help = "Cria contas de teste locais e o aluno fictício Davi com histórico de notas."

    def _usuario(self, username, papel, nome, sobrenome=""):
        usuario, _ = Usuario.objects.get_or_create(username=username, defaults={"papel": papel})
        usuario.papel, usuario.first_name, usuario.last_name = papel, nome, sobrenome
        senha = secrets.token_urlsafe(9)
        usuario.set_password(senha)
        usuario.save()
        return usuario, senha

    @transaction.atomic
    def handle(self, *args, **opcoes):
        prof, s_prof = self._usuario("prof.teste", Usuario.Papel.PROFESSOR, "Professora", "Teste")
        aluno_u, s_aluno = self._usuario("aluno.teste", Usuario.Papel.ALUNO, "Davi", "(fictício)")
        familia, s_fam = self._usuario("familia.teste", Usuario.Papel.FAMILIA, "Família do Davi", "(fictícia)")

        Turma.objects.filter(professor=prof).exclude(nome=TURMA).delete()
        turma, _ = Turma.objects.get_or_create(nome=TURMA, professor=prof)
        aluno, _ = Aluno.objects.get_or_create(usuario=aluno_u, defaults={"turma": turma})
        aluno.turma, aluno.responsavel = turma, familia
        aluno.save()
        perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
        perfil.foco, perfil.textual, perfil.concreto = True, False, True
        perfil.fonte_dislexia, perfil.leitura_voz, perfil.modo_limpo = False, True, False
        perfil.revisado_pelo_professor = True
        perfil.save()

        turma.aulas.all().delete()  # recria o histórico do zero
        agora = timezone.now()
        for titulo, texto, questoes, acertos, dias, minutos in AULAS:
            aula = Aula.objects.create(turma=turma, titulo=titulo, conteudo=texto, publicada=True)
            objs = [Questao.objects.create(aula=aula, ordem=i + 1, enunciado=e, alternativas=alt, indice_correto=c)
                    for i, (e, alt, c) in enumerate(questoes)]
            if titulo.endswith("reta numérica"):
                VersaoAdaptada.objects.create(aula=aula, mascara=perfil.mascara, conteudo=VERSAO_RETA[0],
                                              enunciados=VERSAO_RETA[1], aprovada=True)
            if acertos is None:
                # tarefas novas: publicadas há 1 a 3 dias (o prazo do protótipo é publicação + 7 dias)
                n_pend = sum(1 for a in AULAS if a[3] is None)
                ordem = [a[0] for a in AULAS if a[3] is None].index(titulo)
                Aula.objects.filter(pk=aula.pk).update(criada_em=agora - timedelta(days=n_pend - ordem + 1))
                continue
            quando = agora - timedelta(days=dias, hours=3)
            Aula.objects.filter(pk=aula.pk).update(criada_em=quando - timedelta(days=2))
            for i, q in enumerate(objs):
                certa = i < acertos
                escolha = q.indice_correto if certa else (q.indice_correto + 1) % len(q.alternativas)
                r = Resposta.objects.create(aluno=aluno, questao=q, indice_escolhido=escolha, correta=certa,
                                            tempo_ms=minutos * 60_000)
                Resposta.objects.filter(pk=r.pk).update(criado_em=quando)  # auto_now_add: ajusta a data depois

        ARQUIVO.write_text(
            "Contas de TESTE locais (dados fictícios; não versionar, não usar na demo oficial)\n"
            "Login: http://127.0.0.1:8000/prototipo/login/\n\n"
            f"professor  usuario: prof.teste     senha: {s_prof}\n"
            f"aluno      usuario: aluno.teste    senha: {s_aluno}   (Davi, apoio de foco + concreto)\n"
            f"familia    usuario: familia.teste  senha: {s_fam}\n",
            encoding="utf-8",
        )
        self.stdout.write(self.style.SUCCESS(f"Contas de teste prontas. Usuários e senhas em {ARQUIVO.name}"))
