# Histórico de prompts — Hackathon LEPV × FGV (Teachy) — Out/2026

**Equipe:** João, Thiago, Cauã, Gabriel Franco (IME, 4º período)
**Ferramenta de IA:** Claude (Anthropic)

Registro cronológico e literal de todos os prompts enviados à IA durante o hackathon, mantido para consulta da banca avaliadora.

---

## Prompt 01 — 30/10/2026, 19:31 (BRT) — autor: João

**Anexos:** `Manual Oficial do Participante (v1.1).pdf`; `Desafios da educação brasileira — Teachy.pdf`

> Sou aluno do segundo ano do IME (quarto período) e estou fazendo um hackathon com mais três alunos da minha turma que estão no meu grupo:
> João (Eu)
> Thiago
> Cauã
> Gabriel Franco.
> O evento está sendo feito pela lepv (liga de empreendendorismo da praia vermelha) que foi criada por alunos do IME. Mandaram isso aqui na época de inscrição, junto com o manual que está anexo ao prompt.
> """
> 🚀 VEM AÍ O 1º HACKATHON LEPV & FGV!
>
> Nos dias 30 e 31 de outubro, na FGV (Praia de Botafogo), estudantes vão formar equipes para identificar um problema real e construir a melhor solução para ele, em uma experiência intensa de criatividade, colaboração e empreendedorismo.
>
> 📚 Tema desta edição: Educação
> 🧠 Mentoria com profissionais do mercado
> 🏆 Prêmio de R$ 1.100 por integrante do grupo vencedor
> 🦜 Patrocínio: Teachy
>
> ⚠️ Atenção: as inscrições oficiais são feitas exclusivamente pelo nosso site. Mesmo quem já fez a pré-inscrição precisa confirmar a inscrição por lá.
>
> 👉 Garanta sua vaga: https://lepv.org/evento.html?t=97446f6cdba902a4
> """
> Entretanto, isso já tem muito tempo e, agora que o hackathon começou, enviaram o pdf de Desafios, anexo também ao prompt. Explore os documentos e pergunte qualquer dúvida que você tiver sobre a situação para, depois, podermos começar o brainstorming.
>
> Um adendo importante: todos prompts devem ser guardados em algum lugar para que esse histórico fique disponível para a banca avaliadora.
>
> Como explicado nos slides de apresentação do hackathon (Ainda não tenho, mas daqui a pouco eles vão disponibilizar o arquivo e eu já te mando), se ficarmos entre os 5 melhores na FASE 1, pelo que me lembro, teremos que fazer um pitch para uma banca com os "grandes caras" da teachy (vulgo CEO e sócios), o que seria a FASE 2. Entretanto, para passarmos na FASE 1, teremos que ser avaliados por agentes de IA deles que tem os critérios de correção.

**Resumo da resposta da IA:** leitura dos dois documentos, levantamento de pontos de atenção e perguntas de esclarecimento antes do brainstorming.

---

## Prompt 02 — 30/10/2026, 19:56 (BRT) — autor: João

**Anexos:** pasta do projeto com `abertura-hackathon-lepv.pdf` (slides de abertura)

> Tinha esquecido de adicionar uma pasta para você gerenciar e poder colocar o histórico de prompts. Além disso, nessa pasta estão os slides com as orientações do desafio. ("abertura-hackathon-lepv.pdf") Estávamos pensando em focar em uma das perguntas. Essa foi uma orientação de um dos "grandes caras" de venture capital que estão patrocinando o evento. Ele falou para gente que temos pouco tempo para resolver e que, talvez, seja melhor focarmos em uma solução funcional e que resolva alguns problemas/gargalos bem ao invés de tentar resolver tudo e criar um "canivete" que nenhuma das soluções resolve bem. Estávamos pensando em resolver a pergunta 4: "Como podemos ajudar cada aluno a aprender com conteúdos que façam sentido para sua realidade e se adaptem ao seu progresso?". A ideia era, além de utilizar técnicas de gameficação e etc (que todo mundo provavelmente vai fazer, como tem no teachy, no khan academy e no Kapi (uma startup que eu encontrei no linkedin de um aluno de faculdade de uns 19 anos)) que é algo que resolve parcialmente a pergunta 2 "Como podemos ajudar a despertar no aluno o gosto por aprender e a vontade de se dedicar ao conteúdo, dentro e fora de sala de aula?" (que trata do engajamento) nós meio que fazermos um produto que identifica o perfil do estudante e faz tudo direcionado nesse perfil dele, que é gerado de acordo com o que ele erra nos exercícios/provas, somado com possíveis laudos de neurodivergência, etc. A ideia central é que cada um é um individuo e, com base nos slides do desafio, às vezes cada individuo aprende num ritmo diferente e, portanto, estariamos tentando resolver esse descompasso entre os estudantes por meio da identificação do perfil e dos gargalos do indivíduo.

**Resumo da resposta da IA:** leitura dos slides de abertura (regras, entregas da Fase 1, critérios por pilar, jogo limpo); correção do cronograma (submissão às 13h de sábado); análise crítica da ideia para o desafio 4 — manter o diagnóstico pelo erro como núcleo, trocar "perfil/estilo de aprendizagem" por diagnóstico de habilidades, tratar laudos com cuidado (LGPD, dado sensível de menor), incluir a metade "realidade do aluno" (contextualização) que faltava, colocar o professor no circuito e reduzir o escopo a uma disciplina/série.

---

## Prompt 03 — 30/10/2026, 20:28 (BRT) — autor: João

> 1. Podem continuar trabalhando em casa hoje depois das 21h? Isso muda bastante quanto dá para construir. R: Sim. Vamos tentar virar à noite.
> 2. Qual stack vocês dominam para colocar no ar rápido? Se não houver preferência, sugiro Next.js na Vercel com a API de um LLM. R: Não dominamos nada, mas conseguimos fazer com IA. Eu tenho o Claude Pro, Thiago tem Claude Pro, Caua tem qwen pro e Gabriel tem ChatGPT pro.
> 3. Topam dividir assim, com o 4º ajudando onde apertar?
>    * 2 pessoas no app;
>    * 1 no plano de negócio em PDF;
>    * 1 em pedagogia, banco de questões e roteiro do vídeo.
>
> R: Não entendi sua pergunta.
>
> 1. O ajuste de "perfil" para "diagnóstico do erro + contextualização" faz sentido para vocês, ou o perfil tem algo que eu não captei?
>
> R: O perfil estamos fazendo um brainstorming, mas a ideia é utilizarmos os dados que criamos dos alunos e poder fazer coisas personalizadas, como plano de estudos, simulados, etc.

**Resumo da resposta da IA:** explicação da divisão de tarefas com sugestão de nomes; "perfil" redefinido como mapa de aprendizagem (domínio por habilidade + erros recorrentes + interesses + adaptações) que alimenta plano de estudos e simulados; proposta de conceito v1 do NextLearn para o brainstorming; escolha de stack (Next.js + Vercel + Supabase + API gratuita de LLM); cronograma até a submissão das 13h; orientação para registrar os prompts dos quatro integrantes, em todas as ferramentas de IA.

---

## Prompt 04 — 30/10/2026, 22:20 (BRT) — autor: João

> Discutimos muito e mudamos bastante o rumo e nossa ideia. Abaixo temos um resumo. Quero que você veja se o planejamento e a ideia fazem sentido com a proposta do hackathon e com os desafios propostos (não vamos "atacar" todos os desafios):
> """
> Resumo Executivo da Solução (Visão e Arquitetura Unificadas)
>
> Queremos criar uma plataforma de educação específica para neurodivergentes com o objetivo de resolver a dor do aprendizado no ambiente escolar, conectando ativamente a tríade formada por alunos, escolas e famílias. Para o aluno, a plataforma responde à pergunta sobre quais atitudes e métodos adaptativos ele pode adotar para melhorar sua retenção e foco com o auxílio da tecnologia. Para a escola — incluindo professores e coordenadores —, a solução fornece ferramentas práticas e inteligência para que o conteúdo das aulas seja compreendido por estudantes com diferentes perfis cognitivos. Para a família, a plataforma oferece clareza e orientações sobre como criar um ambiente favorável de estudos em casa e como acompanhar a evolução do filho.
>
> Essa solução será comercializada no modelo SaaS para instituições de ensino. O ponto de partida da experiência ocorre com a inclusão de um laudo médico ou com o preenchimento de um questionário interativo de onboarding. A partir desses dados iniciais, o sistema categoriza o estudante em um grupo de perfil funcional de aprendizagem. No MVP da plataforma, esses perfis são consolidados em três eixos principais: o Perfil de Atenção e Foco (focado em Clean UI, redução de sobrecarga sensorial e fatiamento de tarefas), o Perfil de Acessibilidade Textual (com recursos de Text-to-Speech, fontes adaptativas como OpenDyslexic e simplificação semântica via IA para dislexia) e o Perfil Interativo e Concreto (baseado em gamificação, representação visual de conceitos abstratos e tutores conversacionais por áudio).
>
> Tecnicamente, a plataforma é estruturada sobre um backend robusto em Python com o framework Django, aproveitando seu sistema nativo de autenticação e permissões para segregar com segurança os acessos das três pontas (Aluno, Professor e Família). O armazenamento de dados utiliza o banco de dados MySQL, garantindo suporte a transações concorrentes (row-level locking) para evitar race conditions durante o envio simultâneo de respostas, métricas e atualizações de aulas.
>
> O coração da personalização reside em um motor de Inteligência Artificial orquestrado via LangChain. Essa engrenagem recebe o conteúdo pedagógico bruto inserido pelo professor e o perfil dinâmico do aluno (armazenado em formato JSON/Markdown no banco de dados), injetando-o no prompt da LLM para adaptar o método e o formato da aula em tempo real. Por fim, a plataforma implementa um ciclo contínuo de retroalimentação: a partir dos dados de uso coletados durante a resolução de exercícios e da medição de métricas de desempenho (como retenção, tempo de tela, tempo de resposta e nível de foco), o backend atualiza dinamicamente o arquivo de perfil do aluno no MySQL. Dessa forma, a cada nova interação, a IA refina suas respostas e adapta a interface, entregando um método de aprendizagem hiper-personalizado e continuamente aprimorado para cada estudante.
> """

**Resumo da resposta da IA:** avaliação da nova ideia frente aos desafios e aos 4 pilares — encaixe forte no Desafio 1 (o professor prepara o conteúdo uma vez e a IA adapta para cada aluno); riscos: escopo de "canivete", enquadramento "só para neurodivergentes" contra o princípio "junto com a turma", upload de laudo (LGPD), métricas de "foco" sem como medir, perfis em 3 caixas fixas, stack superdimensionada (MySQL/LangChain/locking). Proposta de corte do MVP, ajustes de posicionamento (Desenho Universal para a Aprendizagem) e argumento de negócio (LBI, art. 28).

---

## Prompt 05 — 30/10/2026, 22:28 (BRT) — autor: João

> E se fizermos 2^3 -1 perfis, pegando as intercessoes de quando o aluno se enquadra em mais de um grupo (o -1 é quando ele nao tem nada, que nao queremos trabalhar com isso)

**Resumo da resposta da IA:** a ideia funciona como uma máscara de 3 bits, e cada combinação gera uma versão adaptada guardada em cache. Sugestões: manter o caso "nenhum" como versão base da turma (princípio de inclusão); separar adaptações de conteúdo (que usam a IA e formam a máscara) das adaptações de interface (CSS/navegador, sem custo de IA); definir regras de precedência para combinações conflitantes.

---

## Prompt 06 — 30/10/2026, 22:31 (BRT) — autor: João

> E se considerarmos uns 30 tipos de neurodivergencia, e associarmos cada tipo a um ON/OFF de cada um dos tres grupos propostos. Por exemplo, autismo de nivel mais alto poderia ser 1,1,1 (estou chutando apenas para exemplo), um autismo mais leve teria menos grupos, tipo 1,1,0 etc

**Resumo da resposta da IA:** a tabela diagnóstico→bits só serve como sugestão inicial editável, não como regra. O mesmo diagnóstico gera necessidades diferentes, a tabela traz de volta a dependência do laudo e os 30 tipos exigiriam validação por especialista, o que não cabe no tempo. Proposta: questionário funcional como fonte principal e tabela pequena (cerca de 5 condições do deck) só para pré-preencher, sempre revisada pelo professor e ajustada pelo uso.

---

## Prompt 07 — 30/10/2026, 22:36 (BRT) — autor: João

> E se tivermos os três grupos que tínhamos proposto primeiro mas os pais preencherem quais grupos eles querem que os filhos tenham atendimento especializado, sem necessidade do diagnóstico em algum caso de neuro divergência?

**Resumo da resposta da IA:** ideia aprovada (sem exigir diagnóstico, com a família como fonte das necessidades, alinhada à LGPD e à inclusão). Ajustes: os pais respondem perguntas sobre o comportamento em vez de escolher o nome do grupo; o professor revisa e também pode sugerir; o uso real ajusta os bits; evitar o termo "atendimento especializado" (AEE tem sentido legal próprio). Desenho dado como fechado; próximo passo é escolher a stack e criar o repositório.

---

## Prompt 08 — 30/10/2026, 22:41 (BRT) — autor: João

> Aceitamos os seus tres ajustes. Agora, só temos algumas duvidas:
>
> 1. Foi uma boa ideia pro hackathon? Seja sincero e procure gargalos.
> 2. Como poderiamos dividir as tarefas no grupo? (queriamos dividir em duas duplas)
> 3. Sugestao de repositorio organizado com estrutura de pastas, fácil de entender e que siga notas de boa prática, lembrando que estamos utilizando python, django, mysql e langchain. (veja se faz sentido usarmos essas ferramentas também)
> 4. Dê o roteiro vertical do projeto pelo menos para a versao v1.0

**Resumo da resposta da IA:** avaliação franca (ideia boa; riscos em originalidade, prova de impacto, qualidade da adaptação feita pela IA, deploy e infraestrutura das escolas, com mitigações); divisão em Dupla Produto (João + Thiago) e Dupla Conteúdo & Negócio (Cauã + Gabriel), com pontos de sincronização; avaliação da stack (Django sim; Postgres no lugar de MySQL por causa do deploy gratuito; LangChain dispensável); estrutura de repositório e modelos de dados; roteiro em fatias verticais até a v1.0, com ordem de corte e congelamento às 10h30.

---

## Prompt 09 — 30/10/2026, 22:47 (BRT) — autor: João

> mas pra eu fazer gerenciamento de contexto da IA, system prompt e inclusao do professor + aluno nos prompts mesmo assim vc recomenda sem langchain?

**Resumo da resposta da IA:** continua sem LangChain. O que o projeto precisa (system prompt montado por blocos, contexto do professor e do perfil do aluno, saída em JSON) é composição de texto e uma chamada ao SDK. Foi mostrado um esboço de `prompt_builder.py` e `cliente.py` e listados os casos em que o LangChain valeria a pena (RAG, agentes com ferramentas, memória de chat, troca de provedores).

---

## Prompt 10 — 30/10/2026, 22:54 (BRT) — autor: João

> Como devemos separar as tarefas para cada integrante do grupo por horario?

**Resumo da resposta da IA:** cronograma por integrante e por bloco de horário, das 23h às 13h, alinhado às fatias verticais. Sono em turnos, com sempre um desenvolvedor acordado; entregas da dupla de conteúdo com prazo; deslocamento para o Instituto 12; congelamento às 10h30 e submissão às 12h; cada integrante registra os próprios prompts ao fim de cada bloco.

---

## Prompt 11 — 30/10/2026, 22:59 (BRT) — autor: João

> Mandei os horários no grupo já. Resumo o projeto para eu mandar no grupo de whatsapp do meu grupo.

**Resumo da resposta da IA:** resumo do projeto em formato de mensagem de WhatsApp (problema, solução, perfis, fluxo, stack, MVP, o que fica fora, divisão das duplas e próximo passo).

---

## Prompt 12 — 30/10/2026, 23:04 (BRT) — autor: João

> Beleza. Já mandei no grupo e cada um já está encarregado da sua atividade. O que devo fazer agora?

**Resumo da resposta da IA:** passos da Fatia 0 para o João: criar o repositório público vazio no GitHub, adicionar os colegas, criar contas no Neon e no Render e guardar a string de conexão; em seguida a IA conecta o repositório e monta o esqueleto Django com a configuração de deploy.

---

## Prompt 13 — 30/10/2026, 23:08 (BRT) — autor: João

> eu já havia criado o repositório e compartilhado com todos do grupo (está no private e no site https://github.com/JPedroti/nextlearn). Queria mandar o contexto para o Claude Code e deixar ele fazer todo esse trabalho. Lembrando que ele teria que receber muita informação antes de delegarmos o trabalho. Ele deveria, por exemplo continuar atualizando o historico de prompts (eu delegaria a mesma pasta que te deleguei para fazer git init e jogar nesse repo remoto)

**Resumo da resposta da IA:** criado o `CLAUDE.md` na pasta do projeto, com todo o contexto (regras do hackathon, produto, decisões técnicas, estrutura, modelos, motor de IA, fatias, equipe, protocolo do histórico de prompts e segurança), e escrito o prompt inicial para o Claude Code. Alertas: o deck da Teachy é confidencial e não pode ir para o repositório; o repositório privado precisa ficar público ou acessível à banca antes da submissão.

---

## Prompt 14 — 30/10/2026, 23:18 (BRT) — autor: João

> Não fomos orientados em relação a essa confidencialidade. Se eu já compartilhei nessa conversa, porque não poderia compartilhar na outra? Não disseram nada à gente em relação à isso e acho que já esperavam que íamos utilizar isso no contexto da IA. Agora que parei para pensar, isso poderia dar problema porque estaria no versionamento do github que vai ser publico no final ne? Voce acha que criar arquivos .md com o conteudo nao resolveria isso?

**Resumo da resposta da IA:** usar o deck como contexto de IA (aqui e no Claude Code, localmente) não tem problema; o risco é publicá-lo no repositório público, e o histórico do Git guarda o arquivo mesmo depois de apagado. Converter para .md não resolve, porque o problema é o conteúdo e não o formato. Solução: PDFs ficam locais em `referencias/` (fora do Git, legíveis pelo Claude Code) e o repositório recebe um `docs/contexto.md` escrito com palavras próprias e com os dados citados das fontes públicas originais. CLAUDE.md atualizado.

---

## Prompt 15 — 30/10/2026, 23:20 (BRT) — autor: João — ferramenta: Claude Code

> Leia o CLAUDE.md inteiro e o historico_prompts.md antes de qualquer coisa. Eu sou o João.
>
> Depois, faça a Fatia 0:
> 1. Registre este prompt no histórico, seguindo o protocolo da seção 9 (mova o historico_prompts.md para docs/ com git mv, depois de inicializar o repositório).
> 2. Mova os PDFs para referencias/ e garanta que essa pasta e *.pdf estejam no .gitignore.
> 3. git init, conecte ao remoto https://github.com/JPedroti/nextlearn.git (verifique antes se o remoto já tem commits e, se tiver, integre sem apagar nada).
> 4. Crie o esqueleto Django conforme as seções 4, 5 e 6 do CLAUDE.md: apps, model Usuario com papel, login/logout, uma página inicial diferente para cada papel, settings lendo variáveis de ambiente, .env.example, requirements.txt, render.yaml (gunicorn + whitenoise + collectstatic + migrate no build), README com instruções para Windows.
> 5. Rode localmente com SQLite, confira que o login funciona e faça commit + push.
> 6. Me passe o passo a passo para criar o serviço no Render apontando para o repositório e configurar as variáveis de ambiente (vou colar a connection string do Neon e a chave do Gemini direto no painel do Render, não no chat).
>
> Explique cada passo em linguagem simples, porque não domino Django.

**Resumo da resposta da IA:** Fatia 0 feita. Repositório iniciado (o remoto estava vazio) e PDFs movidos para `referencias/`, fora do Git. Esqueleto Django 5.2 com os 5 apps, `Usuario` com papel, login/logout e uma página inicial por papel, configuração por variáveis de ambiente, `render.yaml` + `build.sh` (collectstatic, migrate, criação do administrador), README para Windows e 5 testes de login. Build do Render simulado localmente, login conferido no servidor local e passo a passo do Render entregue ao João.

---
