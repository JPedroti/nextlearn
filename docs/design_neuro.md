# Design por apoio (skill design_neuro) — branch thiago/prototipo-neuro

Protótipo navegável em `/prototipo/` (rode `python manage.py runserver` e abra http://127.0.0.1:8000/prototipo/).
Usa **dados de exemplo** de `apps/prototipo/dados.py` só para desenhar a estrutura. **Não é a demo** e não deve ir
para a `main` como está (regra de "demo de fachada" do hackathon): o que for aprovado aqui é levado para os templates reais.

## Paleta por apoio

A paleta acompanha o **apoio ligado**, nunca um diagnóstico, e nunca aparece como rótulo do aluno para a turma.
Prioridade quando há vários: modo limpo > foco > textual > concreto > base. Contraste conferido por
`scripts/contraste_paletas.py` (todos os pares de texto ≥ 4,5:1).

| Apoio | Paleta | Fundo | Texto | Destaque | Por quê |
|---|---|---|---|---|---|
| Nenhum (base) | Base | `#F7F8FA` | `#1F2933` | `#2B59C3` | Neutra, um destaque; azul/laranja em vez de verde/vermelho (daltonismo) |
| Atenção e foco (P3, P4) | Calma | `#F4F6F8` | `#1E293B` | `#35557F` | Baixa saturação, um só destaque: menos estímulo. Guia GOV.UK para autismo: "cores simples", evitar "cores vivas contrastantes" |
| Acessibilidade textual (P1, P2) | Leitura confortável | `#FBF8F1` (creme) | `#2B2B2B` (não preto puro) | `#1F5A96` | Fundo levemente tingido e texto cinza-escuro reduzem brilho para quem tem estresse visual; é preferência individual, o aluno pode trocar |
| Interativo e concreto (P5, P7) | Visual | `#F7F9FB` | `#1F2933` | `#0B6BA8` | Cores de apoio da paleta Okabe-Ito (`#0072B2`, `#E69F00`, `#009E73`, `#CC79A7`) para figuras, seguras para daltonismo |
| Modo limpo | Limpo | `#FFFFFF` | `#111827` | `#1D4ED8` | Sem enfeites, letra maior, muito espaço |

## Regras de interface que valem para todos

- Alvos de toque ≥ 44 px (WCAG 2.2, 2.5.5); foco visível; certo/errado sempre com texto ou ícone, não só cor.
- Letras espaçadas = `letter-spacing: .12em; word-spacing: .16em; line-height: 1.8–1.9` (Zorzi et al., 2012). Fonte "para dislexia" não tem ganho comprovado.
- Linha de leitura de no máximo ~65 caracteres; texto da aula ≥ 19 px.
- Foco: um passo por tela, barra de progresso, nada de animação; lista de outras aulas recolhida.
- Textual: frases curtas, enunciado simplificado, botão "Ouvir" (speechSynthesis pt-BR).
- Concreto: figura (ex.: barras de fração) com descrição em texto (`role="img"` + `aria-label`).

## Fontes
- British Dyslexia Association / Dyslexia Scotland: fundo tingido e espaçamento; fonte e cor são preferência individual.
- GOV.UK, "Dos and don'ts on designing for accessibility" (pôster para usuários autistas).
- Okabe & Ito, paleta segura para daltonismo.
- W3C WCAG 2.2.
