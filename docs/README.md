# Documentos do NextLearn

## O produto (o que vale)

| Documento | O que tem |
|---|---|
| [contexto.md](contexto.md) | O problema, com dados do Inep e do Instituto Rodrigo Mendes, e a resposta do produto |
| [arquitetura.md](arquitetura.md) | Partes do código, modelo de dados e como uma versão adaptada é gerada |
| [decisoes.md](decisoes.md) | Cada decisão técnica e de produto, com o porquê |
| [cronograma.md](cronograma.md) | Status das entregas e do trabalho de cada integrante |
| [historico_prompts/](historico_prompts/README.md) | Todos os prompts que a equipe mandou para ferramentas de IA, um arquivo por integrante |
| [aula_exemplo.md](aula_exemplo.md) | Aula usada na demonstração (o professor cola o texto no app) |

## Pesquisa e brainstorm (antes da versão final)

Material produzido pelo Thiago entre a tarde de 30/10 e a madrugada de 31/10, antes de a equipe fechar o produto.
Serviu de base para várias escolhas (por exemplo, os 3 apoios do app vêm dos 8 perfis por barreira), mas parte das
ideias não entrou no app: perfis P1–P8 com banco próprio, laudo opcional, papel de AEE, métricas de foco e retenção,
gamificação. Cada um desses arquivos tem um aviso no topo.

| Documento | O que tem | O que foi aproveitado no app |
|---|---|---|
| [mapeamento_pesquisa_app.md](mapeamento_pesquisa_app.md) | Ponte entre a pesquisa e o app | Justificativa dos 3 apoios. O plano da Fatia 3 (seção 4) acabou feito de outro jeito |
| [NEURODIVERGENCIA_EVIDENCIAS.md](NEURODIVERGENCIA_EVIDENCIAS.md) | Tipos, prevalência e evidências do que funciona e do que não funciona | Base para os apoios e para não depender de laudo |
| [PERFIS_E_METRICAS.md](PERFIS_E_METRICAS.md) | 8 perfis funcionais por barreira (P1–P8) | Os perfis viraram a justificativa dos 3 apoios (bits) |
| [METRICAS_ENSINO.md](METRICAS_ENSINO.md) | Métricas de ensino em 6 camadas, inspiradas no Duolingo | Só acertos e uso dos apoios de leitura; o resto ficou para depois |
| [RISCOS_LEGAIS.md](RISCOS_LEGAIS.md) | Leis e normas que afetam o produto (CNE, LGPD, ECA Digital, Decreto 12.686) | Sem laudo, dados mínimos, o aluno não conversa com a IA e o professor aprova tudo |
| [TESE_PRODUTO.md](TESE_PRODUTO.md) | Primeira tese de produto ("Elo": descobrir a causa do erro) | Não seguida: a equipe escolheu adaptar a mesma aula para cada aluno |
| [5_IDEIAS_NEGOCIO.md](5_IDEIAS_NEGOCIO.md) | 5 ideias de negócio em educação | A ideia 1 (acessibilidade para escolas) é a mais próxima do NextLearn |
| [PLANO_15_PASSOS.md](PLANO_15_PASSOS.md) | Primeiro plano de trabalho | Substituído pelo roteiro em fatias do `CLAUDE.md` |
| [PLANO_IMPLEMENTACAO.md](PLANO_IMPLEMENTACAO.md), [GUIA_METRICAS_E_LEIS.md](GUIA_METRICAS_E_LEIS.md), [MAPA_MICROPROBLEMAS.md](MAPA_MICROPROBLEMAS.md) | Resumos que apontam para documentos externos (claude.ai) | — |
| [PROMPT_PESQUISA_NEURODIVERGENCIA.md](PROMPT_PESQUISA_NEURODIVERGENCIA.md) | Prompt usado para a revisão de literatura | Gerou a pasta `pesquisa/` |
| [pesquisa/](pesquisa/) | Revisão de literatura (entrega 1) | Fonte das evidências citadas acima |
| [../db/schema.sql](../db/schema.sql) | Esboço de banco com 28 tabelas | Não usado: o app usa os models do Django, em `apps/` |
| [../design/](../design/) | Mockup estático da tela do aluno | Não é o app; a tela real está em `templates/` |
| [../prompts/](../prompts/) | Primeiro registro de prompts do Thiago, um arquivo por prompt | A lista completa está em `historico_prompts/thiago.md` |
