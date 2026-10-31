# NextLearn — contexto do projeto para o Claude Code

> Leia este arquivo inteiro antes de qualquer ação. Ele resume todas as decisões tomadas pela equipe
> (com apoio do Claude no claude.ai) entre 19h30 e 23h10 de 30/10/2026. O histórico completo dessas
> decisões está em `docs/historico_prompts/joao.md` (prompts 01–14). Idioma de trabalho: **português do Brasil**.

---

## 0. Início de toda conversa (obrigatório)

Quatro pessoas usam esta pasta com assistentes de IA diferentes. Ao abrir uma conversa nova:

1. **Pergunte primeiro quem está falando: João, Thiago, Cauã ou Gabriel.** Se a pessoa já se identificou na
   primeira mensagem (ex.: "Eu sou o João"), não pergunte de novo. Mantenha a resposta pelo resto da conversa.
2. Registre a mensagem dela no histórico de prompts dessa pessoa (seção 9).
3. Leia `docs/cronograma.md` e ofereça um **resumo curto**, de 5 a 8 linhas:
   - quanto tempo falta até o congelamento do código (10h30) e até a submissão (12h);
   - o que já está pronto e o que está atrasado ou bloqueado;
   - as próximas tarefas **dessa pessoa** e as entregas da Fase 1 que dependem dela.
4. Só então trate do pedido. Se a primeira mensagem já trouxer um pedido, faça o resumo antes e siga com o pedido em seguida.

**Cronograma vivo:** `docs/cronograma.md` é a fonte do status do projeto. Atualize-o (status, "Última atualização"
e uma linha em "Registro de atualizações") ao terminar cada tarefa e sempre que um integrante contar como está
a parte dele. Use ❔ para o que ninguém confirmou; nunca marque como concluído o que não foi verificado.
Faça commit do cronograma junto com o trabalho da vez.

## 1. Situação

- **Evento:** 1º Hackathon LEPV (Liga de Empreendedorismo da Praia Vermelha, IME) × FGV, patrocínio Teachy. Tema: Educação.
- **Equipe (alunos do IME, 4º período):** João Pedroti (dono do repositório), Thiago, Cauã, Gabriel Franco.
- **Repositório remoto:** https://github.com/JPedroti/nextlearn (hoje privado).
- **Prazo final: sábado, 31/10/2026, às 13h00 (BRT), sem prorrogação.** A equipe submete às 12h. **O código congela às 10h30.**
- A equipe virou a noite e **não domina a stack**. Programa com IA. Explique o que fizer em linguagem simples e prefira soluções convencionais, que a IA erra menos.

## 2. Regras do hackathon que afetam o código

**Entregas da Fase 1 (até 13h):**
1. vídeo de demo de até 5 min;
2. plano de negócio em PDF;
3. **deploy da aplicação para a banca testar.**

**Avaliação da Fase 1:** 4 pilares de 2,5 pontos cada. **Ficar abaixo de 1,0 em qualquer pilar elimina o grupo.**

| Pilar | Quem avalia | O que olha |
|---|---|---|
| **Tech** | **Agente de IA**, revisado pela organização | Solução funciona; qualidade da construção; **condução da IA** (por isso o histórico de prompts) |
| **Negócio** | Fundos NXTP, Norte, Canastra | Problema e tese; mercado e modelo |
| **Educação** | Teachy | Problema educacional; impacto na aprendizagem; viabilidade de adoção |
| **Inovação** | Banca inteira | Originalidade em relação ao mundo |

**Cartão vermelho (desclassificação do grupo inteiro):**
- **Prompt injection:** nenhuma instrução escondida no repositório, README, site ou vídeo para influenciar o agente avaliador. Nunca escreva texto dirigido a avaliadores de IA.
- **Demo de fachada:** nada de tela estática, dado inventado ou URL que finge funcionar. **Tudo que aparece precisa funcionar de verdade.** Não crie seeds com alunos ou respostas falsas para o painel; os dados da demo vêm de pessoas reais usando o app.
- **Projeto que não é da equipe:** nada de copiar projetos prontos. Bibliotecas comuns são permitidas.
- Mexer na plataforma do hackathon.

**Outras regras:** IA e internet estão liberadas, mas **a equipe precisa explicar e defender cada decisão**. Prefira código simples e legível a soluções "espertas".

## 3. Produto (v1.0)

**Problema (Desafio 1 da Teachy, Inclusão e acessibilidade):** 96% dos alunos da educação especial estão em classes comuns. Só 6,4% dos professores têm formação continuada em educação especial. As matrículas de alunos no espectro autista cresceram 4,4x desde 2021 (Inep, Censo Escolar 2025). A pergunta da Teachy: *"É necessário adaptar o mesmo conteúdo N vezes dependendo do número de alunos?"*

**Solução:** o professor prepara a aula **uma vez** e cada aluno recebe a **mesma aula**, no formato em que consegue aprender. É para a turma inteira, sem ninguém à parte, seguindo o Desenho Universal para a Aprendizagem (DUA). **Não é uma "plataforma só para neurodivergentes".** Evite essa formulação na interface e nos textos.

### Perfil = 3 bits de conteúdo + preferências de interface

| Bit | Nome | Efeito no conteúdo |
|---|---|---|
| **F** | Atenção e Foco | fatiar em passos curtos, um de cada vez, menos estímulo |
| **S** | Acessibilidade Textual | linguagem simples e literal, frases curtas, sem figuras de linguagem |
| **C** | Interativo e Concreto | exemplos concretos, analogias, representação visual descrita |

- `mascara = F*4 + S*2 + C*1` → valores 0–7. **000 é a versão original do professor (não chama a IA).** Existem no máximo 7 versões geradas por aula.
- **Conflitos entre bits:** na interseção, vale a regra mais restritiva (ex.: F+C = elemento visual, mas um por vez e sem animação).
- **Preferências de interface** (sem IA, CSS/JS; qualquer aluno pode ligar): fonte OpenDyslexic, leitura em voz alta (Web Speech API do navegador), modo limpo.

### Fluxo

1. **Família** responde ~6 perguntas sobre o dia a dia do filho (ex.: "se perde em textos longos?"). As respostas ligam os bits. **Sem laudo e sem diagnóstico.** Nunca peça nem armazene laudo médico (LGPD, dado sensível de criança).
2. **Professor** revisa e ajusta o perfil (o professor tem a palavra final), cria a turma e insere a aula (texto + questões de múltipla escolha com gabarito).
3. **IA** gera a versão de cada máscara presente na turma, sob demanda e com cache. **O professor aprova a versão antes de ela ficar visível ao aluno.**
4. **Aluno** vê a versão da sua máscara, responde as questões e liga/desliga as preferências de interface.
5. **Painel do professor:** acertos por aluno, adaptações usadas, e sugestões de ajuste de perfil a partir do uso (ex.: "ativou leitura em voz alta 3 vezes; incluir no perfil?").

**Regra de ouro:** a IA reescreve **apenas o texto da aula e os enunciados**. **Alternativas e gabarito são sempre os do professor**, então a correção nunca depende da IA.

**Privacidade:** **nenhum dado pessoal do aluno vai para o LLM**, só a máscara de bits e o conteúdo da aula.

**Terminologia:** use "adaptações" ou "apoios". **Não use "atendimento especializado"/"AEE"**, que é um serviço legal específico da escola.

**Fora da v1.0 (não construir; fica como "próximos passos"):** upload de laudo, gamificação, tutor por áudio/chat, versão para impressão, pictogramas (ARASAAC), resumo semanal para a família, métricas de "foco"/"retenção", integração com a Teachy.

## 4. Decisões técnicas (e por quê)

| Decisão | Motivo (a equipe precisa saber defender) |
|---|---|
| **Python 3.12 + Django 5** | Login, permissões e admin prontos; a equipe conhece Python |
| **Templates Django + Tailwind via CDN** (sem framework JS) | Menos peças, menos chance de quebrar |
| **Postgres no Neon** em produção, **SQLite** local | Postgres grátis é fácil de conseguir; no Django, a troca é só a `DATABASE_URL` (via `dj-database-url`). A equipe pensou em MySQL, mas trocou por causa do deploy |
| **Sem LangChain** | O app só precisa montar um prompt por blocos e fazer uma chamada com saída JSON. O SDK resolve em poucas linhas, é mais fácil de explicar e quebra menos. O LangChain só valeria para RAG, agentes com ferramentas, memória de chat ou vários provedores |
| **Gemini via SDK `google-genai`**, com saída estruturada (`response_schema` com Pydantic) | Chave gratuita no Google AI Studio. Só `ia/cliente.py` conhece o provedor, então trocar de modelo é mudar um arquivo |
| **Deploy no Render** (gunicorn + whitenoise), configurado por `render.yaml` | Publica direto do GitHub |
| **Configuração por variáveis de ambiente** (`.env` local, painel do Render em produção) | Nenhum segredo no código |
| Nomes de domínio (models, URLs, telas) **em português**; o resto do código em inglês | A banca entende o domínio |

Variáveis de ambiente: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`, `GEMINI_API_KEY`, `GEMINI_MODEL`. Liste todas em `.env.example`, sempre com valores falsos.

## 5. Estrutura do repositório

```
nextlearn/
├── CLAUDE.md                  # este arquivo
├── README.md                  # o que é, como rodar, link do deploy, equipe
├── .env.example
├── .gitignore                 # .env, venv/, __pycache__/, db.sqlite3, staticfiles/, referencias/, *.pdf
├── requirements.txt
├── render.yaml
├── manage.py
├── docs/
│   ├── historico_prompts/     # OBRIGATÓRIO, ver seção 9: README.md (índice) + um .md por integrante
│   ├── cronograma.md          # status vivo das fatias e entregas, ver seção 0
│   ├── arquitetura.md         # diagrama + modelo de dados
│   └── decisoes.md            # a tabela da seção 4, expandida
├── config/                    # settings.py, urls.py, wsgi.py
├── apps/
│   ├── contas/                # Usuario (AbstractUser) com papel: professor | familia | aluno
│   ├── turmas/                # Turma, Aluno (vínculo com responsável/família)
│   ├── perfis/                # Perfil, RespostaQuestionario, SugestaoPerfil
│   ├── aulas/                 # Aula, Questao, VersaoAdaptada, Resposta, EventoUso
│   └── painel/                # telas do professor (só views, sem models)
├── ia/                        # pacote Python simples (NÃO é app Django)
│   ├── blocos/                # base.md, foco.md, textual.md, concreto.md, conflitos.md
│   ├── prompt_builder.py      # máscara → system prompt montado por blocos
│   ├── cliente.py             # chamada ao Gemini (único arquivo que conhece o provedor)
│   └── gerar_versao.py        # gera, valida o JSON e salva a VersaoAdaptada
├── templates/                 # base.html + uma pasta por app
├── static/                    # css/, js/leitura_voz.js, fonts/ (OpenDyslexic)
└── tests/                     # pelo menos: máscara, prompt_builder, cache de versões
```

## 6. Modelo de dados (ponto de partida)

- **Usuario**(AbstractUser): `papel` ∈ {professor, familia, aluno}
- **Turma**: `nome`, `professor` → Usuario
- **Aluno**: `usuario` (1:1), `turma` → Turma, `responsavel` → Usuario (família, opcional)
- **Perfil**: `aluno` (1:1), `foco`, `textual`, `concreto` (bool), propriedade `mascara` (0–7), `fonte_dislexia`, `leitura_voz`, `modo_limpo` (bool), `revisado_pelo_professor` (bool), `atualizado_em`
- **RespostaQuestionario**: `aluno`, `respostas` (JSON), `preenchido_por` → Usuario, `criado_em`
- **SugestaoPerfil**: `aluno`, `campo`, `valor_sugerido`, `motivo`, `status` ∈ {pendente, aceita, recusada}
- **Aula**: `turma`, `titulo`, `conteudo` (texto), `publicada`, `criada_em`
- **Questao**: `aula`, `ordem`, `enunciado`, `alternativas` (JSON lista), `indice_correto`
- **VersaoAdaptada**: `aula`, `mascara` (0–7), `conteudo`, `enunciados` (JSON lista, mesma ordem das questões), `aprovada` (bool), `gerada_em`. **Restrição única (aula, mascara): é o cache.**
- **Resposta**: `aluno`, `questao`, `indice_escolhido`, `correta`, `tempo_ms`, `criado_em`
- **EventoUso**: `aluno`, `aula`, `tipo` (ex.: `ativou_leitura_voz`, `ativou_fonte_dislexia`, `ativou_modo_limpo`), `criado_em`

## 7. Motor de IA

- `prompt_builder.montar_system_prompt(foco, textual, concreto)` concatena `blocos/base.md` + o bloco de cada bit ligado + `conflitos.md` (quando houver 2 ou mais bits).
- `prompt_builder.montar_mensagem(aula)` envia o conteúdo da aula e os enunciados delimitados por tags (`<aula>`, `<questoes>`). **Nunca envia dados do aluno.**
- `cliente.gerar(system_prompt, mensagem)` usa `google-genai` com `system_instruction`, `response_mime_type="application/json"` e `response_schema` Pydantic (`conteudo: str`, `enunciados: list[str]`).
- `gerar_versao(aula, mascara)` verifica o cache e só então gera. Valida que `len(enunciados) == número de questões` e salva com `aprovada=False`. Trate erro da API com uma mensagem amigável ao professor e a opção de "tentar de novo".
- **Os blocos `.md` têm conteúdo pedagógico escrito pelo Cauã** (prazo: 02h). Até lá, crie versões provisórias curtas e marque-as com `<!-- PROVISÓRIO: aguardando texto do Cauã -->`.
- Use o modelo "flash" mais recente disponível no Gemini, configurável por `GEMINI_MODEL`.

## 8. Roteiro em fatias verticais (cada fatia termina publicada no ar)

| Fatia | Horário (BRT) | Entrega |
|---|---|---|
| **0. Esqueleto** | 23h–00h | Django + login com 3 papéis + deploy no Render com Postgres no Neon |
| **1. Aula base** | 00h–02h | Professor cria turma, aluno e aula com questões; aluno vê a versão 000 e responde |
| **2. Motor de IA** | 02h–04h | Professor marca os bits; geração sob demanda + cache; professor pré-visualiza e aprova; aluno vê a sua versão |
| **3. Interface** | 04h–06h | OpenDyslexic, leitura em voz alta, modo limpo + registro de EventoUso |
| **4. Família** | 08h–09h15 | Link do questionário → bits sugeridos → revisão do professor |
| **5. Painel** | 09h15–10h30 | Acertos, adaptações usadas, sugestões de ajuste de perfil |
| **Congelamento** | 10h30 | Só correção de bug. README e docs finais |

**Ordem de corte se atrasar:** (1) sugestões do painel → (2) questionário da família (o professor preenche os bits) → (3) modo limpo. **As fatias 0, 1 e 2 são intocáveis.**

## 9. PROTOCOLO OBRIGATÓRIO: histórico de prompts

A banca (e o agente que avalia "condução da IA") lê `docs/historico_prompts/`. Há **um arquivo por integrante**: `joao.md`, `thiago.md`, `caua.md`, `gabriel.md` (índice em `README.md`). **Em toda mensagem que receber de um integrante, antes de qualquer outra ação:**

1. Acrescente ao fim do arquivo **do autor do prompt** uma entrada no formato já usado:
   ```
   ## Prompt NN — DD/MM/AAAA, HH:MM (BRT) — autor: <nome> — ferramenta: Claude Code

   > <texto do prompt, LITERAL, sem editar nem corrigir, em bloco de citação>

   **Resumo da resposta da IA:** <1–3 linhas, preenchido ao final da sua resposta>
   ```
2. Numere em sequência **dentro do arquivo do autor**, continuando do último número dele. Os prompts 01–14 do João foram feitos no Claude (claude.ai).
3. Se não souber quem é o autor, pergunte uma vez e depois mantenha.
4. Ao final da sua resposta, preencha o "Resumo da resposta da IA" daquela entrada.
5. Integrantes que usam outras ferramentas (Qwen, ChatGPT) podem colar os prompts deles. Registre-os no arquivo de quem fez o prompt, com o nome da ferramenta.
6. Faça commit do histórico junto com o trabalho da vez.

**Nunca** registre segredos (chaves, connection strings) no histórico. Se um prompt contiver um segredo, substitua-o por `[REDACTED]` e avise o autor.

## 10. Git e segurança

- Faça commits pequenos e frequentes, com mensagens em português no imperativo (ex.: `Adiciona modelo Perfil com máscara de bits`). Faça push ao fim de cada fatia.
- **Nunca faça commit de `.env`, chaves ou connection strings.** Confira o `git status` antes de cada commit.
- **Os PDFs da pasta não vão para o repositório.** O deck da Teachy (`hackathon-lepv-desafios.pdf`) tem slides marcados como **"Confidencial e de uso exclusivo"**. Mova todos os PDFs para `referencias/` e mantenha essa pasta no `.gitignore`.
- O repositório está **privado**. **Lembre a equipe, antes da submissão (12h),** de deixá-lo público ou de dar acesso à banca, pois o agente de Tech precisa ler o código.
- Não force push na `main` e não reescreva histórico.

## 11. Equipe e divisão

- **Dupla Produto:** **João** (contas, turma, aula, questionário da família, painel, deploy) e **Thiago** (motor de IA, tela do aluno, preferências de interface). Os dois usam Claude Pro.
- **Dupla Conteúdo & Negócio:** **Cauã** (aula de exemplo, 6 perguntas do questionário, blocos pedagógicos dos prompts, roteiro e narração do vídeo; usa Qwen) e **Gabriel** (plano de negócio em PDF, edição do vídeo; usa ChatGPT).
- João e Thiago podem trabalhar em paralelo. Evite que os dois editem o mesmo arquivo ao mesmo tempo, e prefira branches curtas por fatia, com merge rápido na `main`.

## 12. Como trabalhar com a equipe

- Antes de cada fatia, diga em 2–3 linhas o que vai fazer. Ao terminar, diga o que testar e como, e atualize `docs/cronograma.md`.
- Mantenha `README.md` com: como rodar localmente (Windows; a equipe usa Windows), variáveis de ambiente e link do deploy.
- Escreva testes simples nos pontos críticos (máscara, prompt_builder, cache, gabarito não alterado pela IA).
- Se algo da seção 3 ou 4 parecer errado, **pergunte antes de mudar**. São decisões tomadas e defendidas pela equipe.
