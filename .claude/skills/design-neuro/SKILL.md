---
name: design-neuro
description: Guia de interface do NextLearn, escrito pelo Thiago. A mesma aula para a turma inteira, apoios em vez de diagnóstico, paleta por apoio com contraste conferido, regras de layout por apoio e checklist antes de entregar uma tela. Use ao criar ou mudar qualquer tela, template ou CSS do app.
---

# design-neuro

> Skill do Thiago (enviada ao João em 31/10/2026). O texto é o dele; só a tabela da paleta foi refeita em Markdown,
> porque chegou com uma cor por linha.

Guia para construir interfaces educacionais em que a mesma aula serve a turma inteira e cada aluno recebe o formato em
que aprende melhor (Desenho Universal para a Aprendizagem). Responda e escreva em português do Brasil.

## Princípios (não negociáveis)

- **Apoio, não diagnóstico.** A interface reage a apoios e preferências, nunca a rótulos clínicos. Nunca mostre
  "TDAH", "autismo", "laudo" ou a cor do perfil como identificação do aluno para a turma.
- **A mesma aula para todos.** Não chame o produto de "plataforma para neurodivergentes". Use "adaptações" ou "apoios"
  (não "AEE").
- **O professor decide.** Toda mudança de perfil vinda de dados de uso ou da família aparece como sugestão para o
  professor aceitar ou recusar.
- **Sem demo de fachada.** Telas com dados de exemplo ficam em protótipo marcado como tal; nunca vão para a demo oficial.
- **Evidência ou etiqueta.** Todo parâmetro vem de estudo/norma (cite) ou é marcado como "valor de produto, a calibrar".

## Perfis por barreira → apoios do app

O app tem 3 apoios de conteúdo (bits da máscara F*4 + S*2 + C*1) e 3 preferências de interface
(fonte_dislexia/letras espaçadas, leitura_voz, modo_limpo).

| Perfil (barreira) | Apoios | Preferências | Evidência |
|---|---|---|---|
| P1 Leitura e fluência | textual | leitura em voz alta, letras espaçadas | Texto em áudio d = 0,35 (Wood et al., 2018); espaçamento +20% de velocidade (Zorzi et al., 2012) |
| P2 Linguagem e compreensão | textual (+ concreto) | — | Estratégias de compreensão g = 0,59 (Filderman et al., 2021) |
| P3 Atenção e memória de trabalho | foco | modo limpo | Memória de trabalho d = 1,63–2,03 (Kofler et al., 2020) |
| P4 Previsibilidade e sensorial | foco + textual | modo limpo | Apoios visuais entre as 28 práticas do NCAEP (2020) |
| P5 Matemática | concreto | — | Intervenções digitais 0,55 (Benavides-Varela et al., 2020) |
| P6 Motor | — | (padrão para todos) alvos ≥ 44 px | WCAG 2.2, 2.5.5 |
| P7 Ritmo e abstração | concreto + foco | — | Análise de tarefa, exemplos concretos (NCAEP) |
| P8 Altas habilidades | fora da v1 | — | Próximo passo: aprofundamento |

Um aluno pode ter vários apoios: some as regras e, em conflito, vale a mais restritiva.

## Paleta por apoio

Prioridade: modo limpo > foco > textual > concreto > base. Use como variáveis CSS no `<body>`
(`--fundo`, `--superficie`, `--texto`, `--texto-suave`, `--destaque`, `--destaque-suave`, `--borda`).

| Tema | fundo | superficie | texto | texto-suave | destaque | destaque-suave | borda |
|---|---|---|---|---|---|---|---|
| base | `#F7F8FA` | `#FFFFFF` | `#1F2933` | `#52606D` | `#2B59C3` | `#E6EDFB` | `#E1E5EA` |
| foco (calma) | `#F4F6F8` | `#FFFFFF` | `#1E293B` | `#475569` | `#35557F` | `#E5EBF2` | `#DDE3EA` |
| textual (leitura) | `#FBF8F1` | `#FFFDF8` | `#2B2B2B` | `#555049` | `#1F5A96` | `#E7EEF7` | `#E8E1D3` |
| concreto (visual) | `#F7F9FB` | `#FFFFFF` | `#1F2933` | `#52606D` | `#0B6BA8` | `#E3F0F8` | `#E1E5EA` |
| limpo | `#FFFFFF` | `#FFFFFF` | `#111827` | `#374151` | `#1D4ED8` | `#EEF2FF` | `#D1D5DB` |

Cores de figuras (concreto): Okabe-Ito `#0072B2`, `#E69F00`, `#009E73`, `#CC79A7` (seguras para daltonismo; laranja e
amarelo só em formas, nunca em texto).

Por quê: foco usa baixa saturação e um só destaque (menos estímulo; GOV.UK: "use cores simples", evite "cores vivas
contrastantes"); textual usa fundo levemente tingido e texto cinza-escuro para reduzir brilho (guias de dislexia:
preferência individual, o aluno pode trocar); base evita verde/vermelho como único sinal.

Ao criar ou mudar uma paleta, confira o contraste: todo par de texto ≥ 4,5:1 (texto/fundo, texto/superfície,
texto-suave/fundo, destaque/superfície, branco/destaque). Calcule a luminância relativa WCAG; não aprove de olho.

## Regras de layout por apoio

- **Foco:** um passo por tela com "Passo X de N", barra de progresso, botões Voltar/Próximo; lista de outras tarefas
  recolhida; nenhuma animação (transition/animation desligados); um destaque por tela.
- **Textual:** frases curtas e literais; enunciado simplificado; botão "Ouvir" (Web Speech API, lang="pt-BR", botão
  vira "Parar"); texto ≥ 19 px, linha ≤ 65 caracteres, line-height ≥ 1,7.
- **Concreto:** exemplo do dia a dia e uma figura simples (ex.: barras de fração) com descrição em texto
  (role="img" + aria-label).
- **Modo limpo:** letra maior, sem sombras nem enfeites, só o essencial na lateral.
- **Letras espaçadas:** letter-spacing: .12em; word-spacing: .16em; line-height: 1.8–1.9. Não prometa ganho de fonte
  "para dislexia": a evidência é para espaçamento.

## Regras para todas as telas

- Alvos ≥ 44 × 44 px; foco visível (outline de 3 px no destaque); elementos reais (`<button>`, `<a href>`,
  `<label>` + `<input>`), aria-pressed em interruptores, aria-label em botões só com ícone.
- Certo/errado com texto ou ícone ("✓ Certo!", "Ainda não. A resposta certa é a B."), nunca só cor.
- Fonte de leitura: Atkinson Hyperlegible (ou a do sistema). Sem emoji como ícone.
- Respeitar prefers-reduced-motion.
- Preferências do aluno mudam só para ele, na hora, e geram registro de uso (no app: EventoUso).
- Tela do professor: sugestões com motivo e origem e botões Aceitar/Recusar; acertos com número + barra; versões da
  aula por combinação de apoios com status.
- Tela da família: linguagem simples, sem jargão nem diagnóstico; apoios escolhidos pelo professor; dicas práticas por
  apoio para fazer em casa.

## O que não fazer

- Personalizar por "estilo de aprendizagem" (Pashler et al., 2008: sem evidência).
- Medir "foco" por câmera, rosto ou emoção (diretrizes do CNE e LGPD).
- Ofensiva que pune, ranking individual para crianças pequenas, recompensa por tempo de uso, loot box, excesso de
  notificações (ECA Digital).
- Usar verde/vermelho como único sinal.

## Checklist antes de entregar uma tela

- Funciona nos 8 casos: original, foco, textual, concreto, foco+textual, os três, modo limpo e com letras espaçadas.
- Contraste de todos os pares de texto ≥ 4,5:1.
- Navegável só com teclado; foco visível; leitor de tela anuncia interruptores e figuras.
- Nenhum rótulo clínico, nenhum dado inventado fora de protótipo marcado.
- Cada parâmetro tem fonte ou está marcado como valor de produto.
