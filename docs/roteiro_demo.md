# Roteiro do vídeo (até 5 min) — com as falas

Roteiro do app que está na `main` (o que a banca vai rodar). Cada fala tem cerca de 130 palavras por minuto; o total
fica em torno de 4min30. Tudo é gravado ao vivo, com contas criadas pela equipe na hora.

## Antes de gravar (5 minutos)

- Duas janelas lado a lado: a normal (professor) e uma anônima (aluno ou família).
- Contas criadas pelo próprio professor no app: turma "7º ano B", aluno **Lucas** (sem apoio), aluna **Bia** (com
  "Atenção e foco") e a família da Bia. A aula de [aula_exemplo.md](aula_exemplo.md) já colada, mas ainda **não publicada**.
- **Chave de IA no `.env`** para mostrar a geração. Sem chave, pule a cena 4 e diga a fala alternativa.
- Nunca mostrar o mockup de `design/` nem os protótipos das branches: só o app da `main`.

## Cenas e falas

| # | Tempo | Na tela | O que dizer |
|---|---|---|---|
| 1 | 0:00–0:25 | Tela de entrar, com o camaleão | "Hoje, 96% dos alunos da educação especial estudam em turmas comuns, e só 6,4% dos professores têm formação continuada para isso. O professor tem uma aula e trinta jeitos diferentes de aprender na sala. O NextLearn resolve isso: o professor prepara a aula uma vez, e cada aluno recebe a mesma aula no formato em que aprende. Tudo o que vocês vão ver está funcionando agora." |
| 2 | 0:25–1:00 | Professor: turma → **Nova aula** (ou **Criar via PDF**) → questões com a correta marcada → **Publicar para a turma** | "Eu escrevo a aula como já faço, ou envio o PDF que já uso. Coloco as questões e marco a resposta certa. Esse gabarito é meu e nunca muda: a correção não depende da inteligência artificial." |
| 3 | 1:00–1:35 | Família (janela anônima): questionário de 9 perguntas → professor em **Apoios** da Bia: a sugestão aparece, **Aceitar** | "A família responde perguntas simples sobre o dia a dia, como 'ela se perde em tarefas longas?'. Não pedimos laudo nem diagnóstico. As respostas viram sugestões, e quem decide é o professor." |
| 4 | 1:35–2:15 | Página da aula → **Gerar com IA** em "Atenção e foco" → revisar → **Aprovar versão** | "Para cada combinação de apoios da turma, a IA reescreve só o texto e os enunciados: aqui, em passos curtos. No máximo sete versões por aula, não uma por aluno. Nada chega ao aluno sem eu revisar e aprovar. E a IA não recebe nenhum dado do aluno: só os apoios e a aula." |
| 5 | 2:15–3:20 | Lado a lado: **Lucas** (aula original) e **Bia** (texto em "Passo 1 de N", cores calmas, camaleão de outra cor). Na tela da Bia: **Letras espaçadas**, **Leitura em voz alta** (clicar em Ouvir), **Modo limpo**. Responder uma certa e uma errada | "Mesma aula, mesma turma, mesmo horário. O Lucas vê o texto original; a Bia vê em passos, um de cada vez, com menos estímulo na tela. Os colegas não veem diferença nenhuma. Qualquer aluno pode ligar letras espaçadas, ouvir o texto ou limpar a tela, sem rótulo. E o erro vem com explicação: 'Ainda não. A resposta certa é a B.'" |
| 6 | 3:20–4:00 | Professor: **Ver painel** → acertos por aluno e por questão, original × adaptada, uso dos apoios, sugestões; **Dashboard** da Bia | "O painel mostra só dado real: quem acertou o quê, na versão original e na adaptada, e quais apoios cada aluno usou. Se o Lucas liga a leitura em voz alta toda vez, eu recebo a sugestão de deixá-la ligada para ele." |
| 7 | 4:00–4:20 | Família: **Ver relatório** → acertos e "Como ajudar em casa" | "A família acompanha em linguagem simples e recebe dicas práticas para os apoios que o professor escolheu." |
| 8 | 4:20–4:40 | Volta à tela inicial | "Professor, aluno e família na mesma aula. Sem laudo, sem rótulo, com o professor no controle. NextLearn: a mesma aula, do jeito que cada aluno aprende." |

**Fala alternativa para a cena 4, se não houver chave de IA:** "A geração usa IA; neste computador ela está
desligada, e a tela avisa isso em vez de fingir. Com a chave configurada, o professor gera, revisa e aprova cada
versão." (E mostre a cena 5 só com as preferências de tela, que não dependem da IA.)

## Para convencer a banca (o que cada pilar procura)

- **Educação (Teachy):** a mesma aula para a turma inteira (Desenho Universal para a Aprendizagem), sem laudo, com o
  professor decidindo e a comparação de acertos entre a aula original e a adaptada.
- **Tech:** IA com saída estruturada, cache por combinação de apoios (no máximo 7 versões por aula), gabarito
  intocado, privacidade testada e 132 testes automáticos.
- **Negócio:** o custo de IA cresce com o número de aulas, não de alunos; na escola privada a adaptação é obrigação
  da escola (Lei 13.146/2015, art. 28).
- **Inovação:** em vez de um material por aluno, uma aula que se adapta por combinação de apoios, com o mascote que
  muda de cor junto.
