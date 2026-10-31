# Arquitetura do NextLearn

Um único projeto Django (Python), com páginas renderizadas no servidor. O navegador só roda JavaScript em três
pontos pequenos: a barra de apoios de leitura, a leitura em voz alta e o aviso de "gerando…".

## Visão geral

```mermaid
flowchart LR
    Familia["Família"] -->|responde o questionário| Sug["Sugestões de apoio"]
    Uso["Uso da barra de apoios"] -->|"ligou 3 vezes"| Sug
    Sug -->|"professor aceita"| Perfil["Perfil do aluno<br/>(máscara de 3 bits)"]
    Prof["Professor"] -->|marca os apoios| Perfil
    Prof -->|escreve uma vez| Aula["Aula + questões<br/>(versão original)"]
    Aula --> IA["Motor de IA (ia/)<br/>uma versão por máscara"]
    IA --> Versao["Versão adaptada<br/>(aguarda aprovação)"]
    Prof -->|revisa e aprova| Versao
    Perfil --> Escolha{"Versão do aluno"}
    Versao --> Escolha
    Aula --> Escolha
    Escolha --> Aluno["Aluno lê e responde"]
    Aluno --> Painel["Painel da turma"]
```

## Partes do código

| Pasta | Responsabilidade |
|---|---|
| `config/` | Configurações (tudo vem de variáveis de ambiente) e rotas principais |
| `apps/contas/` | `Usuario` com `papel` (professor, família, aluno), login, logout e o decorador `papel_requerido` |
| `apps/turmas/` | Turmas, cadastro de alunos e de famílias pelo professor |
| `apps/perfis/` | Perfil (apoios), questionário da família, sugestões de ajuste e preferências de tela |
| `apps/aulas/` | Aulas, questões, versões adaptadas, respostas, registros de uso e a tela do aluno |
| `apps/painel/` | Telas do professor com números da turma (só views e cálculos, sem tabelas próprias) |
| `ia/` | Motor de IA: blocos do prompt (`blocos/*.md`), montagem do prompt, chamada ao provedor e geração com cache |
| `templates/` | Páginas HTML (Django templates + Tailwind) |
| `static/` | CSS das preferências e os scripts da barra de apoios e da leitura em voz alta |
| `tests/` | Testes automatizados, um arquivo por fatia |

## Modelo de dados

```mermaid
erDiagram
    Usuario ||--o{ Turma : "professor de"
    Usuario ||--o| Aluno : "login do aluno"
    Usuario ||--o{ Aluno : "responsável (família)"
    Turma ||--o{ Aluno : "tem"
    Turma ||--o{ Aula : "tem"
    Aluno ||--|| Perfil : "tem"
    Aluno ||--o{ RespostaQuestionario : "família respondeu"
    Aluno ||--o{ SugestaoPerfil : "recebe"
    Aluno ||--o{ Resposta : "dá"
    Aluno ||--o{ EventoUso : "gera"
    Aula ||--o{ Questao : "tem"
    Aula ||--o{ VersaoAdaptada : "uma por máscara"
    Questao ||--o{ Resposta : "recebe"

    Usuario {
        string papel
    }
    Perfil {
        bool foco "bit F, vale 4"
        bool textual "bit S, vale 2"
        bool concreto "bit C, vale 1"
        bool fonte_dislexia
        bool leitura_voz
        bool modo_limpo
        bool revisado_pelo_professor
    }
    Questao {
        int ordem
        text enunciado
        json alternativas
        int indice_correto "gabarito do professor"
    }
    VersaoAdaptada {
        int mascara "1 a 7, única por aula"
        text conteudo
        json enunciados
        bool aprovada
    }
    Resposta {
        int indice_escolhido
        bool correta
        int tempo_ms
        int versao_mascara "0 = original"
    }
    SugestaoPerfil {
        string campo
        bool valor_sugerido
        string origem "questionario ou uso"
        string status "pendente, aceita, recusada"
    }
    EventoUso {
        string tipo "qual apoio de leitura foi ligado"
    }
```

**Máscara:** `foco×4 + textual×2 + concreto×1`, de 0 a 7. A máscara 0 é a aula original e não chama a IA, então
cada aula tem no máximo 7 versões geradas.

## Geração de uma versão adaptada

```mermaid
sequenceDiagram
    actor P as Professor
    participant V as aulas.views.gerar
    participant G as ia.gerar_versao
    participant B as ia.prompt_builder
    participant C as ia.cliente
    participant DB as Banco
    P->>V: Gerar com IA (máscara 5)
    V->>G: gerar_versao(aula, 5)
    G->>DB: já existe versão (aula, 5)?
    alt já existe (cache)
        DB-->>G: versão salva
    else não existe
        G->>B: system prompt: base + foco + concreto + conflitos
        G->>B: mensagem: texto da aula e enunciados, entre tags (sem dados do aluno)
        G->>C: gerar(system prompt, mensagem)
        C-->>G: JSON {conteudo, enunciados}
        G->>G: confere 1 enunciado por questão
        G->>DB: salva com aprovada = falso
    end
    V-->>P: tela de revisão
    P->>DB: corrige (se quiser) e aprova
```

O aluno só vê a versão da sua máscara depois que ela é aprovada; até lá, vê a original. As alternativas e o gabarito
vêm sempre de `Questao`, e cada `Resposta` guarda qual versão o aluno viu, para o painel comparar acertos.

## Quem acessa o quê

- Cada tela exige login e um papel (`papel_requerido`). Tentar abrir a tela de outro papel dá erro 403.
- O professor só encontra as próprias turmas: as consultas filtram por `professor=request.user`.
- A família só responde pelos alunos de quem é responsável; o aluno só vê aulas publicadas da própria turma.
- O que vai para a IA: só os apoios ligados (bits) e o texto da aula com os enunciados. Nunca nome, login, respostas
  ou questionário do aluno.

## Testes

`python manage.py test` roda 80 testes, em `tests/`: login e papéis (Fatia 0), turma, aula e correção (1), máscara,
montagem do prompt, cache e gabarito intocado pela IA (2), preferências de tela e registro de uso (3),
questionário e sugestões (4), painel e sugestões pelo uso (5). Nos testes, a chamada à IA é simulada.
