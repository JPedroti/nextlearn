# Plano de 15 passos até a entrega (sáb 31/10, 12h)

> **Pesquisa e brainstorm, anterior à versão final do produto.** Este primeiro plano foi substituído pelo roteiro em
> fatias do `CLAUDE.md`; os passos com respostas fictícias e personagens não foram feitos. O índice dos documentos está
> em [README.md](README.md).

Tempo disponível: ~18 h (sex 18h → sáb 12h). Time: 4 pessoas.
P1 = front-end · P2 = IA · P3 = pedagogia/dados · P4 = negócio/pitch

| # | Horário | Quem | Passo | Lente do conselho | Entregável / critério de pronto |
|---|---|---|---|---|---|
| 1 | 18:00–18:30 | Todos | Fechar o recorte (frações 6º ano ou alfabetização) e o critério dos juízes. Decidir com ~70% da informação: é porta de mão dupla | Bezos | Decisão escrita em 1 linha no README |
| 2 | 18:30–18:45 | Todos | Escrever o "press release" do Elo (5 linhas) e a lista do que NÃO entra | Bezos + Jobs | Press release + lista de cortes em `docs/` |
| 3 | 18:45–19:00 | Todos | Pré-mortem: "perdemos amanhã; por quê?" Cada um escreve 3 motivos em silêncio, depois juntam | Kahneman + Munger | Top 5 riscos com dono de cada mitigação |
| 4 | 19:00 | Todos | Um capitão por frente, que decide sozinho na sua área. Às 21h, 23h e 8h, cada um manda "Top 3: feito / travado / próximo" no grupo | Hastings + Huang | Divisão de frentes fixada no grupo |
| 5 | 19:00–20:00 | P3 | Taxonomia de 10 equívocos de frações, cada um com exemplo de resposta errada e a intervenção de 10 min | Pólya (entender antes de agir) | `dados/taxonomia.json` |
| 6 | 19:00–19:30 | P2 | Testar a API: a chave funciona? aceita imagem? qual o custo por chamada? Se não aceitar imagem, a entrada vira texto digitado, sem drama | Thorp (provar antes de apostar) + Musk (questionar o requisito) | Script de teste rodando |
| 7 | 20:00–21:00 | P3 | 30 respostas fictícias com o gabarito do equívoco certo, usando os personagens da Teachy (Davi, Talita, Daniel, Bruna) e seus perfis | Simons (dados > opinião) | `dados/respostas_teste.json` |
| 8 | 19:30–22:00 | P2 | Prompt de diagnóstico, medindo a acurácia contra as 30 respostas. Meta: ≥ 80%. Abaixo disso, simplificar a taxonomia | Feynman (não se enganar) + Simons | Número de acurácia (vai para o pitch) |
| 9 | 19:00–22:00 | P1 | Esqueleto ponta a ponta feio: entrada → diagnóstico → painel da turma → tela do aluno → mensagem da família. Sem estilo, com dado falso | Musk (algoritmo: deletar e simplificar antes de otimizar) | Fluxo clicável completo |
| 10 | 19:00–23:00 | P4 | Plano de negócios respondendo as 7 perguntas de Thiel (engenharia, timing, monopólio, pessoas, distribuição, durabilidade, segredo), mais cliente, preço por aluno/mês e custo de IA | Thiel + Walton (custo) | `docs/PLANO_NEGOCIOS.md` |
| 11 | 22:00–00:30 | P1 + P2 | Ligar a IA real no esqueleto: atividade adaptada por perfil, tutor que só dá pistas e mensagem para a família | Jobs (experiência ponta a ponta) | Demo funcionando com IA real |
| 12 | 00:30 | Todos | FEATURE FREEZE. Daqui em diante, só corrigir e embelezar, nada de recurso novo | Taleb (via negativa) + Jobs (foco) | Commit "freeze" no git |
| 13 | 01:00–07:00 | Todos | Dormir. No mínimo 5 h por pessoa, em turnos se precisar. Time exausto erra no pitch | Taleb (evitar a ruína) + Kahneman (fadiga piora decisões) | — |
| 14 | 07:00–09:30 | P1+P2 / P4 | Polir o visual da demo e congelar os dados da apresentação. Gravar um VÍDEO DE BACKUP da demo, para o caso de cair internet ou API. P4 fecha os slides: problema (3 dados dos slides da Teachy) → Elo → demo → acurácia → negócio → time | Thorp (pior cenário) + Knight (história) | Vídeo de backup + deck final |
| 15 | 09:30–11:00 | Todos | Ensaiar o pitch 3× cronometrado. O teste: alguém de fora entende em 1 min? Revisar README, push no git e ENVIAR ATÉ 11h (1 h de margem) | Feynman (explicar simples) + Dalio (dor + reflexão) | Submissão feita às 11h |

## Pendência crítica (resolver HOJE, não amanhã)
- O push para `JPedroti/learnext` ainda está bloqueado. Até as 21h, o dono do repo precisa adicionar `thico12p2` como colaborador e liberar o app do Claude. Se não der, subir num repo próprio e trocar o remote depois. Má notícia tem que viajar rápido (Gates).

## Onde o conselho discorda
- **Musk/Huang** ("acelera, vira a noite") × **Taleb/Kahneman** ("dorme, protege o pitch"): o plano escolhe dormir, porque o pitch vale mais que um recurso a mais.
- **Bezos** (ambição: família + imagem + regionalização) × **Jobs** (corte): fica o ciclo completo, mas num só conteúdo.
