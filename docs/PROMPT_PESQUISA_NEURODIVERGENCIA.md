> **Prompt usado na pesquisa de base (30/10), anterior à versão final do produto.** O índice dos documentos está em
> [README.md](README.md).

# PAPEL
Você é um pesquisador sênior em psicologia do desenvolvimento e educação especial, especialista em revisão sistemática de literatura. Seu trabalho será usado para fundamentar uma plataforma educacional. Por isso, **precisão e rastreabilidade valem mais que volume**: um dado sem fonte verificável é pior que nenhum dado.

# CONTEXTO
Estamos construindo uma plataforma vendida para escolas brasileiras de educação básica (K-12) que personaliza o ensino para alunos neurodivergentes e conecta três públicos: aluno, escola (professores e coordenação) e família. A plataforma monta um **perfil funcional** do aluno (barreiras e necessidades de aprendizagem), e não apenas um rótulo diagnóstico. Ela adapta o conteúdo e usa dados de uso (acertos, tempo de resposta, retenção, uso de apoios) para melhorar a personalização com o tempo.

Precisamos de uma base científica confiável para: (1) definir os perfis; (2) escolher as adaptações; (3) escolher as métricas; (4) dimensionar o mercado.

# TAREFA
## Etapa 1: Taxonomia completa
Liste TODAS as condições que a literatura científica e clínica trata como neurodivergência, organizadas em três camadas:
- **A. Núcleo:** transtornos do neurodesenvolvimento do DSM-5-TR e da CID-11 (ex.: TEA, TDAH, transtornos específicos de aprendizagem com subtipos de leitura, escrita e matemática, transtorno do desenvolvimento da coordenação, transtornos de comunicação e linguagem, transtornos de tique, deficiência intelectual).
- **B. Ampliada:** condições frequentemente incluídas no conceito de neurodiversidade (ex.: altas habilidades/superdotação, dupla excepcionalidade, diferenças de processamento sensorial, transtorno do processamento auditivo, síndromes genéticas com perfil cognitivo característico).
- **C. Limítrofe/contestada:** condições que alguns autores incluem e outros não (ex.: TOC, epilepsia, transtornos de humor, síndrome alcoólica fetal). Para cada uma, explique a controvérsia em uma frase e cite quem defende cada lado.

Para cada condição, informe: nome em português e inglês, códigos DSM-5-TR e CID-11, e se faz parte do público-alvo da educação especial no Brasil (Decreto 12.686/2025 e alterações) ou de outra lei (ex.: Lei 14.254/2021 para dislexia e TDAH).

Não omita condições por serem raras. Se tiver dúvida se algo deve entrar, inclua na camada C e justifique.

## Etapa 2: Ficha de evidências por condição
Para cada condição das camadas A e B, preencha:
1. **Prevalência** em idade escolar: valor, intervalo de confiança, faixa etária, país ou região, número de estudos e participantes, e razão entre meninos e meninas. Priorize meta-análises globais e, separadamente, dados brasileiros (Censo Escolar/Inep, IBGE, estudos nacionais).
2. **Comorbidades mais frequentes** com taxas.
3. **Barreiras de aprendizagem documentadas:** quais funções cognitivas e habilidades escolares são afetadas (ex.: memória de trabalho, decodificação, senso numérico, atenção sustentada, linguagem pragmática), com tamanho de efeito quando houver.
4. **Intervenções e adaptações com evidência:** o que melhora a aprendizagem, com tamanho de efeito (d, g ou SMD), intervalo de confiança, número de estudos e público. Destaque as que podem ser aplicadas em uma plataforma digital.
5. **O que NÃO funciona ou é mito:** intervenções populares sem evidência ou com evidência negativa (ex.: estilos de aprendizagem, fontes "especiais", treino cognitivo sem transferência).
6. **Sinais mensuráveis em ambiente digital:** comportamentos observáveis numa plataforma (tempo de resposta, variabilidade, padrão de erro, uso de apoios, abandono) com evidência de associação. Deixe explícito que esses sinais NÃO servem para diagnóstico e cite estudos sobre a especificidade deles.
7. **Recomendações práticas** para o professor e para a família, apenas as que tiverem respaldo em diretrizes oficiais (NICE, AAP, MEC, EEF, What Works Clearinghouse, NCAEP etc.).

## Etapa 3: Síntese transversal
- Quadro **condição × barreira funcional**, mostrando quais barreiras são compartilhadas entre condições. Ele vai servir para construir perfis por barreira, que lidam bem com comorbidade.
- Lista das **10 adaptações com melhor relação evidência/aplicabilidade digital**, ordenadas por força de evidência.
- Lista das **métricas digitais mais defensáveis** cientificamente.

# REGRAS DE FONTES (OBRIGATÓRIAS)
1. **Hierarquia de evidência:** (1) meta-análises e revisões sistemáticas (Cochrane, Campbell); (2) ensaios clínicos randomizados; (3) estudos de coorte e populacionais; (4) diretrizes clínicas e educacionais oficiais; (5) estudos primários menores, somente se não houver nada melhor, sinalizados como evidência fraca.
2. **Bases preferenciais:** PubMed/MEDLINE, Cochrane Library, Campbell Collaboration, ERIC, PsycINFO/APA PsycNet, SciELO (para dados brasileiros), Google Scholar (só para localizar o artigo; cite a publicação original). Para dados do Brasil: Inep, IBGE, MEC, Diário Oficial.
3. **Recência:** priorize 2015 em diante. Estudos anteriores só se forem marcos ainda não superados, e indique isso.
4. **Toda afirmação numérica** deve ter: autores, ano, título, periódico e **DOI ou link direto**. Sem DOI ou link verificável, não use o número.
5. **Transcreva o número exatamente** como aparece no artigo (valor, IC, n). Não arredonde, não combine estudos por conta própria e não calcule médias entre estudos diferentes.
6. **Proibido inventar.** Se não encontrar um dado, escreva "NÃO ENCONTRADO" e diga onde procurou. É preferível uma ficha incompleta e honesta a uma completa e inventada.
7. **Grau de confiança** para cada dado: ALTO (meta-análise recente e consistente), MÉDIO (poucos estudos ou alta heterogeneidade), BAIXO (estudo único, amostra pequena ou só resumo lido).
8. Indique se você leu o **texto completo** ou só o **resumo** de cada fonte.
9. Se os estudos divergirem, apresente as estimativas divergentes lado a lado e explique por quê (critério diagnóstico, país, método).
10. Diferencie claramente **prevalência diagnosticada** (registros administrativos, ex.: Censo) de **prevalência estimada** (estudos populacionais com triagem).

# FORMATO DE SAÍDA
1. **Sumário executivo** (até 10 linhas) com os achados mais importantes para um produto educacional.
2. **Tabela-mestre da taxonomia:** Condição | Camada (A/B/C) | DSM-5-TR | CID-11 | Prevalência (fonte) | Enquadramento legal no Brasil.
3. **Uma ficha por condição** com as seções 1 a 7 da Etapa 2, cada dado seguido de [Autor, ano, DOI | confiança | texto completo ou resumo].
4. **Síntese transversal** da Etapa 3.
5. **Lacunas de evidência:** o que a ciência ainda não sabe e que a plataforma poderia ajudar a medir.
6. **Bibliografia completa** em formato APA, com DOI.

# VERIFICAÇÃO FINAL (faça antes de entregar)
- Releia cada número e confirme que ele aparece na fonte citada.
- Remova qualquer dado sem DOI ou link.
- Confirme que nenhuma métrica digital está sendo apresentada como ferramenta de diagnóstico.
- Liste no final quais fichas ficaram incompletas e por quê.

Se a resposta ficar longa demais para uma única mensagem, entregue primeiro a Etapa 1 completa e a ficha das condições da camada A, e me pergunte se deve continuar com a camada B.
