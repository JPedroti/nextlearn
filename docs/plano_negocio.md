# Base do plano de negócio

Rascunho para o Gabriel montar o PDF. Todo número tem fonte com link; o que é **hipótese** (ainda não validado com
clientes) está marcado assim. Os campos entre colchetes são decisões da equipe.

## 1. O problema e para quem ele dói

- **A turma comum já é inclusiva, mas a aula ainda é uma só.** Em 2025, o Brasil teve 2,5 milhões de matrículas na
  educação especial (82% a mais que em 2021), e 96% dos alunos de 4 a 17 anos da educação especial estavam em classes
  comuns. As matrículas de alunos com autismo (TEA) passaram de 294 mil (2021) para 1,3 milhão (2025), 4,4 vezes
  mais. [Inep, Censo Escolar 2025](https://download.inep.gov.br/censo_escolar/resultados/2025/apresentacao_coletiva.pdf)
- **Quem dá a aula não foi preparado para isso.** Em 2024, só 6,4% dos professores regentes tinham formação
  continuada em educação especial. [Instituto Rodrigo Mendes, Panorama da Educação Especial 2025](https://institutorodrigomendes.org.br/panorama-educacao-especial-2025/)
- **Adaptar à mão não escala.** Adaptar a mesma aula para cada necessidade multiplica o trabalho do professor a cada
  aula; na prática, muitas vezes não acontece. É a pergunta do desafio: "É necessário adaptar o mesmo conteúdo N vezes
  dependendo do número de alunos?"
- **Na escola privada, o custo da adaptação é da escola.** A Lei Brasileira de Inclusão (Lei 13.146/2015, art. 28,
  §1º) proíbe cobrar valores adicionais do aluno com deficiência para cumprir as adaptações. [Lei 13.146/2015](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm)

## 2. A solução e o que a diferencia

- O professor escreve a aula **uma vez**; o NextLearn gera, com IA, uma versão para cada combinação de 3 apoios
  (atenção e foco, linguagem simples, exemplos concretos). São **no máximo 7 versões por aula**, não uma por aluno.
- **O professor aprova cada versão** antes de o aluno ver, e **alternativas e gabarito nunca mudam**: a correção não
  depende da IA.
- **Sem laudo e sem diagnóstico.** A família responde perguntas sobre o dia a dia; as respostas viram sugestões, e o
  professor decide.
- **Para a turma inteira** (Desenho Universal para a Aprendizagem): qualquer aluno pode ligar leitura em voz alta,
  fonte com mais espaço entre letras e modo limpo, sem rótulo.
- **Privacidade por desenho:** a IA recebe só os apoios e o texto da aula, nunca dados do aluno.
- **Mede o resultado:** o painel compara os acertos de cada aluno na versão original e na adaptada, com dados reais de uso.

## 3. Cliente, usuário e quem paga

| Quem | Papel |
|---|---|
| Escola privada (direção e coordenação pedagógica) | **Hipótese:** primeiro cliente pagante. Decide a compra sozinha e arca com o custo da adaptação (LBI, art. 28) |
| Redes públicas (secretarias de educação) | **Hipótese:** segundo passo, por programas ou compras públicas |
| Professor | Usuário principal: escreve a aula, aprova as versões e acompanha o painel |
| Família | Responde o questionário e vê o relatório do filho |
| Aluno | Recebe a aula no seu formato |

**Modelo de receita (hipótese):** assinatura anual por escola, cobrada por aluno matriculado. Preço: [definir].

## 4. Mercado (números conferidos)

| Dado (Brasil, 2025) | Valor | Fonte |
|---|---|---|
| Escolas de educação básica | 178,8 mil | Inep, Censo Escolar 2025 |
| Matrículas na educação básica | 46 milhões | Inep, Censo Escolar 2025 |
| Professores | 2,4 milhões | Inep, Censo Escolar 2025 |
| Matrículas na educação especial | 2,5 milhões | Inep, Censo Escolar 2025 |
| Escolas com internet | 94,5% | Inep, Censo Escolar 2025 |

Como calcular o tamanho do mercado (a equipe completa com o preço escolhido):

- **Mercado total:** matrículas na educação básica × preço por aluno por ano.
- **Mercado que dá para atender primeiro:** matrículas em escolas privadas × preço por aluno por ano.
  [Número de matrículas na rede privada: conferir no Censo Escolar 2025 antes de usar.]
- **Meta inicial:** [número de escolas-piloto] × alunos por escola × preço.

## 5. Custos

- **IA:** como a versão é uma por aula e combinação de apoios, o custo cresce com o número de **aulas**, não de
  alunos: no máximo 7 gerações por aula, guardadas para toda a turma. Custo por geração: [conferir no preço do
  provedor escolhido].
- **Hospedagem:** app web simples (Django, Postgres); o protótipo roda em planos gratuitos (Render e Neon).
- **Implantação:** treinar professores e coordenadores. **Hipótese:** curta, porque o professor escreve a aula como
  já faz (ou importa um PDF).

## 6. Riscos e como o produto responde

| Risco | Resposta |
|---|---|
| Termos dos provedores de IA para produtos usados por menores | O aluno nunca conversa com a IA: só o professor gera versões. O provedor é trocado por uma variável, sem mudar o app |
| Dados de criança (LGPD) | Sem laudo, dados mínimos, a IA não recebe nada do aluno, e o que a família escreve fica só com o professor |
| Erro da IA | O professor revisa e aprova cada versão; o gabarito é sempre o dele |
| Adoção pelo professor | A aula é escrita uma vez; as versões vêm prontas para revisar. **Hipótese a validar em piloto** |

## 7. Próximos passos

- Piloto com [n] escolas para medir o efeito na aprendizagem (acertos na versão adaptada × original, ao longo do tempo).
- Fora desta versão, já mapeados: versão para impressão, pictogramas, resumo periódico para a família, integração com
  plataformas que a escola já usa.
