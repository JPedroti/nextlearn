# Login e área do aluno (como funciona hoje)

## Login
- O backend do time já autentica de verdade: `Usuario` (Django) com `papel` = professor, aluno ou família.
- Tela no visual do protótipo: `/prototipo/login/?perfil=aluno|professor|familia` (o perfil só muda o visual: cor e fala do Next).
  Ela usa o `LoginView` do Django; depois do login, `contas:inicio` manda cada um para a sua página pelo papel:
  professor → `/professor/`, aluno → `/aluno/`, família → `/familia/`.
- Não existe cadastro público: o professor cria o aluno e a família na tela da turma (`/professor/turmas/<id>/`).
  O primeiro professor vem do `python manage.py createsuperuser` (ele pergunta o papel).
- Para testar na máquina local: `python manage.py contas_teste` cria `prof.teste`, `aluno.teste`, `familia.teste`,
  uma turma e uma aula publicada. As senhas ficam em `contas_teste_local.txt` (fora do Git). Só para desenvolvimento,
  nunca na demo oficial. O `rodar_prototipo.bat` roda isso sozinho na primeira vez.

## Área do aluno (backend atual)
1. `/aluno/` lista as aulas **publicadas** da turma do aluno e marca as já respondidas.
2. `/aluno/aulas/<id>/` mostra a aula na **versão do perfil dele**: a máscara de 3 bits do `Perfil`
   (foco, textual, concreto) escolhe a `VersaoAdaptada`; só aparece se o professor **aprovou**. Sem versão aprovada, vê a original.
3. As questões são as mesmas para todos (o gabarito é do professor; a IA só reescreve o enunciado).
4. Ao enviar, cada `Resposta` guarda a alternativa, se acertou e o tempo desde que abriu a aula (`tempo_ms`). Não dá para responder duas vezes.
5. Esses dados voltam para o professor (e viram sugestões de ajuste de apoio, que ele aceita ou recusa).

## O que ainda falta (para o front)
- Preferências do aluno na tela (`fonte_dislexia`, `leitura_voz`, `modo_limpo`) já existem no `Perfil`, mas os templates do time ainda não as aplicam.
- Registro de uso (`EventoUso`: tempo por bloco, pediu dica, ouviu em voz alta) é da Fatia 3.
- Visual: as telas reais usam `templates/aulas/inicio_aluno.html` e `ver_aula.html` (Tailwind). O desenho alvo está em
  `/prototipo/aluno/` e `/prototipo/aluno/aula/`: é só portar o visual mantendo as mesmas variáveis de contexto.
