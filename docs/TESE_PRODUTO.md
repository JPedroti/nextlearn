# Tese de produto — Hackathon Teachy <> LEPV 2026

> **Pesquisa e brainstorm, anterior à versão final do produto.** Esta primeira tese ("Elo") não foi seguida: a equipe
> escolheu adaptar a mesma aula para cada aluno. O que vale para o NextLearn está em [contexto.md](contexto.md) e
> [decisoes.md](decisoes.md); o índice dos documentos está em [README.md](README.md).

> Versão 1 (brainstorm), 30/10/2026. Nome provisório: **Elo**.

## 1. A tese em uma frase

**A escola já produz dados sobre cada aluno todo dia (provas, tarefas, faltas), mas ninguém tem tempo de ler o que esses erros dizem.** O Elo lê a resposta do aluno (inclusive foto da prova em papel), descobre *por que* ele errou e devolve, em minutos, o próximo passo certo para três pessoas: o aluno, o professor e a família. Depois mede de novo para ver se funcionou.

Desafio principal atacado: **05 (diagnóstico → recomendação)**. Por consequência, ele também cobre o 04 (adaptação), o 03 (IA saudável), o 01 (acessibilidade) e o 02 (engajamento por feedback e progresso).

## 2. Por que essa tese (os dados dos próprios slides)

| Fato | Fonte citada no slide | O que implica |
|---|---|---|
| O professor brasileiro gasta **6,1 h/semana corrigindo** (OCDE: 4,6 h); 60% citam correção como fonte de estresse | TALIS 2024 | Corrigir é a tarefa da rotina onde a IA devolve mais tempo |
| "Uma nota sozinha não mostra onde o aluno travou": 1/2 + 1/3 = 2/5 revela falta do *conceito* de fração | Slide Teachy | O valor está na **causa** do erro, não na nota |
| **72–73%** abaixo do nível básico em matemática | PISA 2025 | Há lacunas em massa: precisa ser por habilidade e escalável |
| Feedback bem feito = **+6 meses** de progresso | EEF Toolkit | O ciclo diagnosticar → recomendar → agir → medir é a alavanca com evidência |
| **88–89%** dos pais acham que o filho está no nível; nos testes, 30–50% estão | Gallup / Learning Heroes | A família está cega, e "quem sabe, age" |
| Chatbot sem proteção = **−17%** na prova sem IA; tutor com pistas mitigou o prejuízo | Bastani et al., PNAS 2025 | A IA do aluno precisa dar **pistas, nunca a resposta** |
| 50,2% da educação especial está em sala comum **sem AEE**; 6,4% dos professores têm formação | Censo / Todos Pela Educação | Adaptação precisa ser automática e embutida, não um extra |
| Notas e faltas no 9º ano preveem quem conclui o EM (81% × 22%) | UChicago Consortium | Sinais simples já servem para alerta precoce |

## 3. O que a Teachy já faz (não competir com o juiz)

A Teachy já gera planos de aula, slides, quizzes e jogos, corrige automaticamente, adapta material (ex.: TDAH) e gera relatórios. A estratégia declarada do CEO é ser "a infraestrutura integrada de IA da educação", juntando escola, professor, aluno e **família**.

**Conclusão:** um "gerador de aulas" ou um "Kahoot com IA" seria redundante. O espaço livre é **fechar o ciclo**: transformar o erro em causa, a causa em ação e a ação em medida, e levar isso **até a família**. É uma peça que se encaixa na Teachy em vez de disputar com ela.

## 4. O produto (MVP do hackathon)

**Fluxo de demonstração (3 minutos):**
1. **Professor fotografa** uma pilha de folhas de exercícios de frações (6º ano) ou importa respostas digitais.
2. **Raio-X do erro:** a IA lê cada resposta e classifica numa *taxonomia fixa* de ~10 equívocos de frações (ex.: "soma numeradores e denominadores", "não reconhece frações equivalentes", "erro de leitura do enunciado"). Classifica também o *tipo* de barreira: conceito, procedimento ou leitura (slide "Adaptação a partir do que o aluno demonstra").
3. **Painel da turma:** em vez de 30 notas, o professor vê **4 grupos por causa** ("9 alunos somam os denominadores"), cada um com uma mini-intervenção de 10 minutos sugerida. O professor aprova ou edita: o humano decide.
4. **Trilha do aluno:** cada aluno recebe uma próxima atividade curta, já no formato do seu perfil (Davi daltônico: cor + símbolo; Daniel com dislexia: áudio e texto curto; Talita com TDAH: um passo por vez) e com contexto regional (pizza em SP, açaí em Belém). Um **tutor que só dá pistas** ajuda sem entregar a resposta.
5. **Mensagem para a família:** um WhatsApp em linguagem simples ("A Ana entende frações quando vê desenhos, mas ainda soma os de baixo. Esta semana, peça para ela dividir uma pizza em 3 e em 4…").
6. **Medir de novo:** a próxima tentativa mostra se o apoio funcionou e atualiza o perfil. O ciclo fecha.

**Recorte deliberado (o que fica de fora):** só matemática, só frações, só 6º ano. Nada de vídeos personalizados, gamificação completa, gestão escolar ou outras disciplinas. Um ciclo profundo e funcionando vale mais que cinco módulos rasos.

## 5. Diferencial (por que nós e não um ChatGPT)

1. **Taxonomia de equívocos, não nota:** o diagnóstico vem da causa pedagógica e é auditável pelo professor.
2. **IA com guarda-corpos:** o aluno nunca recebe a resposta pronta, só pistas (evidência do PNAS).
3. **Três saídas de um só dado:** a mesma correção vira painel do professor, trilha do aluno e mensagem da família.
4. **Acessibilidade por padrão:** o perfil de acessibilidade é aplicado automaticamente a toda atividade gerada.
5. **Mede se funcionou:** o ciclo fecha com dado, não com fé.

## 6. Modelo de negócio (rascunho para o plano)

- **Cliente pagante:** escolas particulares de K-12 (a anotação do time: "Private K-12 is a massive market"). São ~46 milhões de matrículas na educação básica (Censo 2025); a rede privada é aproximadamente 1 em cada 5 (*confirmar o número exato no Censo*).
- **Por que a escola particular paga:** retenção de matrícula. Pais que veem o progresso real ficam, e a família vira argumento comercial.
- **Preço (hipótese a validar):** assinatura por aluno/mês, com professor e família incluídos. Plano piloto gratuito para 1 turma.
- **Expansão:** depois, redes públicas via secretarias (o alerta precoce de evasão é a proposta para a rede pública) e integração/parceria com plataformas como a Teachy.
- **Custo principal:** chamadas de modelo de IA por correção; ancorar o preço em ~10× o custo de IA por aluno.

## 7. Riscos (inversão: como isso fracassa)

1. **A IA diagnostica errado e o professor perde a confiança.** Mitigação: taxonomia fechada, confiança exibida, professor aprova antes de enviar, e um teste com respostas reais antes da demo.
2. **Escopo explode e a demo quebra ao vivo.** Mitigação: um único fluxo com dados fictícios preparados (os personagens dos slides da Teachy: Davi, Talita, Daniel), mais um vídeo de backup.
3. **Privacidade de dados de menores (LGPD).** Mitigação: na demo, só dados fictícios; no plano, consentimento da escola, minimização de dados e nada de dado sensível no prompt.
4. **"A Teachy já faz isso."** Mitigação: o pitch ancora no ciclo fechado com a família e na causa do erro, que é exatamente o desafio 05.

## 8. Viabilidade para 4 estudantes de engenharia

| Pessoa | Frente |
|---|---|
| 1 | Front-end: painel do professor, tela do aluno e prévia da mensagem da família (Streamlit para ir rápido, ou Next.js) |
| 2 | IA: prompts de diagnóstico com taxonomia, leitura de imagem e geração adaptada por perfil |
| 3 | Pedagogia e dados: montar a taxonomia de equívocos, as folhas de teste e as respostas fictícias realistas |
| 4 | Negócio e pitch: plano de negócios, slides e roteiro da demo |

**Stack mínima:** um modelo com visão via API (a chave fica no `.env`), backend em Python e banco simples (SQLite ou JSON).

## 9. Perguntas que o time precisa responder

1. Qual é o critério de avaliação dos juízes? (Inovação? Viabilidade? Aderência a um desafio específico?)
2. Matemática/frações é o melhor recorte, ou alfabetização (2º ano, dado do Inep) dá uma história mais forte?
3. A chave de API que temos aceita imagem (visão)? Se não, a entrada vira resposta digitada.

## 10. Próximos passos

1. **(Hoje, 30 min)** O time vota entre esta tese e as alternativas (seção 11) e fecha o recorte.
2. **(Em até 48 h)** Criar a taxonomia de 10 equívocos de frações e 30 respostas fictícias. Testar o prompt de diagnóstico e medir quantos acerta.
3. Construir o ciclo ponta a ponta feio, depois embelezar. Escrever o pitch em paralelo.

## 11. Ideias alternativas consideradas

| Ideia | Desafio | Por que não é a principal |
|---|---|---|
| Adaptador universal (1 material → N versões acessíveis) | 01 | A Teachy já adapta material; vira recurso **dentro** do Elo |
| Tutor socrático que só dá pistas | 03 | Forte, mas sozinho é commodity; vira peça **dentro** do Elo |
| Missões gamificadas regionalizadas | 02/04 | Gamificação é saturada (Kahoot, Duolingo, Wayground) e difícil de provar em 2 dias |
| Boletim real para os pais | 05 | Ótimo argumento de venda; entra como a saída "família" |
| Alerta precoce de evasão (notas + faltas) | 05 | Bom para a rede pública; fica como expansão no plano |
