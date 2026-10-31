# Roteiro de telas do vídeo (até 5 min)

Rascunho para o Cauã (roteiro e narração) e o Gabriel (edição) adaptarem. A ordem das telas segue o app como ele
funciona hoje; as falas são sugestões curtas.

## Antes de gravar

- **Tudo ao vivo e de verdade.** Professor, alunos e família são contas criadas na hora pela equipe; as respostas
  são dadas pela equipe durante a gravação. Nada de tela estática, dado inventado ou montagem que finja funcionar.
- **Nunca mostrar** o mockup de `design/` nem o protótipo da branch `thiago/prototipo-neuro`: são rascunhos de
  design com dados de exemplo.
- **Dois navegadores** (ou uma janela normal e uma anônima): um para o professor, outro para o aluno ou a família.
- **IA:** a geração só aparece se houver uma chave configurada. Sem chave, a tela mostra o aviso "A geração com IA não
  está ligada neste servidor"; nesse caso, explique isso em vez de mostrar uma versão adaptada que não foi gerada.
- Tenha aberta a aula de [aula_exemplo.md](aula_exemplo.md) para colar.

## Sequência

| Tempo | Tela | O que mostrar | Fala sugerida |
|---|---|---|---|
| 0:00–0:30 | Slide ou tela inicial | O problema, com os números de [contexto.md](contexto.md) | "96% dos alunos da educação especial estudam em turmas comuns. As matrículas de alunos autistas cresceram 4,4 vezes desde 2021. E só 6,4% dos professores regentes têm formação continuada em educação especial." |
| 0:30–0:50 | Login | A proposta em uma frase | "O professor prepara a aula uma vez, e cada aluno recebe a mesma aula no formato em que aprende. É para a turma inteira, sem laudo e sem separar ninguém." |
| 0:50–1:30 | Turma do professor | Criar turma, cadastrar 2 alunos e a família de um deles; **Nova aula** colando o texto e as 5 questões (ou **Criar via PDF**) | "A aula é escrita uma vez só, com o gabarito do professor." |
| 1:30–2:10 | Família (outro navegador) | Questionário de 9 perguntas sobre o dia a dia; depois, na tela **Apoios** do aluno, a sugestão que chegou e o professor aceitando | "A família conta o que observa em casa. Não pedimos laudo. As respostas viram sugestões, e quem decide é o professor." |
| 2:10–2:50 | Página da aula (professor) | **Gerar com IA** para a combinação "Atenção e foco"; revisar e **Aprovar versão**; mostrar que alternativas e gabarito não mudaram | "A IA reescreve só o texto e os enunciados. As alternativas e a resposta certa são sempre do professor, e nada chega ao aluno sem aprovação." |
| 2:50–3:40 | Aluno com foco (outro navegador) | Texto em passos ("Passo 1 de N"), barra **Apoios de leitura** (fonte, ouvir, modo limpo), questões uma por vez, correção | "Cada aluno vê a mesma aula no seu formato. Qualquer aluno pode ligar a leitura em voz alta ou a fonte com mais espaço entre as letras." |
| 3:40–4:30 | Painel da turma e Dashboard do aluno | Acertos por aluno e por questão, original × adaptada, uso dos apoios, sugestões; relatório da família | "Tudo o que aparece aqui vem do uso real. Se um aluno liga sempre a leitura em voz alta, o professor recebe a sugestão de deixá-la ligada." |
| 4:30–5:00 | Encerramento | Privacidade e próximos passos | "A IA nunca recebe o nome do aluno nem o que a família escreveu: só os apoios e a aula. Próximos passos: testar com escolas e medir o efeito na aprendizagem." |

## Depois de gravar

- Confira se nenhum segredo (chave de API, connection string) apareceu na tela ou na barra de endereço.
- Corte as esperas da IA (a geração pode levar alguns segundos), sem esconder que ela acontece.
