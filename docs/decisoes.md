# Decisões técnicas e de produto

Cada decisão com o motivo e a alternativa que foi descartada. As primeiras foram tomadas pela equipe ao planejar o
projeto (prompts 01–14 do João, em `docs/historico_prompts/joao.md`); as outras surgiram durante a construção.

## Base técnica

| Decisão | Por quê | Alternativa descartada |
|---|---|---|
| **Python + Django 5.2** | Login, permissões, admin e formulários prontos; a equipe conhece Python | Next.js + Supabase: mais peças e a equipe não domina JavaScript |
| **Páginas renderizadas pelo Django + Tailwind via CDN**, sem framework JavaScript | Menos peças, menos coisas para quebrar e para explicar | React/Vue: exigiria API, build e outro deploy |
| **SQLite no computador, Postgres (Neon) em produção**, trocados só pela `DATABASE_URL` (`dj-database-url`) | Postgres grátis e fácil de conseguir; o código não muda entre os dois | MySQL: pensado no início, trocado por ser mais difícil de hospedar grátis |
| **Sem LangChain**: o SDK do provedor e um montador de prompt próprio | O app só monta um prompt por blocos e faz uma chamada com saída JSON; o SDK resolve em poucas linhas e é fácil de explicar | LangChain valeria para busca em documentos (RAG), agentes com ferramentas, memória de chat ou vários provedores, que o app não usa |
| **Saída estruturada da IA** (`response_schema` com Pydantic: `conteudo` + `enunciados`) | A resposta já chega validada; o app confere ainda que veio um enunciado por questão | Pedir texto livre e "recortar" a resposta: frágil |
| **Só `ia/cliente.py` conhece o provedor de IA** | Trocar de modelo ou de empresa é mexer em um arquivo | Chamadas ao SDK espalhadas pelo código |
| **Deploy no Render** com `render.yaml` + `build.sh` (gunicorn, WhiteNoise, `collectstatic`, `migrate`) | Publica direto do GitHub a cada push; WhiteNoise serve o CSS/JS sem servidor extra | Vercel: feita para apps Node |
| **Tempo-limite do gunicorn em 120 s** | Gerar uma versão com a IA pode passar dos 30 s padrão | Gerar em segundo plano com fila: mais complexo do que o necessário para a v1 |
| **Configuração por variáveis de ambiente** (`.env` local, painel do Render em produção) | Nenhum segredo no código ou no histórico do Git | Arquivo de configuração no repositório |
| **Nomes do domínio em português** (modelos, telas, URLs); o resto em inglês | A banca e a equipe entendem o domínio na hora | Tudo em inglês |

## Produto e regras do app

| Decisão | Por quê |
|---|---|
| **Três apoios de conteúdo viram uma máscara de 3 bits** (`foco×4 + textual×2 + concreto×1`) | Toda combinação de apoios vira um número de 0 a 7: no máximo 7 versões geradas por aula, não uma por aluno. Na combinação, vale a regra mais restritiva (bloco `conflitos.md`) |
| **Máscara 0 é a aula original e não chama a IA** | Quem não precisa de apoio vê o texto do professor, sem custo nem risco |
| **Cache: uma versão por (aula, máscara)**, garantida no banco por restrição única | Gera uma vez e reaproveita para todos os alunos com a mesma combinação |
| **O professor aprova cada versão, e pode corrigi-la, antes de o aluno ver** | A IA pode errar; quem responde pela aula é o professor. Até a aprovação, o aluno vê a original |
| **A IA reescreve só o texto e os enunciados; alternativas e gabarito são sempre do professor** | A correção nunca depende da IA. Testes garantem que gerar uma versão não altera `Questao` |
| **Editar a aula apaga as versões adaptadas; aula com respostas não pode ser editada** | Versões antigas não valem para um texto novo, e mudar o gabarito depois das respostas deixaria correções erradas |
| **Nenhum dado do aluno vai para a IA**: só os bits e a aula, entre as tags `<aula>` e `<questoes>` | LGPD (dado de criança). As tags e a regra do bloco base fazem o texto da aula ser tratado como conteúdo, nunca como instrução |
| **Sem laudo e sem diagnóstico**: a família responde 6 perguntas sobre o dia a dia | Laudo é dado sensível de criança e não deve ser condição para receber apoio. As respostas descrevem barreiras, não condições médicas |
| **Respostas da família viram sugestões, não mudanças** | O professor tem a palavra final. Um apoio é sugerido quando a soma das duas perguntas dele chega a 2 (uma "com frequência" ou duas "às vezes") |
| **Um só tipo de sugestão para o questionário e para o uso** (`SugestaoPerfil`, aceitar ou recusar) | O professor revisa tudo no mesmo lugar. Sugestão recusada não volta a aparecer |
| **O professor cria os logins de aluno e de família** | Escola não depende de e-mail de criança; menos dados coletados |
| **Apoios de leitura sem IA**: fonte OpenDyslexic, leitura em voz alta e modo limpo, numa barra para qualquer aluno | Não custam nada, não rotulam ninguém e ajudam a turma toda (Desenho Universal para a Aprendizagem) |
| **Padrão no perfil + escolha do aluno na sessão** | O professor define o que já vem ligado; o aluno liga e desliga quando quiser. Se ele liga o mesmo apoio 3 vezes, o professor recebe a sugestão de deixá-lo ligado |
| **Leitura em voz alta pela Web Speech API do navegador** | Sem custo, sem servidor e sem enviar o texto para fora. O texto é lido em frases curtas, porque alguns navegadores cortam falas longas |
| **OpenDyslexic pelo CDN** (pacote Fontsource no jsDelivr, licença SIL OFL) | Mesmo critério do Tailwind: nada de arquivo binário no repositório |
| **Painel calculado na hora, a partir das respostas e dos registros de uso** | Mostra só o que foi medido de verdade. Cada resposta guarda a versão que o aluno viu, para comparar acertos entre a original e as adaptadas. Métricas de "foco" ou "retenção" ficaram de fora porque o app não tem como medi-las |
| **Tempo de resposta medido no servidor** (hora em que a aula abriu, guardada na sessão) | Não depende de JavaScript nem do relógio do aluno |

## Pendente

| Assunto | Situação |
|---|---|
| **Provedor de IA** | Os termos da Gemini API (gratuita e paga) proíbem usar a API em apps voltados a menores de 18 anos. O código está pronto para o Gemini, mas a geração só deve ir ao ar com um provedor cujos termos permitam o uso em educação básica. Como só `ia/cliente.py` conhece o provedor, a troca mexe em um arquivo |
| **Textos pedagógicos** | Os blocos de `ia/blocos/` e as 6 perguntas do questionário (`apps/perfis/questionario.py`) estão com textos provisórios até a revisão do Cauã |
