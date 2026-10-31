# Perfis funcionais e métricas da plataforma (v1, 30/10/2026)

> **Pesquisa e brainstorm, anterior à versão final do produto.** No app, os 8 perfis viraram a justificativa de
> 3 apoios (ver [mapeamento_pesquisa_app.md](mapeamento_pesquisa_app.md)); laudo e métricas de foco ou retenção
> ficaram de fora. O índice dos documentos está em [README.md](README.md).

> Base: `docs/pesquisa/base_cientifica_neurodivergencia_entrega1.md` (verificada abaixo) + pesquisa nova com fontes.
> Convenção: **[LIT]** = parâmetro tirado da literatura · **[PRODUTO]** = valor inicial de projeto, sem estudo que o fixe; precisa ser calibrado com dados reais.

---

## Parte 1 — Verificação da Entrega 1

| Afirmação no arquivo | Status | Observação |
|---|---|---|
| TDAH 8,0% (IC 6–10%), 13 meta-análises, 588 estudos; meninos 10%, meninas 5% (Ayano 2023) | ✅ Confirmado | Também são 3.277.590 participantes |
| TEA + TDAH: 28% (Lai 2019) | ✅ Confirmado | 96 estudos; ansiedade 20%, sono 13%, depressão 11%, TOC 9% |
| Compreensão leitora g = 0,59, 64 estudos (Filderman 2021) | ✅ Confirmado | Acrescentar IC 95% [0,47; 0,74]. Maiores efeitos: conhecimento prévio e ensino de estratégias |
| Memória de trabalho executiva no TDAH: d = 1,63–2,03, 75–81% com prejuízo, n = 172 (Kofler 2020) | ⚠️ Números certos, **autores errados** | Os autores corretos são Kofler, Singh, Soto, Chan, Miller, Harmon e Spiegel. Corrigir a bibliografia |
| Kofler et al. 2019 (DOI 10.1037/neu0000598) | ⚠️ Conferir | Lista de autores e volume não verificados |
| Dislexia 7,10% (Yang 2022) | ✅ Confirmado | Meninos 9,22%, meninas 4,66% |
| TDC "NÃO ENCONTRADO" | ❌ Lacuna resolvida | 5% (IC 3–7%), 12 estudos, ~29 mil crianças — Li et al. 2024, *Front. Pediatr.*, DOI 10.3389/fped.2024.1387406 |
| Coluna "DSM-5-TR" (299.00, 314.0x, 315.00…) | ❌ Errado | São códigos do DSM-IV/CID-9-CM. O DSM-5-TR usa a CID-10-CM: TEA F84.0; TDAH F90.0/F90.1/F90.2; dislexia F81.0; discalculia F81.2; escrita F81.81; TDC F82; DI F70–F73; TDL F80.2; tiques/Tourette F95.x |
| Polanczyk 2015 (3,4%), Norbury 2016 (7,58%), Knight 2012 (0,77%), Zeidan 2022 | ◻️ Não reverificado nesta rodada | Fontes conhecidas e consistentes com o levantamento anterior; checar o DOI antes do slide |

---

## Parte 2 — Por que perfis por barreira (e não por diagnóstico)

1. **Lei:** o Decreto 12.686/2025 proíbe condicionar o AEE a laudo. O laudo entra como informação opcional, não como porta obrigatória.
2. **Comorbidade:** 28% dos autistas têm TDAH (Lai 2019). Um aluno pode ter **vários perfis ativos**, e as adaptações se somam.
3. **Funciona sem rótulo:** o professor marca as barreiras que observa, o sistema confirma com os dados de uso.

**Como o perfil nasce (três entradas):**
- Laudo (opcional), convertido em barreiras prováveis.
- Questionário curto de professor e família (ex.: "se cansa com textos longos", "precisa saber o que vem a seguir").
- Primeiras 2 semanas de uso: a plataforma mede e ajusta.

---

## Parte 3 — Núcleo de métricas (vale para TODOS os perfis)

| Métrica | Parâmetro | Tipo | Fonte |
|---|---|---|---|
| **Domínio por habilidade** (modelo de traçado de conhecimento, BKT) | Considerar dominada quando a probabilidade estimada de domínio for ≥ 0,95. Estudo recente sugere que ≥ 0,98 prediz melhor desempenho na lição seguinte | [LIT] | Corbett & Anderson (critério 0,95); Zhang, Vanacore, Baker et al., EDM 2025 |
| **Retenção** (revisão espaçada) | Intervalo ótimo entre estudo e revisão ≈ 20–40% do prazo em que se quer lembrar (ex.: para lembrar daqui a 1 semana, revisar após 1–2 dias); cai para 5–10% em prazos de 1 ano | [LIT] | Cepeda et al., *Psychol Sci* 2008 (n > 1.350) |
| **Uso indevido de ajuda** ("gaming the system") | Sinal: várias ações rápidas seguidas ou pedidos de dica em sequência até sair a resposta. Alunos que fazem isso aprendem menos | [LIT] para o padrão; limiar de tempo [PRODUTO] | Baker, Corbett & Koedinger, ITS e CHI 2004 |
| **Latência por item** | Mediana individual por tipo de item; comparar o aluno com ele mesmo | [PRODUTO] | — |
| **Variabilidade da latência** (coeficiente de variação na sessão) | Usar só para ajustar pausas e tamanho da tarefa. Não diagnostica: no TDAH g = 0,76, mas quase não separa de outros grupos clínicos (g = 0,25) | [LIT] para a não especificidade | Kofler et al., *Psychol Bull* 2013 (319 estudos) |
| **Uso de cada apoio** (áudio, dica, glossário, espaçamento) | Taxa de uso por sessão; apoio nunca usado sai do padrão | [PRODUTO] | — |
| **Teste A/B por aluno** | Alternar a adaptação entre sessões (desenho de tratamentos alternados) e manter a que melhora o domínio | [LIT] metodologia de caso único em educação especial | — |
| **Engajamento por gamificação** | Gamificação: g = 0,49 no aprendizado, 0,36 na motivação, 0,25 no comportamento; competição combinada com colaboração rende mais que competição sozinha | [LIT] | Sailer & Homner, *Educ Psychol Rev* 2020 |

**Regra de ouro (LGPD):** só telemetria comportamental. Nada de webcam, rastreamento ocular ou voz gravada sem necessidade.

---

## Parte 4 — Os perfis

### P1 · Decodificação e fluência de leitura
**Condições associadas:** dislexia, TDL, deficiência intelectual, baixa visão.
**Adaptações padrão:**
- Leitura em voz alta (texto para fala): d = 0,35 na compreensão, 22 estudos [LIT] — Wood et al., *J Learn Disabil* 2018.
- Espaçamento extra entre letras: +20% de velocidade, erros pela metade, n = 94 [LIT] — Zorzi et al., *PNAS* 2012.
- Não usar fonte "especial para dislexia" (sem evidência).

**Métricas e parâmetros:**
| Métrica | Parâmetro | Fonte |
|---|---|---|
| Palavras corretas por minuto (fluência) | Norma de referência: percentil 50 no 3º ano = 83 (início), 97 (meio), 112 (fim do ano). Sinal de intervenção: 10 ou mais palavras abaixo do percentil 50 | [LIT] Hasbrouck & Tindal 2017 — **normas em inglês**; para PT-BR, usar normas brasileiras ou a curva do próprio aluno |
| Diferença de acerto entre item em áudio e item em texto | Se o aluno acerta muito mais com áudio, a barreira é a leitura, não o conteúdo | [PRODUTO] |
| Uso de texto para fala | Alto uso + bom acerto = apoio funcionando; manter | [PRODUTO] |

**Para o professor:** "A barreira é a leitura, não a matemática: dê o enunciado em áudio."
**Para a família:** leitura compartilhada curta, todos os dias; o filho lê, o adulto apoia.

### P2 · Linguagem e compreensão
**Condições associadas:** TDL, TEA (linguagem pragmática e figurada), deficiência intelectual.
**Adaptações padrão:**
- Ensino de estratégias de compreensão + conhecimento prévio antes do texto: g = 0,59 (IC 0,47–0,74), 64 estudos [LIT] — Filderman et al. 2021.
- Enunciados com sintaxe simples (sem voz passiva nem orações encaixadas), glossário com imagem e linguagem literal [LIT] — Norbury et al. 2016 (barreiras); W3C COGA (padrões de conteúdo).

**Métricas:**
| Métrica | Parâmetro | Fonte |
|---|---|---|
| Acerto em item com enunciado complexo vs. simplificado (mesma habilidade) | Diferença grande = barreira de linguagem | [PRODUTO] |
| Uso do glossário visual | Uso alto e persistente = pré-ensinar vocabulário da próxima aula | [PRODUTO] |
| Acerto em perguntas inferenciais vs. literais | Separa compreensão literal de inferencial | [LIT] Filderman 2021 (estratégias) |

### P3 · Atenção e memória de trabalho (funções executivas)
**Condições associadas:** TDAH, também TEA, deficiência intelectual e lesão cerebral adquirida.
**Adaptações padrão:**
- Uma instrução por vez, instrução sempre visível na tela, tarefa dividida em etapas. Motivo: o déficit de memória de trabalho executiva no TDAH é grande (d = 1,63–2,03; 75–81% das crianças) [LIT] — Kofler et al. 2020.
- Sessões curtas com pausas; feedback imediato.
- **Não vender "mais tempo de prova" como solução:** de 26 estudos, 11 positivos, 3 mistos e 12 sem efeito; evidência inconclusiva [LIT] — NCEO, Accommodations Toolkit.
- **Não oferecer "treino cerebral":** sem efeito significativo no desempenho escolar [LIT] — Cortese et al. 2015.

**Métricas:**
| Métrica | Parâmetro | Fonte |
|---|---|---|
| Variabilidade da latência ao longo da sessão | Quando sobe acima da linha de base do próprio aluno, oferecer pausa ou encurtar a tarefa | [LIT] Kofler 2013 para o fenômeno; limiar [PRODUTO] |
| Queda de acerto ao longo da sessão | Define a duração ideal da sessão para aquele aluno | [PRODUTO] |
| Respostas rápidas demais e erradas | Sinal de impulsividade ou chute; pedir confirmação antes de enviar | [LIT] padrão de Baker 2004 |
| Taxa de conclusão de sessão | Abandono frequente = tarefa grande demais | [PRODUTO] |

**Para a família:** rotina fixa de estudo, blocos curtos, um lugar sem distrações, celular longe.

### P4 · Previsibilidade, sensorial e comunicação social
**Condições associadas:** TEA, diferenças de processamento sensorial.
**Adaptações padrão:**
- Apoios visuais, agenda visual da sessão ("primeiro isso, depois aquilo"), análise de tarefa, video modeling, reforço: entre as **28 práticas baseadas em evidência**, levantadas de 972 estudos [LIT] — Steinbrenner et al., NCAEP 2020.
- Intervenções mediadas por tecnologia no TEA: d = 0,47 (IC 0,08–0,86) [LIT] — Grynszpan et al., *Autism* 2014.
- Interface calma: sem animações automáticas, som opcional, aviso antes de qualquer mudança.

**Métricas:**
| Métrica | Parâmetro | Fonte |
|---|---|---|
| Abandono logo após mudança inesperada (troca de layout, som, tipo de atividade) | Sinal de sobrecarga; congelar o formato | [PRODUTO] |
| Desempenho com e sem agenda visual (A/B) | Mantém a agenda se ajudar | [LIT] NCAEP (apoios visuais) + A/B |
| Acerto em linguagem figurada vs. literal | Se cair muito, enunciados literais | [PRODUTO] |

### P5 · Senso numérico e matemática
**Condições associadas:** discalculia; também TDAH e deficiência intelectual.
**Adaptações padrão:**
- Intervenções digitais para dificuldade em matemática: efeito médio de 0,55, 15 ensaios randomizados, 1.073 crianças. **Videogames não superaram exercícios e tutoria digitais** [LIT] — Benavides-Varela et al., *Computers & Education* 2020.
- Representação concreta e visual (reta numérica, blocos), passo a passo.

**Métricas:**
| Métrica | Parâmetro | Fonte |
|---|---|---|
| Tipo de erro (conceito, procedimento, fato aritmético) | Classifica a causa | Slide Teachy ("nota sozinha não mostra onde travou") |
| Latência em fatos básicos (ex.: 7+5) | Latência alta e estável = fato não automatizado; praticar fluência | [PRODUTO] |
| Acerto com e sem apoio visual | Indica se o concreto ainda é necessário | [PRODUTO] |

### P6 · Motor e grafomotor
**Condições associadas:** TDC/dispraxia, disgrafia, Tourette, deficiência física.
**Adaptações padrão:**
- Abordagem orientada à tarefa e à participação; diretriz com 35 recomendações [LIT] — Blank et al., EACD, *Dev Med Child Neurol* 2019.
- Alvos de toque grandes: mínimo WCAG 2.2 AA = 24×24 px; recomendado neste perfil = **44×44 px** (AAA) [LIT] — W3C WCAG 2.2 (2.5.8 e 2.5.5).
- Trocar arrastar-e-soltar e escrita livre por toque, múltipla escolha ou ditado por voz. Nada de cronômetro em tarefa motora (WCAG 2.2.1, tempo ajustável).

**Métricas:**
| Métrica | Parâmetro | Fonte |
|---|---|---|
| Toques fora do alvo / erros de arrastar | Acima da média do próprio aluno = aumentar alvos | [PRODUTO] |
| Acerto em digitação livre vs. múltipla escolha (mesma habilidade) | Diferença grande = barreira motora, não de conteúdo | [PRODUTO] |

### P7 · Ritmo e abstração
**Condições associadas:** deficiência intelectual, síndromes genéticas.
**Adaptações padrão:** análise de tarefa e passos menores, exemplos concretos, mais repetições espaçadas. Objetivos ajustados no PEI/PAEE.
**Métricas:** número de tentativas até o domínio (≥ 0,95); retenção em 1 e 7 dias com revisões mais frequentes (Cepeda 2008); nível de dica usado.

### P8 · Altas habilidades (inclusive dupla excepcionalidade)
**Condições associadas:** altas habilidades/superdotação (56 mil no Censo 2025), sozinhas ou junto com TEA, TDAH ou dislexia.
**Adaptações padrão:** pular conteúdo já dominado, desafios mais profundos (enriquecimento). Em 2e, combinar com o perfil da outra condição.
**Métricas:** domínio rápido (poucos itens até 0,95) → oferecer aceleração; tédio = respostas rápidas e certas seguidas de abandono [PRODUTO].

---

## Parte 5 — Regras do ciclo de retroalimentação (exemplos)

| Se… | Então… |
|---|---|
| Acerto com áudio ≫ acerto com texto (P1) | Ativar texto para fala por padrão e avisar o professor |
| Variabilidade da latência sobe acima da linha de base (P3) | Oferecer pausa de 2 min ou encurtar o bloco |
| Domínio ≥ 0,95 | Avançar e agendar revisão espaçada (Cepeda) |
| Domínio não sobe após 2 sessões | Trocar a adaptação (A/B) e avisar o professor |
| Sinais de "gaming" | Bloquear dica seguida por alguns segundos e pedir uma tentativa |
| Toques fora do alvo altos (P6) | Aumentar alvos para 44 px e trocar o formato da questão |

---

## Fontes desta rodada
- Hasbrouck & Tindal (2017), normas de fluência — Reading Rockets
- Cepeda et al. (2008), *Psychological Science*, PMID 19076480
- Zhang, Vanacore, Baker et al. (EDM 2025), limiar de domínio em BKT
- Baker, Corbett & Koedinger (2004), "gaming the system", ITS/CHI
- Sailer & Homner (2020), *Educ Psychol Rev*, DOI 10.1007/s10648-019-09498-w
- NCEO, Accommodations Toolkit: tempo estendido
- W3C WCAG 2.2 (2.5.5, 2.5.8, 2.2.1) e W3C COGA
- Ayano et al. (2023), DOI 10.1016/j.jad.2023.07.071
- Lai et al. (2019), *Lancet Psychiatry* (via The Transmitter)
- Filderman et al. (2021), *Exceptional Children*
- Kofler et al. (2020), *Neuropsychology*, DOI 10.1037/neu0000641
- Grynszpan et al. (2014), *Autism*, PMID 24092843
- Benavides-Varela et al. (2020), *Computers & Education*, DOI 10.1016/j.compedu.2020.103953
- Li et al. (2024), *Front. Pediatr.*, DOI 10.3389/fped.2024.1387406
