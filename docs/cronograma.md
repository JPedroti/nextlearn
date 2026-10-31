# Cronograma e status do NextLearn

**Última atualização:** 31/10/2026, 10:58 (BRT), por João (Claude Code)

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
| Aplicação para a banca testar | João | ✅ decisão · ⚠️ | **Decisão do grupo (31/10, 07h44): o MVP roda localmente.** O README põe em destaque como rodar no Windows, no macOS e no Linux e um teste de 5 minutos. A configuração do Render fica pronta para depois. ⚠️ O `CLAUDE.md` listava o deploy como entrega (tirado das anotações da abertura; o texto do manual não fala de deploy): vale confirmar com a organização que app local é aceito. ⚠️ Sem chave de IA, quem rodar o app vê o botão "Gerar com IA" desligado: o vídeo precisa mostrar a geração funcionando |
| Vídeo de demo (até 5 min) | Cauã (roteiro e narração), Gabriel (edição) | 🔄 | Rascunho do roteiro de telas em `docs/roteiro_demo.md` e aula para colar em `docs/aula_exemplo.md`. Falta gravar, narrar e editar |
| Plano de negócio em PDF | Gabriel | 🔄 | Base em `docs/plano_negocio.md` (números conferidos com link, hipóteses marcadas, preço a definir). Falta o Gabriel fechar o texto e gerar o PDF (PDFs não vão para o repositório) |
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
| Docs finais | João | ✅ · ⚠️ | `README.md` (com macOS/Linux e teste em 5 minutos), `docs/arquitetura.md`, `docs/decisoes.md` e o índice `docs/README.md` atualizados às 07h10. Falta o link do deploy no README e rever os docs se o código mudar de novo |
| Testes automáticos no GitHub | João | ✅ | `.github/workflows/testes.yml` roda os 120 testes a cada envio para a `main` (aba Actions do GitHub) |

**Ordem de corte se atrasar:** (1) sugestões do painel → (2) questionário da família (o professor marca os apoios) →
(3) modo limpo. As fatias 0, 1 e 2 não podem ser cortadas.

## Por integrante

### João (Produto: contas, turma, aula, questionário da família, painel, deploy)

- ✅ Ideia, escopo e decisões do projeto (prompts 01–14 no claude.ai)
- ✅ Repositório, `CLAUDE.md`, histórico de prompts por integrante, Fatias 0–5 e docs
- ✅ Revisão do que o Cauã enviou de madrugada, com as decisões registradas no prompt 36 do `joao.md`
- ⚠️ Deploy no Render (ver Entregas)
- ⏳ Repositório público antes das 12h
- ✅ Fonte pública do "6,4% dos professores regentes com formação continuada em educação especial" (2024): Instituto Rodrigo Mendes, Panorama da Educação Especial 2025, com dados do Censo Escolar. Link em `docs/contexto.md`

### Thiago (Produto: motor de IA, tela do aluno, preferências de interface)

- ✅ Histórico de prompts 01–23 e `docs/mapeamento_pesquisa_app.md`, copiados da branch dele para a `main` às 06h17, sem o protótipo
- 🔄 Branch `thiago/prototipo-neuro` (último commit às 05h12): protótipo de design em `/prototipo/` (paleta por apoio, aula em passos, painel com menu lateral)
- ⚠️ O protótipo usa dados de exemplo (alunos "Aluno A–F" com acertos inventados): **não pode ir para a `main` nem para o deploy** (regra de demo de fachada). O passo a passo do apoio de foco já foi levado para a tela real; paleta por apoio e painel com menu lateral ficam para ele decidir
- ⚠️ A branch partiu da `main` das 01h32; a `main` mudou muito desde então (Fatias 3–5, visual novo do Cauã). Atualizar a branch antes de qualquer merge
- ⚠️ Os documentos antigos dele (ex.: `docs/TESE_PRODUTO.md`, que descreve outro produto) ganham um aviso no topo e um índice em `docs/README.md`, sem apagar nada
- ⚠️ O mockup em `design/` é uma tela estática: não pode aparecer no vídeo como se fosse o app funcionando
- 🔄 (07h44, pelo João) O Thiago está fazendo um frontend novo e vai pedir para o João seguir o estilo dele; talvez mande um meta prompt para guiar a IA. Quando ele fizer commit, a IA do João aplica o estilo nas telas reais. Cuidados: combinar com o Cauã, que mudou o visual entre 06h46 e 07h00, para o app ter um estilo só; construir em cima da `main` atual; nada de dados de exemplo nas telas

### Cauã (Conteúdo: aula de exemplo, questionário, blocos pedagógicos, roteiro e narração do vídeo)

- ✅ Blocos pedagógicos definitivos (`ia/blocos/*.md`), baseados no DUA
- ✅ 9 perguntas do questionário da família (3 por apoio), com campo de observações. **Mudança (decisão do João, 06h30):** as observações da família ficam só para o professor ler e **não vão para a IA**, como manda a regra de privacidade do `CLAUDE.md` (a família pode escrever um diagnóstico, que é dado sensível de criança). Pelo mesmo motivo saiu o histórico do aluno que ia para o prompt
- ✅ Aula de exemplo (equações do 2º grau) em `docs/aula_exemplo.md`. **Mudança (decisão do João, 06h45):** o comando `criar_aula_demo` foi apagado, porque criava professor e alunos de mentira (Daniel e Talita), o que o `CLAUDE.md` proíbe; na demo, o professor cola a aula no app
- ✅ Nova aula via PDF (corrigida: faltava a biblioteca e a aula não era salva), relatório da família, página do aluno para o professor, sugestão por acertos, modo concentração, visual novo e IA com vários provedores
- 🔄 Roteiro e narração do vídeo: rascunho de roteiro de telas em `docs/roteiro_demo.md`, para adaptar
- ⚠️ No histórico dele, os prompts 09 e 10 estão com horário estimado ("~07:10", "~07:25"); trocar pelo horário real do relógio, como pede a seção 9 do `CLAUDE.md`

### Gabriel (Negócio: plano de negócio, edição do vídeo)

- ❔ Plano de negócio em PDF
- ❔ Edição do vídeo

## Registro de atualizações

- 31/10, 10:58 — Depois do congelamento, decisões do João (prompt 43): (1) o app de protótipo (rota /jogo/, comando `contas_teste` com aluno fictício e respostas inventadas, templates `prototipo/`) saiu da `main`, por ser demo de fachada e gamificação fora da v1.0; continua no histórico do Git e nas branches do Thiago; (2) as métricas de acertos das turmas saíram do prompt da IA (a IA recebe só apoios e aula); a avaliação das versões pelo professor (`FeedbackVersao`) ficou; (3) entrou a skill design-neuro do Thiago nas telas reais (paleta por apoio com contraste testado, "Letras espaçadas", certo/errado escrito, aulas recolhidas com o apoio de foco, dicas para a família). 131 testes passando. **Até a submissão, ninguém envia nada para a `main`**; a branch `integracao/thiago-ux-mais-logica-main` não entra.
- 31/10, 07:45 — Decisão do grupo: o MVP roda localmente. README reorganizado (como rodar no computador primeiro; deploy vira nota de "depois do hackathon"); a chave de IA saiu da lista de variáveis pedidas pelo Render. O Thiago vai mandar um frontend novo para o app seguir.
- 31/10, 07:24 — Testes automáticos no GitHub (`.github/workflows/testes.yml`). Tela de login sem as dicas de usuários e senha de contas de mentira. App conferido em modo de produção (`DEBUG` desligado): arquivos estáticos, página 404 em português e todas as migrações num banco novo. 120 testes passando.
- 31/10, 07:12 — Rascunhos de `docs/roteiro_demo.md` (roteiro de telas do vídeo) e `docs/plano_negocio.md` (base do plano de negócio, só com números de fonte conferida).
- 31/10, 07:05 — Documentos organizados para a banca: índice `docs/README.md` e aviso no topo dos rascunhos antigos; fonte pública do 6,4% (Instituto Rodrigo Mendes); README, arquitetura e decisões atualizados. Barra de apoios voltou a mudar de cor na hora.
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
