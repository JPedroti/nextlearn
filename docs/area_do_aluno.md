# Login e área do aluno (como funciona hoje)

## Login
- O backend do time já autentica de verdade: `Usuario` (Django) com `papel` = professor, aluno ou família.
- Tela no visual do protótipo: `/prototipo/login/?perfil=aluno|professor|familia` (o perfil só muda o visual: cor e fala do Next).
  Ela usa o `LoginView` do Django; depois do login, `contas:inicio` manda cada um para a sua página pelo papel:
  professor → `/professor/`, aluno → `/aluno/`, família → `/familia/`.
- Não existe cadastro público: o professor cria o aluno e a família na tela da turma (`/professor/turmas/<id>/`).
  O primeiro professor vem do `python manage.py createsuperuser` (ele pergunta o papel).
- Para testar na máquina local: `python manage.py contas_teste` cria `prof.teste`, `aluno.teste` (Davi, fictício, apoio de foco + concreto), `familia.teste`,
  uma turma e uma aula publicada. As senhas ficam em `contas_teste_local.txt` (fora do Git). Só para desenvolvimento,
  nunca na demo oficial. O `rodar_prototipo.bat` roda isso sozinho na primeira vez.

## Área do aluno (backend atual)
1. `/aluno/` lista as aulas **publicadas** da turma do aluno e marca as já respondidas.
2. `/aluno/aulas/<id>/` mostra a aula na **versão do perfil dele**: a máscara de 3 bits do `Perfil`
   (foco, textual, concreto) escolhe a `VersaoAdaptada`; só aparece se o professor **aprovou**. Sem versão aprovada, vê a original.
3. As questões são as mesmas para todos (o gabarito é do professor; a IA só reescreve o enunciado).
4. Ao enviar, cada `Resposta` guarda a alternativa, se acertou e o tempo desde que abriu a aula (`tempo_ms`). Não dá para responder duas vezes.
5. Esses dados voltam para o professor (e viram sugestões de ajuste de apoio, que ele aceita ou recusa).

## Painel do aluno no protótipo (`/prototipo/aluno/inicio/`)
O login do aluno pelo `/prototipo/login/` cai aqui. Lê os dados reais do banco (no teste local, o Davi fictício).
- **Missão de hoje:** a próxima tarefa em destaque, um botão só (apoio de foco: uma ação por vez), com o prazo.
  À direita, o dia do mês em destaque: ao clicar, o **calendário** abre em zoom (aulas feitas, prazos, dias com estudo,
  semanas com a meta, próximos prazos; setas do teclado mudam o dia). Também abre pelo botão "Calendário" do topo,
  pela ofensiva semanal, pelo ícone de cada tarefa e pela página de treino (`#calendario`).
- **Prazo:** o backend ainda não tem prazo; o protótipo usa publicação + 7 dias (valor de produto, a calibrar).
- **Minha média:** comparada com o próprio aluno no mês anterior. Sem ranking.
- **Ofensiva semanal:** semanas seguidas com a meta mínima (2 aulas); semana parada só pausa, não zera.
- **Tempo de estudo:** minutos na semana e hoje, ao lado do limite diário combinado com a família (ECA Digital).
- **Painéis interativos (blocos temáticos):** notas filtradas por matéria (barra clicável mostra a aula), tempo de estudo
  por semana ou 4 semanas com a linha do limite da família, tarefas para fazer/feitas. O tema é só um marcador de cor
  pequeno (Okabe-Ito em forma, nunca em texto); animações só com a preferência "Animações suaves" (desligada com foco).
- **Minhas tarefas:** com foco, só a atual aparece; as outras ficam recolhidas.
- **Treinar:** revisar o que errei, treino rápido (3 questões) e revisão de 7 dias; uma questão por tela, confirmar antes
  de ver a resposta, certo/errado com texto e ícone; treino não vale nota.
- **Lateral:** apoios escolhidos pelo professor, preferências (letras espaçadas, ouvir, modo limpo) e "Como foi hoje?" opcional.

### Trilha, carrossel e temas (prompt 32)
- **Trilha estilo jogo** no bloco grande: uma unidade por matéria; fase feita = estrelas (acertos) + cor da nota; fase
  atual com o Next e "Começar!"; uma revisão a cada 3 fases (retenção); fases futuras bloqueadas.
  Foco: só a unidade atual aberta, sem rótulos ao redor, no máximo 2 fases bloqueadas visíveis ("+N depois").
- **Notas em carrossel** com escala vermelho → verde (Vamos revisar < 5 · Quase lá < 7 · Bom < 8,5 · Muito bom < 10 · Dominado! = 10),
  sempre com símbolo e texto junto da cor (daltonismo). Faixas são valor de produto, a calibrar.
- **Tema por apoio** (prioridade limpo > foco > textual > concreto > base): Aurora (sem apoios), Oceano (foco),
  Pergaminho (leitura, letra maior), Parque (concreto, ícones por matéria), Limpo. Contraste de texto >= 4,5:1 conferido.
- Animação (pulsar da fase atual, quique do balão) só com a preferência "Animações": desligada por padrão com foco e modo limpo.
- Barra "Protótipo · ver como" (`?ver=base|foco|textual|concreto|limpo`) para comparar os temas com os mesmos dados.

## O que ainda falta (para o front)
- Preferências do aluno na tela (`fonte_dislexia`, `leitura_voz`, `modo_limpo`) já existem no `Perfil`, mas os templates do time ainda não as aplicam.
- Registro de uso (`EventoUso`: tempo por bloco, pediu dica, ouviu em voz alta) é da Fatia 3.
- Visual: as telas reais usam `templates/aulas/inicio_aluno.html` e `ver_aula.html` (Tailwind). O desenho alvo está em
  `/prototipo/aluno/` e `/prototipo/aluno/aula/`: é só portar o visual mantendo as mesmas variáveis de contexto.
