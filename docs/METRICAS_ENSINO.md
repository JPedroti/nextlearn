# Métricas de ensino da plataforma (v1, 30/10/2026)

> Público: alunos de 6 a 18 anos (fundamental I ao ensino médio), com os perfis funcionais P1–P8 de `docs/PERFIS_E_METRICAS.md`.
> Convenção: **[LIT]** = parâmetro de estudo ou dado publicado · **[DUO]** = prática documentada pelo Duolingo · **[PRODUTO]** = valor inicial de projeto, a calibrar com dados.

---

## 1. O que aprender com o Duolingo (e o que NÃO copiar)

### 1.1 O método, em 6 peças
| Peça | Como funciona | Resultado publicado | Fonte |
|---|---|---|---|
| **Prática curta de recuperação** | Lições de poucos minutos, só com exercícios (o aluno produz a resposta) | — | Duolingo; base: Dunlosky 2013 (prática de recuperação) |
| **Modelo de esquecimento por item (Half-Life Regression, HLR)** | Para cada palavra e cada aluno estima a "meia-vida" da memória (h). Chance de lembrar = 2^(−Δ/h), onde Δ = tempo desde a última prática. Acerto aumenta h, erro diminui. A melhor hora de revisar é quando Δ ≈ h (chance ~50%) | Erro de previsão 0,13, quase metade do método anterior (Leitner); no teste A/B: +9,5% de sessões de prática, +12% de atividade diária | Settles & Meeder, ACL 2016; blog Duolingo |
| **Dificuldade personalizada (Birdbrain)** | Prevê a chance de o aluno acertar cada exercício, modelando o que ele sabe e a dificuldade do item; monta a lição com exercícios no nível certo | Testes A/B: alunos aprenderam mais e voltaram mais (sem tamanho de efeito publicado) | Blog Duolingo (Birdbrain), IEEE Spectrum |
| **Modelo de estados do usuário** | 7 estados (novo, atual, reativado, ressuscitado, em risco na semana, em risco no mês, dormente). Métrica-norte: **CURR**, a taxa de retenção de quem já é ativo | CURR +21% em 4 anos; evasão diária dos melhores usuários −40%; DAU 4,5× | Blog Duolingo (growth model); Lenny's Newsletter |
| **Ofensiva (streak)** | Contador de dias seguidos. Mudança-chave: bastar 1 lição para manter a ofensiva, separada da meta diária | Retenção no dia 14: +3,3%; alunos em ofensiva: +10,5%; quem chega a 7 dias tem 2,4× mais chance de voltar no dia seguinte (correlação) | Blog Duolingo ("Improving the streak") |
| **Ligas** | Ranking semanal em grupos de 30 | Tempo de estudo +17%; usuários muito engajados triplicaram | Lenny's Newsletter |

**Eficácia:** quem completou 5 unidades de espanhol ou francês teve leitura e compreensão auditiva equivalentes a 4 semestres de faculdade (Jiang et al., *Foreign Language Annals*, 2021). Atenção: estudo feito por cientistas do próprio Duolingo.

### 1.2 Três lições para nós
1. **Modelar o esquecimento item a item** (HLR) e **a dificuldade item a item** (Birdbrain) é o núcleo técnico. Dá para fazer uma versão simples no hackathon.
2. **Hábito antes de volume:** a barreira para "manter a ofensiva" deve ser menor que a meta de estudo.
3. **Uma métrica-norte só**, com o resto como apoio.

### 1.3 O que NÃO copiar
1. **O Duolingo otimiza engajamento, não aprendizagem.** A análise do crescimento dele mede tempo e retenção, e nunca mede se o aluno aprendeu mais (Lenny's Newsletter). Nossa métrica-norte tem que ser de aprendizagem.
2. **Lei brasileira (ECA Digital, Lei 15.211/2025, em vigor desde 17/03/2026):** o Decreto 12.880/2026 trata como práticas de risco **recompensas atreladas ao tempo de uso**, **notificações em excesso**, ocultar pontos naturais de parada e autoplay. **Caixas de recompensa (loot boxes) são proibidas** para produtos de acesso provável por menores (art. 20). Configuração padrão deve ser a mais protetiva (art. 7º). Exige supervisão parental com limite de tempo (arts. 17 e 18).
3. **Ofensiva punitiva** ("você vai perder sua ofensiva!") gera ansiedade, e 20% dos autistas já têm transtorno de ansiedade (Lai et al. 2019). Usar ofensiva **semanal e flexível**, sem perda.

---

## 2. Arquitetura de métricas: 6 camadas

### Camada A — Aprendizagem (é aqui que fica a métrica-norte)
| Métrica | Definição | Parâmetro | Tipo |
|---|---|---|---|
| **Domínio por habilidade (BNCC)** | Probabilidade estimada de o aluno dominar a habilidade (modelo BKT) | Dominada com ≥ 0,95; estudo de 2025 indica que ≥ 0,98 prediz melhor a lição seguinte | [LIT] Corbett & Anderson; Zhang, Baker et al., EDM 2025 |
| **Taxa de acerto na sessão** | Acertos ÷ tentativas | **Zona-alvo: ~85% de acerto.** É o ótimo teórico para aprendizado (Wilson et al., *Nat Commun* 2019), mas o estudo foi em modelos de aprendizado de máquina e tarefas simples. Para alunos neurodivergentes, usar faixa de 70% a 85% [PRODUTO]: abaixo de 70% frustra, acima de 90% não ensina | [LIT] + [PRODUTO] |
| **Probabilidade prevista de acerto por item** | Estilo Birdbrain: escolher o próximo exercício com chance de acerto perto da zona-alvo | Mesma zona-alvo | [DUO] |
| **Ganho de aprendizagem** | Diferença entre diagnóstico inicial e final por habilidade | Ganho normalizado = (pós − pré) ÷ (100 − pré) | [PRODUTO], métrica padrão em pesquisa educacional |
| **Tipo de erro** | Conceito, procedimento, leitura do enunciado, fato aritmético, motor | Classificação por regras + IA | Slide Teachy |
| **Transferência** | Acerto em item novo da mesma habilidade, em contexto diferente | Confirma que não decorou o item | [PRODUTO] |

### Camada B — Memória e retenção
| Métrica | Definição | Parâmetro | Tipo |
|---|---|---|---|
| **Força de memória por habilidade** | Meia-vida h estimada (HLR); chance de lembrar = 2^(−Δ/h) | Agendar revisão quando a chance prevista cair para ~50% (Δ ≈ h) | [DUO] Settles & Meeder 2016 |
| **Retenção em 1, 7 e 30 dias** | Acerto ao rever a habilidade depois desses intervalos | Intervalo de revisão ≈ 20–40% do prazo desejado de lembrança | [LIT] Cepeda et al. 2008 |
| **Habilidades esquecidas** | Habilidades que já foram dominadas e caíram abaixo do limiar | Disparam revisão automática | [PRODUTO] |

### Camada C — Processo (como o aluno resolve)
| Métrica | Definição | Parâmetro | Tipo |
|---|---|---|---|
| Latência por item | Tempo da exibição até a resposta | Comparar com a mediana do próprio aluno, por tipo de item | [PRODUTO] |
| Variabilidade da latência | Coeficiente de variação na sessão | Subiu acima da linha de base → pausa ou bloco menor. **Nunca usar para diagnóstico** (Kofler 2013) | [LIT] + [PRODUTO] |
| Uso de dicas e nível da dica | Quantas dicas e de que profundidade | Dica funcionou = acertou a tentativa seguinte | [PRODUTO] |
| Uso indevido de ajuda (gaming) | Ações rápidas seguidas ou pedidos de dica em sequência até sair a resposta | Esses alunos aprendem menos; detectar e intervir | [LIT] Baker et al. 2004 |
| Erros consecutivos | Erros seguidos na mesma habilidade | 3 seguidos → mudar a estratégia (exemplo resolvido, pré-requisito) | [PRODUTO] |
| Autocorreção | Errou, revisou sozinho e acertou | Sinal de metacognição | [PRODUTO] |
| Uso de cada apoio (áudio, glossário, espaçamento) | Taxa por sessão | Apoio nunca usado sai do padrão | [PRODUTO] |

### Camada D — Hábito e engajamento (adaptado à rotina escolar)
| Métrica | Definição | Parâmetro | Tipo |
|---|---|---|---|
| **Estados do aluno** (versão escolar dos 7 estados do Duolingo) | Ativo na semana / em risco (sem uso há 7 dias) / dormente (14+ dias) | Ciclo **semanal**, porque escola tem fim de semana e férias | [DUO] adaptado |
| **Taxa de retorno semanal** (CURR escolar) | % dos alunos ativos numa semana que voltam na seguinte | Métrica de apoio, não norte | [DUO] adaptado |
| Sessões por semana e minutos ativos | Contagem e soma | Meta definida por professor e família, não pelo app | [PRODUTO] |
| Conclusão da sessão | Sessões terminadas ÷ iniciadas | Queda = sessão grande demais | [PRODUTO] |
| Ofensiva semanal | Semanas seguidas com a meta mínima cumprida (ex.: 3 sessões) | Sem perda punitiva; "congelamento" automático em férias | [DUO] adaptado + ECA Digital |

### Camada E — Bem-estar e limites (guarda-corpos)
| Métrica | Definição | Parâmetro | Tipo |
|---|---|---|---|
| Tempo diário de uso | Minutos por dia | Limite definido pela família (exigência do ECA Digital) e alerta ao professor | [LIT] lei |
| Sinal de frustração | Erros consecutivos + abandono rápido | Reduzir dificuldade e mensagem de encorajamento | [PRODUTO] |
| Autoavaliação rápida (opcional) | "Como foi? 🙂😐🙁" ao fim da sessão | Só para ajustar a experiência, nunca para publicidade (vedado pelo art. 22) | [PRODUTO] |
| Notificações enviadas | Quantidade por semana | Teto baixo (ex.: 1 por dia, só lembrete de estudo combinado) [PRODUTO]; o ECA Digital trata excesso como risco | [LIT] lei + [PRODUTO] |

### Camada F — Escola e família (agregadas)
| Para quem | Métrica |
|---|---|
| Professor | % da turma que domina cada habilidade; grupos por tipo de erro; alunos "em risco" ou com frustração |
| Coordenação | Evolução por turma; adaptações mais eficazes; dados para o PAEE e o PEI |
| Família | Habilidades dominadas na semana; 1 atividade de 10 min para casa; se a atividade foi feita |

---

## 3. Métrica-norte (o equivalente ao CURR do Duolingo)

**Habilidades dominadas E retidas por aluno, por mês**
(= habilidades com domínio ≥ 0,95 que continuam acima do limiar na revisão de 7 dias)

Por quê: mede aprendizagem real e durável, não tempo de tela. É também o número que a escola compra.
**Métricas de guarda (nunca piorar):** tempo diário dentro do limite da família, taxa de frustração, notificações.

---

## 4. Ajuste por perfil

| Perfil | Métricas primárias | Ajustes nos parâmetros |
|---|---|---|
| **P1 Leitura** | Acerto com áudio vs. com texto; fluência (palavras por minuto, comparando o aluno com ele mesmo); uso do texto para fala | Latência medida **depois** do fim do áudio, para não punir a leitura lenta |
| **P2 Linguagem** | Acerto com enunciado complexo vs. simplificado; literal vs. inferencial; uso do glossário | Zona-alvo calculada com o enunciado simplificado |
| **P3 Atenção / memória de trabalho** | Variabilidade da latência; queda de acerto ao longo da sessão; conclusão de sessão; respostas rápidas e erradas | Blocos curtos com pausa (duração calibrada pela queda de acerto do próprio aluno); pedir confirmação antes de enviar |
| **P4 Previsibilidade / sensorial** | Abandono após mudança; A/B com e sem agenda visual | Sem ofensiva nem ranking por padrão (o aluno ou a família ativam); formato de lição estável |
| **P5 Matemática** | Tipo de erro; latência em fatos básicos; acerto com e sem apoio visual | Fluência em fatos básicos como habilidade própria, com HLR |
| **P6 Motor** | Toques fora do alvo; acerto em digitação vs. múltipla escolha | Excluir o tempo motor da latência; alvos de 44 px |
| **P7 Ritmo / abstração** | Tentativas até o domínio; retenção em 1 e 7 dias | Mais repetições; revisões mais frequentes (meia-vida inicial menor) |
| **P8 Altas habilidades** | Itens até o domínio; respostas rápidas e certas seguidas de abandono (tédio) | Pular conteúdo dominado; zona-alvo mais exigente (~75–85%) |

Um aluno com mais de um perfil (ex.: TEA + TDAH = P3 + P4) recebe a **união** dos ajustes.

---

## 5. Ajuste por etapa (até 18 anos)

| Etapa | Quem conduz | Formato | Engajamento |
|---|---|---|---|
| **Fundamental I (6–10 anos)** | Família e professor mediam; painel principal é do adulto | Sessões curtas, muito visual e com áudio | Recompensas de progresso (trilha, medalhas); **sem ranking individual** |
| **Fundamental II (11–14)** | Aluno ganha autonomia; família acompanha | Sessões um pouco maiores; o aluno escolhe temas | Ligas **por equipe** (competição + colaboração, Sailer & Homner 2020) |
| **Ensino médio (15–18)** | Aluno define metas; família só recebe resumo | Trilhas por objetivo (ex.: ENEM) | Autoacompanhamento: painel pessoal de domínio e retenção |

Não há evidência sólida para um "tempo de atenção por idade" fixo. A duração da sessão é calibrada por aluno, pela queda de acerto (camada C) [PRODUTO].

---

## 6. Gamificação futura: o que pode e o que não pode

**Pode (evidência + lei):** barra de progresso, trilha de habilidades, medalhas por domínio (não por tempo), ligas por equipe, narrativa/missão, ofensiva semanal sem punição.
**Não pode / evitar:** loot boxes (proibidas), recompensa por tempo de uso, notificações em excesso, autoplay, ranking individual exposto para crianças pequenas, perda punitiva de ofensiva.

---

## 7. Recorte para a demo de amanhã (6 métricas)
1. Domínio por habilidade (BKT simplificado, limiar 0,95)
2. Taxa de acerto da sessão com zona-alvo
3. Tipo de erro
4. Latência e variabilidade (ajuste de pausa no P3)
5. Acerto com áudio vs. texto (P1)
6. Retenção agendada (revisão quando a chance de lembrar cai a ~50%)

---

## Fontes
- Settles & Meeder (2016), "A Trainable Spaced Repetition Model for Language Learning", ACL — e blog Duolingo "How we learn how you learn"
- Blog Duolingo: "Introducing Birdbrain"; "Growth model"; "Improving the streak"
- Lenny's Newsletter, "How Duolingo reignited user growth"
- Jiang et al. (2021), *Foreign Language Annals* (via comunicado do Duolingo, 2022)
- Wilson, Shenhav, Straccia & Cohen (2019), "The Eighty Five Percent Rule for optimal learning", *Nature Communications*
- Cepeda et al. (2008), *Psychological Science*
- Zhang, Vanacore, Baker et al. (EDM 2025), limiar de domínio em BKT
- Baker, Corbett & Koedinger (2004), ITS/CHI
- Kofler et al. (2013), *Psychological Bulletin*
- Sailer & Homner (2020), *Educational Psychology Review*
- Lai et al. (2019), *Lancet Psychiatry*
- Lei 15.211/2025 (ECA Digital) e Decreto 12.880/2026 — factsheet Machado Meyer
