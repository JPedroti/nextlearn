# Histórico de prompts — Cauã

**Hackathon LEPV × FGV (Teachy) — Out/2026.** Índice da equipe: [README.md](README.md)
**Ferramenta de IA principal:** Qwen

Registro cronológico e literal dos prompts que Cauã enviou à IA durante o hackathon, mantido para consulta da banca avaliadora.

---

## Prompt 01 — 31/10/2026, 02:37 (BRT) — autor: Cauã — ferramenta: Qwen

> @nextlearn/CLAUDE.md Avalie o projeto, o que eu, cauã, ainda preciso fazer, e vamos começar após entender as demandas do projeto etc om as configurações de system prompt de engenharia de IA e backend necessárias ,me informe as mudanças e escolhas de tradeoff a serem feitas, vamos trabalhar

**Resumo da resposta da IA:** Blocos pedagógicos reescritos com conteúdo baseado em DUA (5 arquivos). Questionário expandido para 9 perguntas (3 por apoio), com tom humano e cordial + campos de nome do aluno e observações. Modelo `RespostaQuestionario` ganhou `nome_aluno` e `observacoes`; `Perfil` ganhou `contexto_familia` (editável pelo professor, alimenta o system prompt da IA). `prompt_builder.py` e `gerar_versao.py` integrados ao contexto familiar. Templates atualizados. 80 testes passando.

---

## Prompt 02 — 31/10/2026, 02:56 (BRT) — autor: Cauã — ferramenta: Qwen

> @nextlearn/CLAUDE.md @/home/caua/Área de trabalho/Hackathon/3288d172-edc6-4d82-b28c-e9e34cf50ac7.tmp.pdf @/home/caua/Área de trabalho/Hackathon/Mapa de Microproblemas Resolvidos.pdf verique se estamos seguindo essas diretrizes e normas, e como estamos perante a elas. Verifique ainda o que falta, independente de ser da minha parte ou não, para o backend e essa área dos outros me informe

**Resumo da resposta da IA:** Análise cruzada: código atende 12 das diretrizes dos PDFs (IA sugere/professor decide, sem laudo, DUA, LGPD). Diverge em stack (Django vs Streamlit), perfis (3 bits vs 8 P1–P8) e motor (IA generativa vs BKT). Gaps: deploy bloqueado (Gemini veda <18), push pendente (SSH), falta aula de exemplo e vídeo. Material do Thiago é pesquisa de apoio; CLAUDE.md é o documento canônico de decisões.

---

## Prompt 03 — 31/10/2026, 03:01 (BRT) — autor: Cauã — ferramenta: Qwen

> @nextlearn/CLAUDE.md Vamos focar na questão do django mesmo. Quero que você me explique como está a engenhenharia de IA e generenciamento do contexto do código e como podemos melhorar, se é possível. Vamos trabalhar com os exemplos, vamos pensar que o professor passe uma lista de exercícios, e devemos ensinar o aluno, como isso está sendo feito. ademas, como no backend está funcionando a diferenciação entre o site para cada um de seus perfis de aluno e suas intersecções?

**Resumo da resposta da IA:** Explicação detalhada do pipeline de IA (prompt_builder → cliente → gerar_versao), fluxo de aula/exercícios (professor cria → IA adapta → aluno responde com gabarito do professor), e diferenciação por papel (3 camadas: roteamento, máscara de bits, preferências de interface). Sugestões de melhoria: cache com contexto, feedback de erro, memória de interação.

---

## Prompt 04 — 31/10/2026, 03:17 (BRT) — autor: Cauã — ferramenta: Qwen

> @nextlearn/CLAUDE.md Quero que faça esse sistema de adaptação do conteúdo, enviando feedbacks diretamente para o professor em caso de ero/fraqueza específica, pelo menos faça algo simples que mexa com isso pro MVP. Faça alguma forma de guardar a memoria da interação, seja adcionando um com as conversas ou melhorado o system prompt. dÊ um relatório de como o filho está performando. faça com que o professor possa upar um PDF que será compreendido pelo agente de IA e será ensinado, com cada estratégia pra o aluno, após isso de commit

**Resumo da resposta da IA:** 4 features implementadas: (1) Memória de interação via `Perfil.historico_ia` — acumula eventos de geração e respostas, alimenta o system prompt; (2) Feedbacks automáticos via `analise.py` — detecta 3 padrões de erro e gera `SugestaoPerfil` para o professor; (3) Relatório da família em `/familia/alunos/X/relatorio/` com acertos, original vs adaptada e apoios usados; (4) Upload de PDF com PyPDF2 — professor sobe PDF, texto é extraído e pré-preenche formulário. 80 testes passando. Commit `216f3f4`.
