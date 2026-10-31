# Cronograma e status do NextLearn

**Última atualização:** 31/10/2026, 03:15 (BRT), por Cauã (Qwen)

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
| Deploy da aplicação para a banca testar | João | ⚠️ | Configuração pronta no repositório (`render.yaml`, `build.sh`) e conferida com `check --deploy`. Banco criado no Neon (São Paulo). Blueprint do Render aberto, mas o deploy foi pausado (01h15) até decidir o provedor de IA; dá para publicar antes com `GEMINI_API_KEY=pendente`. Depois: testar no ar e pôr o link no README. O endereço `nextlearn.onrender.com` é de outro projeto; o nosso vai ter um sufixo |
| Vídeo de demo (até 5 min) | Cauã (roteiro e narração), Gabriel (edição) | ❔ | |
| Plano de negócio em PDF | Gabriel | ❔ | |
| Repositório público ou com acesso para a banca | João | ⏳ | Fazer antes das 12h: o agente que avalia o pilar Tech precisa ler o código |
| **Decisão: provedor de IA** | Equipe (João decide) | ⚠️ | Os termos da Gemini API (grátis e paga) proíbem apps voltados a menores de 18 anos. Opções: API da Anthropic (Claude), que aceita produtos para menores com salvaguardas mas é paga; ou Vertex AI (Google Cloud), com termos a conferir. Trocar o provedor mexe só em `ia/cliente.py`. Sem isso, a geração por IA não funciona no ar |

## Fatias do app

| Fatia | Horário previsto | Responsável | Status | O que falta |
|---|---|---|---|---|
| 0. Esqueleto (login com 3 papéis, deploy) | 23h–00h | João | ✅ código · ⚠️ deploy | Criar o serviço no Render e testar no ar |
| 1. Aula base (turma, aluno, aula, aluno responde a versão 000) | 00h–02h | João | ✅ (adiantada) | Testar no ar |
| 2. Motor de IA (apoios, geração com cache, aprovação, aluno vê a sua versão) | 02h–04h | Thiago (feita pelo João com Claude Code) | ✅ código (adiantada) · ⚠️ | Decidir o provedor de IA (ver Entregas) e testar a geração real; trocar os blocos provisórios de `ia/blocos/` pelo texto do Cauã |
| 3. Interface (OpenDyslexic, leitura em voz alta, modo limpo, registro de EventoUso) | 04h–06h | Thiago (feita pelo João com Claude Code) | ✅ código (adiantada) | Testar a leitura em voz alta num celular e no navegador da banca; testar no ar |
| 4. Família (questionário → apoios sugeridos → revisão do professor) | 08h–09h15 | João | ✅ código (adiantada) | Trocar as 6 perguntas provisórias (`apps/perfis/questionario.py`) pelas do Cauã; testar no ar |
| 5. Painel (acertos, adaptações usadas, sugestões de ajuste de perfil) | 09h15–10h30 | João | ✅ código (adiantada) | Testar no ar com respostas reais da equipe |
| Docs finais | até 10h30 | João | ✅ (adiantada) · ⚠️ | `docs/arquitetura.md`, `docs/decisoes.md` e `docs/contexto.md` prontos. Falta o link do deploy no README e revisar os docs se o código mudar |

**Ordem de corte se atrasar:** (1) sugestões do painel → (2) questionário da família (o professor marca os apoios) →
(3) modo limpo. As fatias 0, 1 e 2 não podem ser cortadas.

## Por integrante

### João (Produto: contas, turma, aula, questionário da família, painel, deploy)

- ✅ Ideia, escopo e decisões do projeto (prompts 01–14 no claude.ai)
- ✅ Repositório no GitHub, `CLAUDE.md` e histórico de prompts separado por integrante
- ✅ Fatias 0, 1 e 2 (código na `main`, 45 testes passando)
- ✅ Projeto criado no Neon
- ⚠️ Deploy no Render: pausado no Blueprint; falta escolher o provedor de IA (ou publicar com a chave `pendente`)
- ✅ Fatia 4 (família), com perguntas provisórias
- ✅ Fatia 3 (interface), no lugar do Thiago, que não tinha começado
- ✅ Fatia 5 (painel)
- ✅ Docs finais (arquitetura, decisões, contexto com dados do Inep 2025)
- ⏳ Repositório público antes das 12h
- ❔ O número "6,4% dos professores com formação continuada em educação especial" (usado no CLAUDE.md) não foi encontrado na apresentação pública do Censo 2025. Achar a fonte pública antes de usar no vídeo ou no plano de negócio

### Thiago (Produto: motor de IA, tela do aluno, preferências de interface)

- ❔ Ainda não há prompts dele no histórico nem commits no repositório
- ✅ Pesquisas e materiais do repositório `learnext` juntados a este às 01h32 (`docs/*.md`, `db/`, `design/`, `prompts/0001–0020`)
- ⚠️ Alinhar com a equipe: parte desse material descreve outra versão do produto (tabela de laudo, papel de AEE, perfis P1–P8, métricas em 6 camadas), diferente das decisões do `CLAUDE.md` (sem laudo, 3 apoios). A banca vai ler tudo; decidir se fica como pesquisa de apoio, com um aviso, ou se sai do repositório
- ⚠️ O mockup em `design/` é uma tela estática: não pode aparecer no vídeo como se fosse o app funcionando (regra de demo de fachada)
- ℹ️ As Fatias 2 e 3 (motor de IA, tela do aluno e interface) já foram feitas pelo João com Claude Code. Sugestão: o Thiago testa o app (celular, leitura em voz alta) e ajuda no vídeo

### Cauã (Conteúdo: aula de exemplo, questionário, blocos pedagógicos, roteiro e narração do vídeo)

- ✅ Blocos pedagógicos dos prompts (`ia/blocos/*.md`) — texto definitivo, baseado em DUA, sem marcadores provisórios
- ✅ 9 perguntas do questionário da família (3 por apoio: foco, textual, concreto), com tom humano e cordial, + campo de nome do aluno + campo de observações (texto livre que alimenta o `contexto_familia` do perfil)
- ⏳ Aula de exemplo para a demo
- ⏳ Roteiro e narração do vídeo

### Gabriel (Negócio: plano de negócio, edição do vídeo)

- ❔ Plano de negócio em PDF
- ❔ Edição do vídeo

## Registro de atualizações

- 31/10, 03:15 — Cauã: Blocos pedagógicos reescritos com base no DUA (5 arquivos, sem texto provisório). Questionário expandido para 9 perguntas (3 por apoio) com tom humano + campos de nome do aluno e observações. Modelo `RespostaQuestionario` com `nome_aluno` e `observacoes`; `Perfil` com `contexto_familia` (alimenta o system prompt). Integração no `prompt_builder.py` e `gerar_versao.py`. Migração criada e aplicada. 80 testes passando.
- 31/10, 01:44 — Documentação final escrita (arquitetura com diagramas, decisões, contexto com dados conferidos no Inep). Todas as fatias do app concluídas no código; faltam deploy, provedor de IA e textos do Cauã.
- 31/10, 01:39 — Fatia 5 concluída no código (painel da turma e sugestões a partir do uso); 80 testes passando. Material do Thiago (repositório learnext) juntado à `main`, com as marcas de conflito resolvidas.
- 31/10, 01:33 — Fatia 3 concluída no código (barra de apoios de leitura, OpenDyslexic, voz, modo limpo, EventoUso); 70 testes passando.
- 31/10, 01:28 — Fatia 4 concluída no código (família, questionário, sugestões aceitas ou recusadas pelo professor); 60 testes passando.
- 31/10, 01:20 — Neon criado; deploy pausado pela questão dos termos da IA. O João pediu à IA as Fatias 4, 3 e 5 e a documentação final, em sequência.
- 31/10, 00:50 — Teste do deploy pedido; o serviço no Render ainda não existe. Passo a passo reenviado ao João.
- 30/10, 23:52 — Cronograma criado. Fatias 0, 1 e 2 concluídas no código, adiantadas em relação ao plano. O deploy ainda não foi feito (João).
