-- Esboço de pesquisa, anterior à versão final do produto: o app NÃO usa este arquivo.
-- O banco real vem dos models do Django, em apps/. Índice dos documentos: docs/README.md.
-- =====================================================================
-- Schema da plataforma (MVP hackathon) — SQLite
-- Compatível com PostgreSQL trocando: INTEGER PRIMARY KEY -> SERIAL/UUID,
-- TEXT(JSON) -> JSONB, datetime('now') -> now().
-- Princípios: perfil por BARREIRA (não por CID), laudo opcional e separado,
-- IA só sugere (tabela sugestao), dados mínimos de menores (LGPD/ECA Digital).
-- =====================================================================
PRAGMA foreign_keys = ON;

-- ---------- Organização ----------
CREATE TABLE escola (
  id INTEGER PRIMARY KEY,
  nome TEXT NOT NULL,
  cidade TEXT, uf TEXT,
  criado_em TEXT DEFAULT (datetime('now'))
);

CREATE TABLE usuario (
  id INTEGER PRIMARY KEY,
  escola_id INTEGER NOT NULL REFERENCES escola(id),
  papel TEXT NOT NULL CHECK (papel IN ('aluno','professor','aee','coordenacao','familia')),
  nome TEXT NOT NULL,
  email TEXT,                       -- não obrigatório para aluno
  criado_em TEXT DEFAULT (datetime('now'))
);

CREATE TABLE turma (
  id INTEGER PRIMARY KEY,
  escola_id INTEGER NOT NULL REFERENCES escola(id),
  nome TEXT NOT NULL,               -- ex.: '6º A'
  ano_escolar INTEGER NOT NULL CHECK (ano_escolar BETWEEN 1 AND 12), -- 1–9 fundamental, 10–12 médio
  ano_letivo INTEGER NOT NULL
);

CREATE TABLE turma_professor (
  turma_id INTEGER REFERENCES turma(id),
  professor_id INTEGER REFERENCES usuario(id),
  PRIMARY KEY (turma_id, professor_id)
);

-- Aluno: sem data de nascimento completa (minimização); a etapa define regras do CNE
CREATE TABLE aluno (
  usuario_id INTEGER PRIMARY KEY REFERENCES usuario(id),
  turma_id INTEGER NOT NULL REFERENCES turma(id),
  etapa TEXT NOT NULL CHECK (etapa IN ('fund1','fund2','medio')),  -- fund1 = sem IA autônoma (CNE)
  apelido_exibicao TEXT
);

CREATE TABLE responsavel_aluno (
  responsavel_id INTEGER REFERENCES usuario(id),
  aluno_id INTEGER REFERENCES aluno(usuario_id),
  parentesco TEXT,
  PRIMARY KEY (responsavel_id, aluno_id)
);

-- ---------- Consentimento e dados sensíveis (LGPD arts. 11 e 14) ----------
CREATE TABLE consentimento (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  responsavel_id INTEGER NOT NULL REFERENCES usuario(id),
  tipo TEXT NOT NULL CHECK (tipo IN ('uso_plataforma','dados_saude','ia_externa','mensagens_familia')),
  concedido INTEGER NOT NULL CHECK (concedido IN (0,1)),
  versao_termo TEXT NOT NULL,
  data TEXT DEFAULT (datetime('now'))
);

-- Laudo: OPCIONAL, guardado à parte, arquivo criptografado fora do banco; acesso restrito (AEE/coordenação)
CREATE TABLE laudo (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  arquivo_ref TEXT NOT NULL,        -- caminho/URL do arquivo criptografado
  enviado_por INTEGER REFERENCES usuario(id),
  data TEXT DEFAULT (datetime('now'))
  -- NUNCA guardar CID aqui em texto aberto; o perfil usa barreiras
);

-- ---------- Perfis por barreira ----------
CREATE TABLE barreira (
  codigo TEXT PRIMARY KEY,          -- P1..P8
  nome TEXT NOT NULL,
  descricao TEXT
);

CREATE TABLE perfil_barreira (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  barreira_codigo TEXT NOT NULL REFERENCES barreira(codigo),
  origem TEXT NOT NULL CHECK (origem IN ('questionario_professor','questionario_familia','laudo','dados_uso')),
  confianca REAL CHECK (confianca BETWEEN 0 AND 1),
  status TEXT NOT NULL DEFAULT 'sugerida' CHECK (status IN ('sugerida','confirmada','descartada')),
  confirmado_por INTEGER REFERENCES usuario(id),
  atualizado_em TEXT DEFAULT (datetime('now'))
);

CREATE TABLE questionario_item (
  codigo TEXT PRIMARY KEY,          -- ex.: 'Q_LEITURA_LENTA'
  texto TEXT NOT NULL,              -- observação pedagógica (NÃO é teste psicológico)
  barreira_codigo TEXT NOT NULL REFERENCES barreira(codigo),
  peso REAL DEFAULT 1.0
);

CREATE TABLE questionario_resposta (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  respondente_id INTEGER NOT NULL REFERENCES usuario(id),
  item_codigo TEXT NOT NULL REFERENCES questionario_item(codigo),
  valor INTEGER NOT NULL CHECK (valor BETWEEN 0 AND 3), -- 0 nunca .. 3 sempre
  data TEXT DEFAULT (datetime('now'))
);

-- ---------- Adaptações ----------
CREATE TABLE adaptacao (
  codigo TEXT PRIMARY KEY,          -- ex.: 'AUDIO_ENUNCIADO'
  nome TEXT NOT NULL,
  barreira_codigo TEXT NOT NULL REFERENCES barreira(codigo),
  descricao TEXT,
  fonte_evidencia TEXT,
  parametros_padrao TEXT            -- JSON
);

CREATE TABLE aluno_adaptacao (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  adaptacao_codigo TEXT NOT NULL REFERENCES adaptacao(codigo),
  ativa INTEGER NOT NULL DEFAULT 1,
  parametros TEXT,                  -- JSON (ex.: {"bloco_min": 6})
  aprovada_por INTEGER REFERENCES usuario(id),
  atualizado_em TEXT DEFAULT (datetime('now'))
);

-- ---------- Conteúdo ----------
CREATE TABLE habilidade (
  codigo TEXT PRIMARY KEY,          -- BNCC, ex.: 'EF06MA07'
  componente TEXT NOT NULL,         -- 'Matemática'
  ano_escolar INTEGER NOT NULL,
  descricao TEXT NOT NULL,
  prerequisito_codigo TEXT REFERENCES habilidade(codigo)
);

CREATE TABLE item (
  id INTEGER PRIMARY KEY,
  habilidade_codigo TEXT NOT NULL REFERENCES habilidade(codigo),
  tipo TEXT NOT NULL CHECK (tipo IN ('multipla','numerica','vf')),  -- só objetivas (CNE)
  enunciado TEXT NOT NULL,
  enunciado_simplificado TEXT,      -- P2
  audio_ref TEXT,                   -- P1
  apoio_visual_ref TEXT,            -- P5
  alternativas TEXT,                -- JSON: [{"id":"a","texto":"2/5","tipo_erro":"soma_num_den"}, ...]
  gabarito TEXT NOT NULL,
  dificuldade REAL DEFAULT 0.0,     -- logit; >0 mais difícil
  dica_1 TEXT, dica_2 TEXT,         -- pistas, nunca a resposta
  exemplo_resolvido TEXT            -- P7 / após 3 erros
);

CREATE TABLE tipo_erro (
  codigo TEXT PRIMARY KEY,          -- 'conceito','procedimento','leitura','fato_aritmetico','motor', ou específico
  descricao TEXT NOT NULL,
  intervencao_sugerida TEXT
);

-- ---------- Uso (telemetria comportamental — nada de webcam/biometria) ----------
CREATE TABLE sessao (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  contexto TEXT NOT NULL CHECK (contexto IN ('casa','escola_mediada')),
  mediador_id INTEGER REFERENCES usuario(id),   -- obrigatório na prática para fund1
  inicio TEXT DEFAULT (datetime('now')),
  fim TEXT,
  concluida INTEGER DEFAULT 0,
  autoavaliacao TEXT CHECK (autoavaliacao IN ('bem','medio','mal'))  -- opcional
);

CREATE TABLE tentativa (
  id INTEGER PRIMARY KEY,
  sessao_id INTEGER NOT NULL REFERENCES sessao(id),
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  item_id INTEGER NOT NULL REFERENCES item(id),
  ordem_na_sessao INTEGER NOT NULL,
  resposta TEXT,
  correta INTEGER NOT NULL CHECK (correta IN (0,1)),
  latencia_ms INTEGER,              -- conta a partir do fim do áudio (P1) e sem tempo motor (P6)
  dicas_usadas INTEGER DEFAULT 0,
  tipo_erro_codigo TEXT REFERENCES tipo_erro(codigo),
  apoios_usados TEXT,               -- JSON: ["audio","glossario"]
  toques_fora_alvo INTEGER DEFAULT 0,
  variante_ab TEXT,                 -- 'A' / 'B' quando há experimento
  criado_em TEXT DEFAULT (datetime('now'))
);

-- ---------- Estado do motor ----------
CREATE TABLE dominio_habilidade (
  aluno_id INTEGER REFERENCES aluno(usuario_id),
  habilidade_codigo TEXT REFERENCES habilidade(codigo),
  p_dominio REAL NOT NULL DEFAULT 0.2,   -- BKT P(L)
  n_tentativas INTEGER DEFAULT 0,
  dominada_em TEXT,
  atualizado_em TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (aluno_id, habilidade_codigo)
);

CREATE TABLE memoria_habilidade (
  aluno_id INTEGER REFERENCES aluno(usuario_id),
  habilidade_codigo TEXT REFERENCES habilidade(codigo),
  meia_vida_dias REAL NOT NULL DEFAULT 1.0,
  ultima_pratica TEXT,
  proxima_revisao TEXT,
  PRIMARY KEY (aluno_id, habilidade_codigo)
);

CREATE TABLE experimento_ab (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  adaptacao_codigo TEXT NOT NULL REFERENCES adaptacao(codigo),
  inicio TEXT DEFAULT (datetime('now')),
  fim TEXT,
  resultado TEXT,                   -- JSON: ganho de domínio com e sem
  decisao TEXT CHECK (decisao IN ('manter','desligar','inconclusivo'))
);

-- ---------- IA sugere, humano decide (CNE) ----------
CREATE TABLE sugestao (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  tipo TEXT NOT NULL CHECK (tipo IN ('ativar_adaptacao','desativar_adaptacao','confirmar_barreira','mudar_trilha','revisar_prerequisito','pausa','iniciar_ab')),
  regra_codigo TEXT NOT NULL,       -- qual regra disparou
  explicacao TEXT NOT NULL,         -- "por que estou sugerindo isso" (transparência)
  payload TEXT,                     -- JSON com o que muda
  status TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente','aprovada','rejeitada')),
  decidido_por INTEGER REFERENCES usuario(id),
  criado_em TEXT DEFAULT (datetime('now')),
  decidido_em TEXT
);

CREATE TABLE alerta (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  tipo TEXT NOT NULL CHECK (tipo IN ('em_risco','dormente','frustracao','gaming','esquecimento')),
  severidade INTEGER CHECK (severidade BETWEEN 1 AND 3),
  detalhe TEXT,
  criado_em TEXT DEFAULT (datetime('now')),
  resolvido INTEGER DEFAULT 0
);

-- ---------- Família ----------
CREATE TABLE mensagem_familia (
  id INTEGER PRIMARY KEY,
  aluno_id INTEGER NOT NULL REFERENCES aluno(usuario_id),
  responsavel_id INTEGER NOT NULL REFERENCES usuario(id),
  semana_inicio TEXT NOT NULL,
  resumo TEXT NOT NULL,
  atividade_casa TEXT,
  lida_em TEXT,
  atividade_feita INTEGER DEFAULT 0
);

CREATE TABLE limite_uso (
  aluno_id INTEGER PRIMARY KEY REFERENCES aluno(usuario_id),
  minutos_dia INTEGER NOT NULL DEFAULT 30,
  notificacoes_dia_max INTEGER NOT NULL DEFAULT 1,
  definido_por INTEGER REFERENCES usuario(id)
);

-- ---------- Transparência e auditoria ----------
CREATE TABLE log_ia (
  id INTEGER PRIMARY KEY,
  finalidade TEXT NOT NULL,         -- 'simplificar_enunciado','mensagem_familia'
  modelo TEXT,
  entrada_hash TEXT,                -- hash do prompt pseudonimizado (sem nome/laudo)
  saida TEXT,
  criado_em TEXT DEFAULT (datetime('now'))
);

CREATE TABLE auditoria (
  id INTEGER PRIMARY KEY,
  usuario_id INTEGER REFERENCES usuario(id),
  acao TEXT NOT NULL,               -- 'ver_laudo','aprovar_sugestao',...
  entidade TEXT, entidade_id INTEGER,
  criado_em TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_tentativa_aluno ON tentativa(aluno_id, criado_em);
CREATE INDEX idx_sugestao_status ON sugestao(status, aluno_id);
