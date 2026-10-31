# Cronograma e status do NextLearn

**Última atualização:** 31/10/2026, 06:58 (BRT), por João (Claude Code)

Este arquivo mostra o que já foi feito, o que está em andamento e o que falta. A IA que estiver trabalhando com a equipe
atualiza o arquivo ao fim de cada tarefa e sempre que um integrante contar como está a parte dele.

**Legenda:** ✅ concluída · 🔄 em andamento · ⏳ a fazer · ⚠️ pendência ou bloqueio · ❔ sem informação (confirmar com o responsável)

## Prazos

| Marco | Quando (BRT) | Status |
|---|---|---|
| Congelamento do código (depois disso, só correção de bug e docs) | 31/10, 10h30 | ⏳ |
| Submissão pela equipe | 31/10, 12h00 | ⏳ |
| Prazo final do hackathon (sem prorrogação) | 31/10, 13h00 | — |

## Entregas da Fase 1

| Entrega | Responsável | Status | Observação |
|---|---|---|---|
| Deploy da aplicação para a banca testar | João | ⚠️ | O grupo cogitou deixar o app só local, mas o deploy é entrega obrigatória e o pilar Tech avalia se a solução funciona. Configuração pronta (`render.yaml`, `build.sh`); banco criado no Neon; o Blueprint do Render parou na tela de variáveis. Dá para publicar **sem chave de IA**: o app funciona inteiro e o botão "Gerar com IA" fica desligado, com aviso. Depois: testar no ar e pôr o link no README |
| Vídeo de demo (até 5 min) | Cauã (roteiro e narração), Gabriel (edição) | ⏳ | Aula para colar na demo em `docs/aula_exemplo.md`. Roteiro de telas: ver o registro de atualizações |
| Plano de negócio em PDF | Gabriel | ❔ | |
| Repositório público ou com acesso para a banca | João | ⏳ | Fazer antes das 12h: o agente que avalia o pilar Tech precisa ler o código |
| **Decisão: provedor de IA** | Equipe (João decide) | 🔄 | Desde 06h46 (Cauã) o código aceita o Gemini ou qualquer API compatível com a da OpenAI (DeepSeek, Groq, OpenAI…), escolhidos pela variável `IA_PROVEDOR`. Falta escolher um provedor cujos termos permitam o uso em educação básica (os da Gemini API proíbem apps voltados a menores de 18 anos) e colocar a chave no Render |

## Fatias do app

| Fatia | Responsável | Status | O que falta |
|---|---|---|---|
| 0. Esqueleto (login com 3 papéis, deploy) | João | ✅ código · ⚠️ deploy | Criar o serviço no Render e testar no ar |
| 1. Aula base (turma, aluno, aula, aluno responde a versão 000) | João | ✅ | Testar no ar |
| 2. Motor de IA (apoios, geração com cache, aprovação, aluno vê a sua versão) | Thiago (feita pelo João com Claude Code) | ✅ código · ⚠️ | Blocos pedagógicos definitivos do Cauã ✅. Falta testar a geração real com uma chave |
| 3. Interface (fonte, leitura em voz alta, modo limpo, registro de uso) | Thiago (feita pelo João com Claude Code) | ✅ | Desde 06h50: texto da versão com apoio de foco **um passo por vez**, questões uma por vez com barra de progresso e "modo concentração" (tela cheia, do Cauã). Testar no celular e no ar |
| 4. Família (questionário → apoios sugeridos → revisão do professor) | João | ✅ | 9 perguntas definitivas do Cauã ✅. Testar no ar |
| 5. Painel (acertos, adaptações usadas, sugestões de ajuste de perfil) | João | ✅ | Testar no ar com respostas reais da equipe |
| Extras do Cauã (madrugada) | Cauã (revisados pelo João) | ✅ | Nova aula a partir de PDF, relatório da família, página de cada aluno para o professor, sugestão de apoio pelos acertos, visual novo. Corrigidos às 06h30–06h55 (ver registro) |
| Docs finais | João | 🔄 | Atualizar `README.md`, `docs/arquitetura.md` e `docs/decisoes.md` com as mudanças da manhã; índice de `docs/` |

**Ordem de corte se atrasar:** (1) sugestões do painel → (2) questionário da família (o professor marca os apoios) →
(3) modo limpo. As fatias 0, 1 e 2 não podem ser cortadas.

## Por integrante

### João (Produto: contas, turma, aula, questionário da família, painel, deploy)

- ✅ Ideia, escopo e decisões do projeto (prompts 01–14 no claude.ai)
- ✅ Repositório, `CLAUDE.md`, histórico de prompts por integrante, Fatias 0–5 e docs
- ✅ Revisão do que o Cauã enviou de madrugada, com as decisões registradas no prompt 36 do `joao.md`
- ⚠️ Deploy no Render (ver Entregas)
- ⏳ Repositório público antes das 12h
- ❔ O número "6,4% dos professores com formação continuada em educação especial" precisa de fonte pública (o slide da Teachy cita Censo Escolar 2024, Anuário da Educação Básica 2025 e Panorama da Educação Especial 2025)

### Thiago (Produto: motor de IA, tela do aluno, preferências de interface)

- ✅ Histórico de prompts 01–23 e `docs/mapeamento_pesquisa_app.md`, copiados da branch dele para a `main` às 06h17, sem o protótipo
- 🔄 Branch `thiago/prototipo-neuro` (último commit às 05h12): protótipo de design em `/prototipo/` (paleta por apoio, aula em passos, painel com menu lateral)
- ⚠️ O protótipo usa dados de exemplo (alunos "Aluno A–F" com acertos inventados): **não pode ir para a `main` nem para o deploy** (regra de demo de fachada). O passo a passo do apoio de foco já foi levado para a tela real; paleta por apoio e painel com menu lateral ficam para ele decidir
- ⚠️ A branch partiu da `main` das 01h32; a `main` mudou muito desde então (Fatias 3–5, visual novo do Cauã). Atualizar a branch antes de qualquer merge
- ⚠️ Os documentos antigos dele (ex.: `docs/TESE_PRODUTO.md`, que descreve outro produto) ganham um aviso no topo e um índice em `docs/README.md`, sem apagar nada
- ⚠️ O mockup em `design/` é uma tela estática: não pode aparecer no vídeo como se fosse o app funcionando

### Cauã (Conteúdo: aula de exemplo, questionário, blocos pedagógicos, roteiro e narração do vídeo)

- ✅ Blocos pedagógicos definitivos (`ia/blocos/*.md`), baseados no DUA
- ✅ 9 perguntas do questionário da família (3 por apoio), com campo de observações. **Mudança (decisão do João, 06h30):** as observações da família ficam só para o professor ler e **não vão para a IA**, como manda a regra de privacidade do `CLAUDE.md` (a família pode escrever um diagnóstico, que é dado sensível de criança). Pelo mesmo motivo saiu o histórico do aluno que ia para o prompt
- ✅ Aula de exemplo (equações do 2º grau) em `docs/aula_exemplo.md`. **Mudança (decisão do João, 06h45):** o comando `criar_aula_demo` foi apagado, porque criava professor e alunos de mentira (Daniel e Talita), o que o `CLAUDE.md` proíbe; na demo, o professor cola a aula no app
- ✅ Nova aula via PDF (corrigida: faltava a biblioteca e a aula não era salva), relatório da família, página do aluno para o professor, sugestão por acertos, modo concentração, visual novo e IA com vários provedores
- ⏳ Roteiro e narração do vídeo

### Gabriel (Negócio: plano de negócio, edição do vídeo)

- ❔ Plano de negócio em PDF
- ❔ Edição do vídeo

## Registro de atualizações

- 31/10, 06:58 — Juntados os envios do Cauã das 06h46 (IA com Gemini ou API compatível com a OpenAI) e 06h55 (visual novo dos painéis e do login). Acrescentada a biblioteca `openai` (faltava), `IA_PROVEDOR` no `render.yaml` e aviso de IA não configurada para os dois provedores. 119 testes passando.
- 31/10, 06:50 — Tela do aluno: versão com apoio de foco em passos; aula com uma questão volta a poder ser enviada; sem JavaScript tudo funciona. Painel individual: tempo deixou de ser multiplicado pelo número de questões. Páginas de erro em português. Sem chave de IA, o botão "Gerar com IA" fica desligado com aviso.
- 31/10, 06:45 — Comando `criar_aula_demo` apagado (criava alunos de mentira); aula de exemplo em `docs/aula_exemplo.md`.
- 31/10, 06:35 — Revisão do envio do Cauã das 06h17: observações da família e histórico do aluno saem do prompt da IA (privacidade); cache por (aula, máscara) volta a valer; PDF consertado (`pypdf`); relatório da família corrigido; sugestão por acertos com uma regra só. 99 testes passando.
- 31/10, 06:17 — Nome do João só com o primeiro nome no repositório. Histórico de prompts do Thiago (01–23) e `docs/mapeamento_pesquisa_app.md` trazidos da branch dele para a `main`, sem o protótipo.
- 31/10, 05:57 — Revisão do GitHub: nada novo na `main` desde 01h45; chegou a branch `thiago/prototipo-neuro` (protótipo de design com dados de exemplo, fora da demo). Nenhuma chave nos commits novos. 80 testes passando.
- 31/10, 03:15 — Cauã: blocos pedagógicos reescritos com base no DUA; questionário com 9 perguntas, nome do aluno e observações; `Perfil` com `contexto_familia` no system prompt (revertido às 06h35, ver acima).
- 31/10, 01:44 — Documentação final escrita (arquitetura com diagramas, decisões, contexto com dados conferidos no Inep). Todas as fatias do app concluídas no código.
- 31/10, 01:39 — Fatia 5 concluída no código (painel da turma e sugestões a partir do uso). Material do Thiago (repositório learnext) juntado à `main`.
- 31/10, 01:33 — Fatia 3 concluída no código (barra de apoios de leitura, OpenDyslexic, voz, modo limpo, EventoUso).
- 31/10, 01:28 — Fatia 4 concluída no código (família, questionário, sugestões aceitas ou recusadas pelo professor).
- 31/10, 01:20 — Neon criado; deploy pausado pela questão dos termos da IA.
- 31/10, 00:50 — Teste do deploy pedido; o serviço no Render ainda não existe.
- 30/10, 23:52 — Cronograma criado. Fatias 0, 1 e 2 concluídas no código.
