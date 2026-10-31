# NextLearn

O professor prepara a aula **uma vez** e cada aluno recebe a **mesma aula** no formato em que consegue aprender.
É para a turma inteira, seguindo o Desenho Universal para a Aprendizagem (DUA).

Projeto do 1º Hackathon LEPV × FGV (tema: Educação, patrocínio Teachy) — Desafio 1: Inclusão e acessibilidade.

- **Deploy:** _(link do Render, preencher após o primeiro deploy)_
- **Cronograma e status das entregas:** [docs/cronograma.md](docs/cronograma.md)
- **Histórico de prompts usados com IA:** [docs/historico_prompts/](docs/historico_prompts/README.md) (um arquivo por integrante)

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

### Como usar (o que já funciona)

1. **Contas de professor** são criadas em http://127.0.0.1:8000/admin/, em **Usuários → Adicionar**,
   escolhendo o **papel**. As contas de aluno e de família o próprio professor cria nas telas da turma.
2. O **professor** entra e, em **Minhas turmas**, cria uma turma. Dentro dela:
   - **Cadastrar aluno**: cria o usuário e a senha de primeiro acesso do aluno;
   - **Nova aula**: escreve o texto da aula e as questões de múltipla escolha (2 a 4 alternativas, com a correta marcada).
     A aula nasce como rascunho; o botão **Publicar para a turma** libera para os alunos.
3. Na lista de alunos da turma, **Cadastrar família** cria o login do responsável. A família entra e responde
   6 perguntas sobre o dia a dia do aluno (sem laudo e sem diagnóstico). As respostas viram **sugestões de apoio**,
   que o professor aceita ou recusa em **Ajustar apoios**: a família não muda o perfil sozinha.
4. Em **Ajustar apoios**, o professor também marca direto o que ajuda cada aluno:
   **Atenção e foco**, **Acessibilidade textual** e/ou **Interativo e concreto**. Cada combinação vira uma máscara
   de 3 bits (F×4 + S×2 + C×1, de 0 a 7); 0 é a aula original.
5. Na página da aula, em **Versões adaptadas**, aparece uma linha para cada combinação presente na turma.
   **Gerar com IA** cria a versão (o texto e os enunciados reescritos pelo Gemini). O professor revisa, pode corrigir
   e clica em **Aprovar versão**. Cada versão é gerada uma vez e fica guardada (cache); **Gerar de novo** refaz.
   Se o professor editar a aula, as versões são apagadas e precisam ser geradas de novo.
6. O **aluno** entra, vê as aulas publicadas da turma na versão aprovada da sua combinação (ou a original, enquanto
   não houver versão aprovada), responde e vê na hora quantas acertou.
   A correção usa sempre o gabarito do professor: a IA nunca mexe em alternativas nem na resposta certa.

Para testar a geração no seu computador, coloque a sua chave do Google AI Studio em `GEMINI_API_KEY` no `.env`.
A IA recebe só os apoios ligados e o conteúdo da aula, nunca dados do aluno.

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
ia/            motor de IA: blocos do prompt (ia/blocos/), montagem do prompt e chamada ao Gemini
templates/     páginas HTML
static/        CSS, JS e fontes
tests/         testes automatizados
docs/          histórico de prompts e documentação
```
