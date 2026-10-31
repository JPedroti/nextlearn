# Riscos legais e regulatórios no Brasil (v1, 31/10/2026)

> **Pesquisa de base, anterior à versão final do produto.** O app seguiu as conclusões principais: sem laudo, dados
> mínimos, o aluno não conversa com a IA e o professor aprova tudo. O índice dos documentos está em
> [README.md](README.md).

> Levantamento para o produto (plataforma para alunos neurodivergentes de 6 a 18 anos, vendida a escolas).
> **Não é parecer jurídico.** Antes de operar com dados reais, validar com advogado de proteção de dados e educação.

## Resumo: os 3 riscos que podem travar o produto
1. **Diretrizes do CNE sobre IA na educação (Parecer CNE/CP nº 15/2026):** até o 5º ano, o aluno **não pode usar sozinho** ferramentas de IA adaptativas ou conversacionais; decisões automatizadas sobre a trajetória do aluno e reconhecimento de emoções ficam **proibidos**; IA **não pode corrigir redação nem prova dissertativa**.
2. **LGPD — dado de saúde de criança:** o laudo e o perfil de neurodivergência são **dados pessoais sensíveis** de menores. Esse é o tipo de tratamento mais protegido da lei, e o uso de API de IA estrangeira vira **transferência internacional**.
3. **ECA Digital (Lei 15.211/2025):** limita mecânicas de engajamento (recompensa por tempo de uso, notificações em excesso, loot boxes) e exige configuração protetiva por padrão e controle parental.

---

## Matriz de riscos

| # | Norma | O que diz (relevante para nós) | Impacto no produto | Gravidade | Mitigação |
|---|---|---|---|---|---|
| 1 | **Diretrizes do CNE sobre IA na educação** — Parecer CNE/CP nº 15/2026, aprovado em 01/09/2026; súmula publicada no DOU em 06/10/2026. **Conferir se a resolução já foi homologada.** Vale para escolas públicas e privadas; 12 meses de adequação após a homologação, mas as proibições valem de imediato | **Até o 5º ano:** sem acesso direto e sem supervisão a IA generativa, conversacional, preditiva ou adaptativa; só em atividade planejada e mediada pelo professor, sem coleta desnecessária de dados; famílias informadas. **Proibido (risco excessivo):** IA corrigindo prova de interpretação subjetiva (redação, dissertativa), sanção acadêmica sem supervisão, pontuação social, reconhecimento de emoções, **decisões sobre a trajetória educacional do aluno**, uso de dados para publicidade. **Alto risco (supervisão contínua):** correção automatizada, monitoramento biométrico. Objetivas podem ser corrigidas automaticamente com validação humana. Escolas devem divulgar os sistemas automatizados usados e garantir revisão humana | O "tutor de IA" e a trilha adaptativa autônoma **não podem ser usados sozinhos por alunos do 1º ao 5º ano**. A adaptação não pode "decidir" o percurso: precisa ser recomendação aprovada pelo professor | 🔴 Alta | (a) Do 1º ao 5º ano: o aluno usa só em atividade mediada (professor ou família junto); sem chatbot livre. (b) Toda mudança de trilha = **sugestão que o professor aprova**. (c) Só itens objetivos corrigidos automaticamente, com validação humana. (d) Nada de webcam nem análise de emoção. (e) Página de transparência explicando o que a IA faz |
| 2 | **LGPD (Lei 13.709/2018)**: art. 11 (dados sensíveis) e art. 14 (crianças e adolescentes); **Enunciado CD/ANPD nº 1/2023** | Dado de saúde é sensível. Dados de crianças e adolescentes exigem o **melhor interesse** do titular. O Enunciado 1/2023 permite usar outras bases legais além do consentimento dos pais, desde que prevaleça o melhor interesse | Laudo, perfil funcional e telemetria de aprendizagem de menores = tratamento de alto risco. Vazamento ou uso indevido é o pior cenário possível para uma edtech | 🔴 Alta | Laudo **opcional** e guardado separado e criptografado; **consentimento específico e destacado** dos pais para dados de saúde; minimização (o perfil guarda "barreiras", não o CID); Relatório de Impacto (RIPD); encarregado de dados (DPO); contrato escola–empresa definindo papéis (a escola como controladora, nós como operadores) |
| 3 | **Resolução CD/ANPD nº 2/2022** (agentes de pequeno porte) | Startups têm regime simplificado (documentos simples, prazos maiores), **exceto** se fizerem tratamento de alto risco | Por tratar dados sensíveis de crianças, a startup provavelmente **não terá** o regime simplificado | 🟡 Média | Assumir desde o início as obrigações completas da LGPD (registro das operações, RIPD, DPO, plano de incidentes) |
| 4 | **Resolução CD/ANPD nº 19/2024** (transferência internacional) | Desde 23/08/2025, enviar dados pessoais ao exterior por contrato exige as **cláusulas-padrão da ANPD**. Não há decisão de adequação publicada para nenhum país | Usar API de IA hospedada nos EUA (ou em outro país) com dados dos alunos = transferência internacional | 🟡 Média | Pseudonimizar antes de enviar ao modelo (sem nome, CPF, escola ou laudo no prompt); contratar provedor que aceite as cláusulas-padrão ou que hospede no Brasil; registrar a transferência no RIPD |
| 5 | **ECA Digital (Lei 15.211/2025)**, em vigor desde 17/03/2026, + Decreto 12.880/2026 | Configuração mais protetiva como padrão (art. 7º); proibido perfilamento para publicidade (art. 22); **loot boxes proibidas** (art. 20); o decreto trata como risco **recompensas atreladas ao tempo de uso**, notificações em excesso, autoplay e ocultar pontos de parada; supervisão parental com limite de tempo (arts. 17 e 18); gestão de riscos (art. 8º). Multa de até 10% do faturamento, limitada a R$ 50 mi | Restringe a gamificação "estilo Duolingo" | 🟡 Média | Gamificação por **domínio**, não por tempo; ofensiva semanal sem punição; no máximo 1 notificação por dia; painel da família com limite de tempo; zero publicidade |
| 6 | **Decreto 12.686/2025** (alterado pelo 12.773/2025): Política Nacional de Educação Especial Inclusiva | AEE e profissional de apoio **não podem depender de laudo**; PAEE é documento pedagógico; estudo de caso é a metodologia obrigatória | Um produto que exige laudo para funcionar contraria a política | 🟡 Média (já resolvido no desenho) | Perfil funcional por barreiras, laudo opcional; a plataforma **apoia** o PAEE e o estudo de caso, não substitui o professor do AEE |
| 7 | **Lei 4.119/1962 + Resolução CFP nº 31/2022** (testes psicológicos) e **Lei 12.842/2013** (Ato Médico) | Uso de testes psicológicos é privativo de psicólogos (instrumentos aprovados no SATEPSI). O diagnóstico nosológico é atividade privativa médica | Se a plataforma "diagnosticar" ou aplicar escalas psicológicas, configura exercício irregular | 🟡 Média | Nunca dizer "diagnóstico", "triagem de TDAH" etc. O questionário é **pedagógico** (barreiras observadas em sala), não teste psicológico. Métricas digitais nunca rotulam condições |
| 8 | **Lei 15.100/2025** (celulares nas escolas) | Proíbe celular e tablet do aluno durante todo o período escolar, inclusive no recreio, nas redes pública e privada. **Exceções:** uso pedagógico orientado pelo professor, **acessibilidade e inclusão**, condições de saúde | O aluno não usa o app no celular dele livremente na escola | 🟢 Baixa | Uso na escola só em atividade pedagógica (equipamento da escola ou aula orientada); a exceção de acessibilidade e inclusão favorece justamente nosso público; o grosso do uso individual fica em casa |
| 9 | **PL 2.338/2023** (Marco Legal da IA) — aprovado no Senado em 10/12/2024, parado em comissão especial na Câmara (sem parecer em out/2026) | Ainda **não é lei**. O texto do Senado coloca "seleção de estudantes" como alto risco; para alto risco: avaliação de impacto algorítmico, explicação, contestação e revisão humana. Vigência 730 dias após publicação | Risco futuro; pode ampliar a lista de alto risco para educação | 🟢 Baixa hoje | Já desenhar com explicabilidade ("por que a plataforma sugeriu isso"), revisão humana e registro das decisões |
| 10 | **Lei Brasileira de Inclusão (Lei 13.146/2015)**, art. 63 | Sites de empresas com sede no Brasil devem ser acessíveis | A própria plataforma precisa ser acessível | 🟢 Baixa (e é diferencial) | Seguir WCAG 2.2 AA no mínimo (já previsto nos perfis) |
| 11 | **Publicidade infantil**: Resolução Conanda 163/2014, CDC (art. 37) e ECA Digital (art. 22) | Publicidade dirigida a crianças é considerada abusiva | Proíbe monetizar com anúncios ou ofertas para o aluno | 🟢 Baixa | Modelo B2B (a escola paga), sem anúncios e sem vendas dentro do app para o aluno |

---

## O que muda no produto por causa disso
1. **Por etapa:** do 1º ao 5º ano, o produto é uma **ferramenta do professor e da família** (atividades mediadas, sem chatbot). A partir do 6º ano, o aluno ganha mais autonomia, sempre com professor supervisionando as trilhas.
2. **Toda decisão da IA é sugestão:** o professor aprova mudanças de trilha e de adaptação. Isso cumpre o CNE e o futuro Marco da IA, e é um argumento de venda ("o professor no controle").
3. **Privacidade por padrão:** laudo opcional e separado; perfil por barreiras; prompts pseudonimizados; nenhum dado biométrico.
4. **Gamificação limpa:** medalhas por domínio, ligas por equipe, sem loot box, sem recompensa por tempo e sem pressão de notificação.

## Como usar isso no pitch
"Fomos desenhados para a regulação de 2026: cumprimos as diretrizes do CNE para IA, a LGPD para dados de crianças, o ECA Digital e o novo decreto da educação inclusiva. Concorrentes que corrigem redação com IA ou exigem laudo vão ter que se adaptar; nós já nascemos adequados."

## Fontes
- O Tempo (01/09/2026): CNE veta uso de IA sem supervisão até o 5º ano
- Antihype: diretrizes do CNE, correção de redação e faixas de risco
- ABMES: súmula do Parecer CNE/CP nº 15 (DOU 06/10/2026) e coluna sobre o prazo de 1 ano
- Felsberg Advogados: Enunciado CD/ANPD nº 1/2023
- Lefosse: prazo das cláusulas-padrão (Resolução ANPD 19/2024)
- Demarest: Resolução CD/ANPD nº 2/2022
- Machado Meyer: factsheet do ECA Digital
- Agência Senado: Lei 15.100/2025
- CFP: Resolução nº 31/2022
- Merovian: status do PL 2.338/2023
- ANEC / Câmara: Decreto 12.686/2025
