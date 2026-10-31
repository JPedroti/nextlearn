# NextLearn

O professor prepara a aula **uma vez** e cada aluno recebe a **mesma aula** no formato em que consegue aprender.
É para a turma inteira, seguindo o Desenho Universal para a Aprendizagem (DUA).

Projeto do 1º Hackathon LEPV × FGV (tema: Educação, patrocínio Teachy) — Desafio 1: Inclusão e acessibilidade.

- **Como rodar:** o MVP roda no seu computador em poucos minutos: [Windows](#como-rodar-no-windows) · [macOS ou Linux](#como-rodar-no-macos-ou-no-linux) · [testar em 5 minutos](#testar-em-5-minutos)
- **O problema, com os dados do Inep:** [docs/contexto.md](docs/contexto.md)
- **Arquitetura e modelo de dados:** [docs/arquitetura.md](docs/arquitetura.md)
- **Decisões técnicas e de produto (e por quê):** [docs/decisoes.md](docs/decisoes.md)
- **Cronograma e status das entregas:** [docs/cronograma.md](docs/cronograma.md)
- **Histórico de prompts usados com IA:** [docs/historico_prompts/](docs/historico_prompts/README.md) (um arquivo por integrante)
- **Índice de todos os documentos** (produto, pesquisa e brainstorm): [docs/README.md](docs/README.md)

## Equipe

João, Thiago, Cauã e Gabriel Franco (IME, 4º período).

## Como rodar no Windows

Pré-requisitos: [Python 3.12](https://www.python.org/downloads/) (3.11 também funciona) e Git.
Os comandos abaixo são para o **PowerShell**, dentro da pasta do projeto.

```powershell
# 1. Criar o ambiente virtual (uma pasta venv/ com as bibliotecas só deste projeto)
python -m venv venv

# 2. Ativar o ambiente virtual (faça isso sempre que abrir um terminal novo)
.\venv\Scripts\Activate.ps1

# 3. Instalar as dependências
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Criar o arquivo de configuração local a partir do exemplo
copy .env.example .env

# 5. Criar as tabelas no banco local (SQLite)
python manage.py migrate

# 6. Criar o seu usuário administrador (ele pergunta usuário, e-mail, papel e senha)
python manage.py createsuperuser

# 7. Rodar o servidor
python manage.py runserver
```

Abra http://127.0.0.1:8000 e entre com o usuário criado.

**Problemas comuns**

- *"a execução de scripts foi desabilitada neste sistema"* ao ativar o venv: rode
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` uma vez e tente de novo.
- *Erro de certificado SSL no `pip install`*: atualize o pip (`python -m pip install --upgrade pip --use-feature=truststore`)
  e repita o passo 3.

## Como rodar no macOS ou no Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Testar em 5 minutos

Tudo é feito pela própria pessoa que testa: o repositório não traz alunos, respostas nem aulas prontas.

1. Com o servidor rodando, entre com o administrador. Se no `createsuperuser` você escolheu o papel **professor**, ele
   já serve; senão, crie em `/admin/` um usuário com papel **Professor** e entre com ele.
2. Crie uma turma e cadastre dois alunos.
3. Em **Apoios**, ligue **Atenção e foco** para um dos alunos.
4. Crie uma aula: o texto e as questões de [docs/aula_exemplo.md](docs/aula_exemplo.md) servem, ou use **Criar via PDF**.
   Publique a aula.
5. Com uma chave de IA no `.env`, clique em **Gerar com IA**, revise e aprove a versão.
6. Numa janela anônima, entre como o aluno com foco: o texto aparece em passos. Responda as questões.
7. Volte ao professor e abra **Ver painel** e o **Dashboard** do aluno: os números são os das respostas que você deu.

Para gerar versões com IA no seu computador, coloque a chave em `GEMINI_API_KEY` no `.env` (ou use as variáveis
`IA_*`, abaixo, para outro provedor).

### Rodar os testes

```powershell
python manage.py test
```

São 120 testes, em `tests/`. A chamada à IA é simulada, então não precisam de chave nem de internet.
No GitHub, eles rodam sozinhos a cada envio para a `main` ([.github/workflows/testes.yml](.github/workflows/testes.yml)).

## Como funciona

1. **Contas de professor** são criadas em `/admin/`, em **Usuários → Adicionar**, escolhendo o **papel**.
   As contas de aluno e de família o próprio professor cria nas telas da turma.
2. O **professor** cria uma turma e, dentro dela:
   - **Cadastrar aluno**: cria o usuário e a senha de primeiro acesso do aluno;
   - **Nova aula**: escreve o texto e as questões de múltipla escolha (2 a 4 alternativas, com a correta marcada).
     **Criar via PDF** copia o texto de um PDF para essa mesma tela, para o professor revisar e completar.
     A aula nasce como rascunho; **Publicar para a turma** libera para os alunos.
3. **Cadastrar família** cria o login do responsável. A família responde 9 perguntas sobre o dia a dia do aluno
   (sem laudo e sem diagnóstico) e pode deixar observações. As respostas viram **sugestões de apoio**, que o professor
   aceita ou recusa na tela de **Apoios** do aluno. As observações da família ficam só para o professor ler: não vão
   para a IA.
4. Em **Apoios** (na lista de alunos da turma), o professor marca o que ajuda cada aluno: **Atenção e foco**, **Acessibilidade textual**
   e/ou **Interativo e concreto**. Cada combinação vira uma máscara de 3 bits (F×4 + S×2 + C×1, de 0 a 7);
   0 é a aula original.
5. Na página da aula, em **Versões adaptadas**, aparece uma linha para cada combinação presente na turma.
   **Gerar com IA** cria a versão (o texto e os enunciados reescritos). O professor revisa, pode corrigir e clica em
   **Aprovar versão**. Cada versão é gerada uma vez e fica guardada (cache); **Gerar de novo** refaz.
   Sem chave de IA configurada, o botão fica desligado e a tela avisa; o resto do app funciona normalmente.
6. O **aluno** vê as aulas publicadas na versão aprovada da sua combinação (ou a original, enquanto não houver versão
   aprovada). Com o apoio de foco, o texto aparece **um passo por vez**. As questões vêm uma por vez, com barra de
   progresso, e o **modo concentração** abre a aula em tela cheia. A correção usa sempre o gabarito do professor:
   a IA nunca mexe em alternativas nem na resposta certa.
7. A barra **Apoios de leitura** (sem IA) vale para qualquer aluno: **Fonte para dislexia** (OpenDyslexic, com mais
   espaço entre as letras), **Leitura em voz alta** (voz do próprio navegador) e **Modo limpo**. O professor escolhe o
   que já vem ligado; o aluno liga e desliga quando quiser, e cada vez que ele liga um apoio o sistema registra o uso.
8. O professor acompanha tudo, calculado na hora a partir do uso real:
   - **Painel da turma** (botão **Ver painel**): acertos por aluno e por questão, comparação entre a aula original e as versões adaptadas,
     uso dos apoios de leitura e as **sugestões de ajuste de perfil** (do questionário da família, do uso dos apoios
     e dos acertos). Nada muda sem o professor aceitar;
   - **Página de cada aluno** (link "Dashboard" na turma): acertos por aula, tempo nas aulas e apoios usados.
9. A **família** vê o **relatório** do próprio filho: acertos, versão original × adaptada e apoios de leitura usados.

A IA recebe só os apoios ligados e o conteúdo da aula: nunca nome, login, respostas, questionário ou observações do aluno.

| Papel | Página inicial |
|---|---|
| Professor | `/professor/` |
| Família | `/familia/` |
| Aluno | `/aluno/` |

## Stack

Python + Django 5.2, templates do Django com Tailwind (CDN), SQLite no computador e Postgres (Neon) em produção,
IA pelo Gemini (`google-genai`) ou por uma API compatível com a da OpenAI (`openai`), deploy no Render.

## Variáveis de ambiente

Ficam no `.env` (local, fora do Git) ou no painel do Render (produção). Modelo em [.env.example](.env.example).

| Variável | Para que serve |
|---|---|
| `SECRET_KEY` | Chave secreta do Django. No Render é gerada automaticamente |
| `DEBUG` | `True` só no computador; `False` em produção |
| `ALLOWED_HOSTS` | Endereços aceitos. O endereço do Render entra sozinho |
| `DATABASE_URL` | Connection string do Postgres (Neon). Vazia = SQLite local |
| `IA_PROVEDOR` | `gemini` (padrão) ou `openai` (qualquer API compatível com a da OpenAI) |
| `GEMINI_API_KEY` | Chave do Google AI Studio. Vazia ou ausente = geração com IA desligada, com aviso na tela |
| `GEMINI_MODEL` | Modelo do Gemini (padrão: `gemini-flash-latest`) |
| `IA_API_KEY`, `IA_BASE_URL`, `IA_MODEL` | Chave, endereço e modelo quando `IA_PROVEDOR=openai` (ex.: DeepSeek, Groq, OpenAI) |
| `DJANGO_SUPERUSER_*` | Só no Render: cria o primeiro administrador durante o deploy |

## Publicar na internet (depois do hackathon)

Para o hackathon, o MVP roda no computador (decisão do grupo). O repositório já tem a configuração para publicar
no Render quando a equipe quiser: [render.yaml](render.yaml) descreve o serviço e [build.sh](build.sh) instala as
dependências, prepara os arquivos estáticos, cria as tabelas e o primeiro administrador.

## Créditos

- Fonte [OpenDyslexic](https://opendyslexic.org/) (licença SIL Open Font License), carregada pelo pacote
  [Fontsource](https://fontsource.org/fonts/opendyslexic) no jsDelivr.

## Estrutura

```
config/        configurações do Django (settings, urls)
apps/contas/   usuário com papel (professor, família, aluno), login e logout
apps/turmas/   turmas, alunos e famílias
apps/perfis/   apoios do aluno, questionário e relatório da família, sugestões de ajuste
apps/aulas/    aulas, questões, versões adaptadas, respostas, importação de PDF e a tela do aluno
apps/painel/   telas do professor com os números da turma
ia/            motor de IA: blocos do prompt (ia/blocos/), montagem do prompt e chamada ao provedor
templates/     páginas HTML
static/        CSS e JavaScript (apoios de leitura, leitura em voz alta, navegação da aula)
tests/         testes automatizados
docs/          contexto, arquitetura, decisões, cronograma, histórico de prompts e pesquisa
```

A pesquisa feita durante o hackathon (base científica, perfis, métricas, riscos legais) e os rascunhos de
brainstorm estão listados em [docs/README.md](docs/README.md), com o que foi aproveitado de cada um.
