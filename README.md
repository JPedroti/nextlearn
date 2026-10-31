# NextLearn

O professor prepara a aula **uma vez** e cada aluno recebe a **mesma aula** no formato em que consegue aprender.
É para a turma inteira, seguindo o Desenho Universal para a Aprendizagem (DUA).

Projeto do 1º Hackathon LEPV × FGV (tema: Educação, patrocínio Teachy) — Desafio 1: Inclusão e acessibilidade.

- **Deploy:** _(link do Render, preencher após o primeiro deploy)_
- **Histórico de prompts usados com IA:** [docs/historico_prompts.md](docs/historico_prompts.md)

## Equipe

João Pedroti, Thiago, Cauã e Gabriel Franco (IME, 4º período).

## Stack

Python + Django 5.2, templates do Django com Tailwind (CDN), SQLite no computador e Postgres (Neon) em produção,
Gemini (`google-genai`) para gerar as versões adaptadas, deploy no Render.

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

### Criar outros usuários

Por enquanto, os usuários (professor, família, aluno) são criados em http://127.0.0.1:8000/admin/,
em **Usuários → Adicionar**, escolhendo o **papel**. Cada papel tem a sua página inicial:

| Papel | Página inicial |
|---|---|
| Professor | `/professor/` |
| Família | `/familia/` |
| Aluno | `/aluno/` |

### Rodar os testes

```powershell
python manage.py test
```

## Variáveis de ambiente

Ficam no `.env` (local, fora do Git) ou no painel do Render (produção). Modelo em [.env.example](.env.example).

| Variável | Para que serve |
|---|---|
| `SECRET_KEY` | Chave secreta do Django. No Render é gerada automaticamente |
| `DEBUG` | `True` só no computador; `False` em produção |
| `ALLOWED_HOSTS` | Endereços aceitos. O endereço do Render entra sozinho |
| `DATABASE_URL` | Connection string do Postgres (Neon). Vazia = SQLite local |
| `GEMINI_API_KEY` | Chave do Google AI Studio |
| `GEMINI_MODEL` | Modelo do Gemini (padrão: `gemini-flash-latest`) |
| `DJANGO_SUPERUSER_*` | Só no Render: cria o primeiro administrador durante o deploy |

## Deploy (Render)

O arquivo [render.yaml](render.yaml) descreve o serviço. A cada push na `main`, o Render roda
[build.sh](build.sh) (instala dependências, `collectstatic`, `migrate` e cria o administrador se ainda não existir)
e inicia o site com `gunicorn`.

## Estrutura

```
config/        configurações do Django (settings, urls)
apps/contas/   usuário com papel (professor, família, aluno), login e logout
apps/turmas/   turmas e alunos
apps/perfis/   perfil de adaptações e questionário da família
apps/aulas/    aulas, questões, versões adaptadas e respostas
apps/painel/   telas do professor
ia/            motor de IA: montagem do prompt e chamada ao Gemini (a partir da Fatia 2)
templates/     páginas HTML
static/        CSS, JS e fontes
tests/         testes automatizados
docs/          histórico de prompts e documentação
```
