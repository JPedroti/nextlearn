# Cronograma e status do NextLearn

**Última atualização:** 31/10/2026, 00:50 (BRT), por João (Claude Code)

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
| Deploy da aplicação para a banca testar | João | ⚠️ | Configuração pronta no repositório (`render.yaml`, `build.sh`) e conferida com `check --deploy`. O serviço no Render ainda não foi criado (00h50). Depois: testar no ar e pôr o link no README. O endereço `nextlearn.onrender.com` é de outro projeto; o nosso vai ter um sufixo |
| Vídeo de demo (até 5 min) | Cauã (roteiro e narração), Gabriel (edição) | ❔ | |
| Plano de negócio em PDF | Gabriel | ❔ | |
| Repositório público ou com acesso para a banca | João | ⏳ | Fazer antes das 12h: o agente que avalia o pilar Tech precisa ler o código |

## Fatias do app

| Fatia | Horário previsto | Responsável | Status | O que falta |
|---|---|---|---|---|
| 0. Esqueleto (login com 3 papéis, deploy) | 23h–00h | João | ✅ código · ⚠️ deploy | Criar o serviço no Render e testar no ar |
| 1. Aula base (turma, aluno, aula, aluno responde a versão 000) | 00h–02h | João | ✅ (adiantada) | Testar no ar |
| 2. Motor de IA (apoios, geração com cache, aprovação, aluno vê a sua versão) | 02h–04h | Thiago (feita pelo João com Claude Code) | ✅ código (adiantada) · ⚠️ | Testar a geração real com a chave do Gemini; trocar os blocos provisórios de `ia/blocos/` pelo texto do Cauã |
| 3. Interface (OpenDyslexic, leitura em voz alta, modo limpo, registro de EventoUso) | 04h–06h | Thiago | ⏳ | Tudo |
| 4. Família (questionário → apoios sugeridos → revisão do professor) | 08h–09h15 | João | ⏳ | Tudo. Depende das 6 perguntas do Cauã |
| 5. Painel (acertos, adaptações usadas, sugestões de ajuste de perfil) | 09h15–10h30 | João | ⏳ | Tudo |
| Docs finais | até 10h30 | João | ⏳ | Link do deploy no README; `docs/arquitetura.md`, `docs/decisoes.md` e `docs/contexto.md` |

**Ordem de corte se atrasar:** (1) sugestões do painel → (2) questionário da família (o professor marca os apoios) →
(3) modo limpo. As fatias 0, 1 e 2 não podem ser cortadas.

## Por integrante

### João (Produto: contas, turma, aula, questionário da família, painel, deploy)

- ✅ Ideia, escopo e decisões do projeto (prompts 01–14 no claude.ai)
- ✅ Repositório no GitHub, `CLAUDE.md` e histórico de prompts separado por integrante
- ✅ Fatias 0, 1 e 2 (código na `main`, 45 testes passando)
- ⚠️ Deploy no Render: falta criar o serviço e colar `DATABASE_URL` (Neon) e `GEMINI_API_KEY` no painel
- ⏳ Fatia 4 (família) e Fatia 5 (painel)
- ⏳ Docs finais e repositório público antes das 12h

### Thiago (Produto: motor de IA, tela do aluno, preferências de interface)

- ❔ Ainda não há prompts dele no histórico nem commits no repositório
- ℹ️ A Fatia 2 (motor de IA e tela do aluno) já foi feita pelo João, então a próxima parte do Thiago é a Fatia 3
- ⏳ Fatia 3 (interface)

### Cauã (Conteúdo: aula de exemplo, questionário, blocos pedagógicos, roteiro e narração do vídeo)

- ❔ Blocos pedagógicos dos prompts (`ia/blocos/*.md`), com prazo às 02h. Por enquanto os arquivos têm um texto provisório
- ❔ Aula de exemplo para a demo
- ❔ 6 perguntas do questionário da família (necessárias para a Fatia 4)
- ❔ Roteiro e narração do vídeo

### Gabriel (Negócio: plano de negócio, edição do vídeo)

- ❔ Plano de negócio em PDF
- ❔ Edição do vídeo

## Registro de atualizações

- 31/10, 00:50 — Teste do deploy pedido; o serviço no Render ainda não existe. Passo a passo reenviado ao João.
- 30/10, 23:52 — Cronograma criado. Fatias 0, 1 e 2 concluídas no código, adiantadas em relação ao plano. O deploy ainda não foi feito (João).
