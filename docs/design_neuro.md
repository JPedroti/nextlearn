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

## Cores por perfil (ferramenta do desenvolvedor e cenários da trilha)

O aluno nunca vê o rótulo; na escola, quem liga a interface são os apoios do professor. Para o time comparar,
a área do aluno tem a "Ferramenta do desenvolvedor" (só com `DEBUG=True`), em `apps/prototipo/perfis_dev.py`.

| Perfil (dev) | Apoios | Tema | Saturação do cenário | Por quê |
|---|---|---|---|---|
| Sem adaptação | — | Aurora | 1,0 | Referência |
| TDAH (P3) | foco | Oceano | 0,75, menos elementos | Memória de trabalho (Kofler 2020): menos estímulos competindo, um destaque |
| TEA (P4) / TEA+TDAH | foco + textual | Brisa | 0,45, poucos elementos | Sensibilidade sensorial: cores simples e suaves, nada se mexe (GOV.UK; NCAEP 2020) |
| Dislexia (P1) | textual + ouvir + letras espaçadas | Pergaminho | 0,8 | Fundo creme e texto cinza-escuro reduzem brilho (BDA); espaçamento (Zorzi 2012) |
| Discalculia (P5) | concreto | Parque | 1,0 | Cor como código de quantidade, Okabe-Ito |
| TDL (P2) | textual + concreto | Pergaminho | 0,85 | Linguagem simples + apoio visual |
| DI / ritmo (P7) | foco + concreto | Parque | 0,95, poucos elementos | Concreto e passos curtos |
| TDC (P6) | — (alvos maiores) | Aurora | 1,0 | WCAG 2.5.5: alvos de 56–96 px |
| Altas habilidades (P8) | — | Aurora | 1,1 | Cenário completo |

Os números de saturação e densidade são valor de produto, a calibrar com uso real.

## Mundos da trilha (`apps/prototipo/ambientes.py`)

- No máximo **10 fases por mundo**; depois começa outro mundo, mesmo na mesma matéria (Matemática → Matemática II).
- 12 ambientes: Deserto (pirâmides, oásis, camelos, cactos, dunas), Floresta, Fundo do mar, Polo de gelo, Espaço,
  Vulcão, Savana, Cidade, Praia, Caverna de cristal, Selva tropical, Montanhas e campos.
- Cada mundo usa uma semente (aluno + matéria + parte) que muda a ordem, o lado, o tamanho e o tom das cores
  dos elementos, para parecer novo. O perfil ajusta a saturação e a quantidade de elementos.
- O Next fica ao lado da fase atual, com uma fala gerada pela IA (`apps/prototipo/frases.py`): só o contexto da fase
  vai para a IA (sem nome nem dados do aluno), com cache de 1 hora e frases de reserva se a IA não responder.
