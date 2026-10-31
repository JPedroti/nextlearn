# Mapeamento: pesquisa → app NextLearn (31/10/2026, 01h40)

Como a pesquisa feita pelo Thiago (perfis por barreira, métricas, leis) entra no app Django que já existe,
sem mudar as decisões do `CLAUDE.md`. Foco na **Fatia 3 (interface)**, que é do Thiago.

## 1. O que muda em relação aos documentos de pesquisa

Os documentos em `docs/` (PERFIS_E_METRICAS, METRICAS_ENSINO, PLANO_IMPLEMENTACAO, `db/schema.sql`) foram escritos
antes de o Thiago ver o código do time. Ao usar, valem estas correções, que seguem o `CLAUDE.md`:

| Nos documentos de pesquisa | No app (vale isto) | Por quê |
|---|---|---|
| "Plataforma para neurodivergentes" | "A mesma aula para a turma inteira, no formato de cada aluno" (DUA) | Seção 3 do `CLAUDE.md` |
| 8 perfis (P1–P8) com banco próprio | 3 bits (`foco`, `textual`, `concreto`) + 3 preferências de interface no `Perfil` | Já implementado e testado; os 8 perfis viram a **justificativa** dos bits (seção 2) |
| `db/schema.sql` com 28 tabelas | Models do Django em `apps/` | O schema fica só como referência de próximos passos |
| Streamlit | Templates Django + Tailwind (CDN) | Decisão da equipe |
| Alunos fictícios com histórico simulado na demo | **Proibido**: nada de seed com alunos ou respostas falsas | Cartão vermelho ("demo de fachada") |
| Domínio (BKT), retenção, "foco", gamificação | **Fora da v1.0** → slide de próximos passos | Seção 3 do `CLAUDE.md` |
| "AEE", "PAEE" | "Adaptações" ou "apoios" | Terminologia do `CLAUDE.md` |

## 2. Os 8 perfis da pesquisa → bits e preferências do `Perfil`

Os bits já cobrem 7 dos 8 perfis. Serve para o pitch e para o vídeo explicarem **por que** existem esses 3 bits.

| Perfil da pesquisa (barreira) | Bits | Preferências de interface | Evidência que sustenta |
|---|---|---|---|
| P1 Leitura e fluência (ex.: dislexia) | `textual` | `leitura_voz`, `fonte_dislexia` | Texto em áudio: d = 0,35 (Wood et al., 2018); espaçamento extra entre letras: +20% de velocidade (Zorzi et al., 2012) |
| P2 Linguagem e compreensão (ex.: TDL, TEA) | `textual` (+ `concreto`) | — | Estratégias de compreensão: g = 0,59 (Filderman et al., 2021) |
| P3 Atenção e memória de trabalho (ex.: TDAH) | `foco` | `modo_limpo` | Déficit de memória de trabalho d = 1,63–2,03 (Kofler et al., 2020) |
| P4 Previsibilidade e sensorial (ex.: TEA) | `foco` + `textual` (linguagem literal) | `modo_limpo` | Apoios visuais e previsibilidade entre as 28 práticas com evidência (NCAEP, 2020) |
| P5 Matemática (ex.: discalculia) | `concreto` | — | Intervenções digitais em matemática: 0,55 (Benavides-Varela et al., 2020) |
| P6 Motor (ex.: TDC) | — | **Para todos:** botões grandes (≥ 44 px) | WCAG 2.2, critério 2.5.5. No DUA, entra no padrão da interface, sem campo novo |
| P7 Ritmo e abstração (ex.: deficiência intelectual) | `concreto` + `foco` (+ `textual`) | — | Análise de tarefa e exemplos concretos (NCAEP, 2020) |
| P8 Altas habilidades | Não coberto na v1.0 | — | Próximo passo: versão de aprofundamento |

**Ponto de atenção (fonte OpenDyslexic):** os estudos não mostram ganho de leitura com fontes "para dislexia"
(ex.: Wery & Diliberto, 2017). O que tem evidência é o **espaçamento maior entre letras** (Zorzi et al., 2012).
Sugestão para a Fatia 3, sem mudar o model: a preferência `fonte_dislexia` aplica OpenDyslexic **e**
`letter-spacing` maior. No texto da tela, chamar de "Letras mais espaçadas". Decisão da equipe: perguntar ao João antes de mudar o rótulo.

## 3. Métricas: o que já dá para medir com o que existe

| Métrica | Fonte no app | Onde aparece |
|---|---|---|
| Acertos por aluno e por aula | `Resposta.correta` | Painel (Fatia 5) |
| Acertos por combinação de apoios | `Resposta` + `Perfil.mascara` do aluno | Painel: mostra se as versões adaptadas estão funcionando |
| Tempo para responder a aula | `Resposta.tempo_ms` (hoje é o tempo da aula inteira) | Painel |
| Preferências usadas | **`EventoUso` (falta criar, Fatia 3)** | Painel e sugestões de ajuste |
| Sugestões a partir do uso | `SugestaoPerfil` com `origem = "uso"` (já existe no model) | "Ajustar apoios" do professor |

**Limites do modelo atual (para próximos passos, não para hoje):**
- `Resposta` tem restrição única por aluno e questão, então não há tentativas repetidas: domínio (BKT) e retenção não são possíveis.
- `tempo_ms` é da aula inteira, não por questão: não dá para medir variação do tempo de resposta.

### Regras de sugestão a partir do uso (para a Fatia 5)

Todas criam `SugestaoPerfil(origem="uso")`, que o professor aceita ou recusa. Nada muda sozinho.

| Regra | Se… | Sugestão | `motivo` (texto para o professor) |
|---|---|---|---|
| U1 | O aluno ligou `leitura_voz` em 3 aulas diferentes e o perfil está desligado | Ligar "Leitura em voz alta" | "Ligou a leitura em voz alta em 3 aulas." |
| U2 | Mesmo padrão para `fonte_dislexia` | Ligar "Fonte para dislexia" | "Ligou as letras espaçadas em 3 aulas." |
| U3 | Mesmo padrão para `modo_limpo` | Ligar "Modo limpo" | "Ligou o modo limpo em 3 aulas." |
| U4 | O aluno desligou uma preferência do perfil em 3 aulas | Desligar a preferência | "Desligou X em 3 aulas." |

O número 3 é um valor de produto (não vem de estudo); dá para explicar à banca como "um limite simples, ajustável".

## 4. Fatia 3 (interface): o que construir

### 4.1 Model `EventoUso` (em `apps/aulas/models.py`, como previsto no `CLAUDE.md`)

```python
class EventoUso(models.Model):
    class Tipo(models.TextChoices):
        LIGOU = "ligou", "Ligou preferência"
        DESLIGOU = "desligou", "Desligou preferência"
        OUVIU = "ouviu", "Ouviu texto em voz alta"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="eventos")
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, null=True, blank=True, related_name="eventos")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    preferencia = models.CharField(max_length=20, blank=True)  # fonte_dislexia | leitura_voz | modo_limpo
    criado_em = models.DateTimeField(auto_now_add=True)
```

### 4.2 Preferências na tela do aluno

- **Onde:** uma barra "Como prefiro ler" no topo de `templates/aulas/ver_aula.html`, com 3 interruptores
  (`<button aria-pressed>` reais, alvos de 44 px).
- **Estado inicial:** vem do `Perfil` (o que o professor ligou). O aluno pode mudar só para ele, como diz o model.
- **Ao clicar:** JavaScript troca a classe no `<body>` na hora e faz um `fetch` POST (com CSRF) para uma view nova,
  `aulas:evento`, que grava o `EventoUso`. Sem recarregar a página.
- **Classes no `<body>`** (em `base.html`, a partir do perfil): `pref-fonte-dislexia`, `pref-modo-limpo`, `pref-leitura-voz`.

### 4.3 CSS (`static/css/acessibilidade.css`)

| Classe | Efeito |
|---|---|
| `.pref-fonte-dislexia` | Fonte OpenDyslexic (em `static/fonts/`), `letter-spacing: 0.12em`, `word-spacing: 0.16em`, `line-height: 1.8` |
| `.pref-modo-limpo` | Letra maior (`font-size: 1.25rem`), fundo branco, sem sombras e sem cores de destaque, largura máxima de leitura (~65 caracteres) |
| Padrão para todos | Botões e opções com no mínimo 44 px de altura; foco visível (`outline`); correto ou errado indicado por texto, não só por cor (já é assim) |

### 4.4 Leitura em voz alta (`static/js/leitura_voz.js`)

- Um botão "Ouvir" ao lado do texto da aula e de cada enunciado (aparece quando `pref-leitura-voz` está ativa).
- Usa `speechSynthesis` do navegador, com voz `pt-BR`. Botão vira "Parar" enquanto lê.
- Cada clique em "Ouvir" registra `EventoUso(tipo="ouviu")`.

### 4.5 Testes mínimos (em `tests/`)

- POST em `aulas:evento` cria o `EventoUso` só para o aluno logado.
- Aluno não consegue registrar evento em aula de outra turma.
- A página da aula renderiza com as classes do perfil no `<body>`.

## 5. Coordenação

O cronograma diz que o João pediu à IA dele para fazer a Fatia 3 caso o Thiago não começasse. **Antes de codar,
o Thiago avisa o João** que está assumindo a Fatia 3, para os dois não editarem `ver_aula.html` e `base.html` ao mesmo tempo.
