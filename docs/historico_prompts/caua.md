# Histórico de prompts — Cauã

**Hackathon LEPV × FGV (Teachy) — Out/2026.** Índice da equipe: [README.md](README.md)
**Ferramenta de IA principal:** Qwen

Registro cronológico e literal dos prompts que Cauã enviou à IA durante o hackathon, mantido para consulta da banca avaliadora.

---

## Prompt 01 — 31/10/2026, 02:37 (BRT) — autor: Cauã — ferramenta: Qwen

> @nextlearn/CLAUDE.md Avalie o projeto, o que eu, cauã, ainda preciso fazer, e vamos começar após entender as demandas do projeto etc om as configurações de system prompt de engenharia de IA e backend necessárias ,me informe as mudanças e escolhas de tradeoff a serem feitas, vamos trabalhar

**Resumo da resposta da IA:** Blocos pedagógicos reescritos com conteúdo baseado em DUA (5 arquivos). Questionário expandido para 9 perguntas (3 por apoio), com tom humano e cordial + campos de nome do aluno e observações. Modelo `RespostaQuestionario` ganhou `nome_aluno` e `observacoes`; `Perfil` ganhou `contexto_familia` (editável pelo professor, alimenta o system prompt da IA). `prompt_builder.py` e `gerar_versao.py` integrados ao contexto familiar. Templates atualizados. 80 testes passando.
