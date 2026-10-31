"""Dúvidas com o Next (mascote): a criança tira dúvidas sobre a PLATAFORMA.

DECISÃO (auditoria de 31/10, alinhada a docs/RISCOS_LEGAIS.md e ao plano de negócio): o aluno NÃO conversa com
IA generativa. O texto digitado pela criança nunca sai do servidor: as respostas vêm só da FAQ validada e dos
botões de dúvidas rápidas. Motivos: Parecer CNE/CP 15/2026 (sem IA conversacional livre para crianças),
LGPD arts. 11 e 14 (a criança pode digitar nome, escola ou condição de saúde) e termos dos provedores para menores.
O código de IA abaixo fica desligado (USAR_IA = False) e só pode voltar com consentimento e revisão jurídica.

Desenho para escalar (MVP → muitos alunos):
1. Respostas prontas primeiro (FAQ por palavras-chave): as perguntas mais comuns não gastam IA nenhuma.
2. Só o que a FAQ não cobre vai para a IA (endpoint compatível com OpenAI), com contexto curto:
   manual da plataforma + fase atual + últimas 6 mensagens. Nada de nome, turma ou dados do aluno.
3. Limite por aluno por dia (ECA Digital: uso moderado; e controle de custo) e tempo máximo de resposta.
4. Antes de enviar, apaga telefone, e-mail e números longos que a criança digitar (LGPD: minimização).
5. Fora do tema ou pedido de ajuda pessoal → orienta a falar com o professor ou a família.
"""

import os
import re
import unicodedata

from django.core.cache import cache

from .frases import _estilo

USAR_IA = False          # ver DECISÃO no topo
LIMITE_DIA = 30          # mensagens por aluno por dia (valor de produto, a calibrar)
HISTORICO = 6            # mensagens anteriores mandadas como contexto

MANUAL = """Você é o Next, um camaleão que ajuda alunos numa plataforma escolar chamada Chamaleon.
Fatos sobre a plataforma (use só estes; se não souber, diga que não sabe e sugira perguntar ao professor):
- A trilha tem mundos (deserto, floresta, fundo do mar...). Cada mundo tem até 10 fases. Cada fase é uma aula.
- Para começar uma fase, toque no círculo laranja com a estrela ou no botão "Começar fase".
- Cada fase tem perguntas. Cada acerto vale uma estrela. A cor da fase mostra como foi: verde muito bom, amarelo bom, laranja quase lá, vermelho vamos revisar.
- A fase de revisão (seta circular) é um treino para não esquecer. Treino não vale nota.
- "Treinar" tem: revisar o que errei, treino rápido (3 questões) e revisão da semana.
- O calendário (botão Calendário ou o número grande do dia) mostra aulas feitas, prazos e dias de estudo.
- A ofensiva semanal conta semanas com a meta de aulas. Semana parada não zera, só pausa.
- "Meu progresso" mostra a evolução do aluno, comparando só com ele mesmo.
- "Do meu jeito" deixa ligar letras espaçadas, botões de ouvir, modo limpo e animações.
- Os apoios (jeito da aula) são escolhidos pelo professor; a aula é a mesma da turma.
Regras: fale só sobre a plataforma e sobre como estudar nela. Não resolva a lição pelo aluno; dê uma dica para ele pensar.
Não peça nem guarde dados pessoais. Se o aluno falar de tristeza, medo, briga, perigo ou algo pessoal sério,
responda com carinho e diga para conversar com o professor ou alguém da família. Nunca diga que é uma pessoa."""

FAQ = [
    (("estrela",), "Cada acerto numa fase vale uma estrela. Três perguntas, até três estrelas!"),
    (("cor", "vermelh", "verde", "amarel", "laranja"), "A cor mostra como foi a fase: verde é muito bom, amarelo é bom, laranja é quase lá e vermelho quer dizer vamos revisar. Sempre tem o texto junto."),
    (("revis",), "A revisão é um treino rápido para não esquecer o que você já aprendeu. Treino não vale nota."),
    (("calend",), "Toque no número grande do dia ou no botão Calendário. Lá aparecem as aulas feitas e os prazos."),
    (("ofensiva", "semana seguida", "semanas seguidas"), "A ofensiva conta as semanas em que você fez as aulas combinadas. Se uma semana ficar parada, ela só pausa, não zera."),
    (("mundo", "deserto", "floresta", "fase"), "Cada mundo tem até 10 fases. Quando você termina, abre um mundo novo!"),
    (("comec", "começ", "iniciar", "abrir aula"), "Toque no círculo com a estrela, onde eu estou, ou no botão Começar fase."),
    (("progresso", "evolu"), "Em Meu progresso você vê como está melhorando, comparando só com você mesmo."),
    (("letra", "ouvir", "modo limpo", "animac", "do meu jeito"), "Em Do meu jeito você liga letras espaçadas, botões de ouvir, modo limpo ou animações. Muda só para você."),
    (("treino", "treinar"), "Em Treinar tem: revisar o que errei, treino rápido de 3 questões e revisão da semana."),
    (("quem e voce", "quem é você", "seu nome", "voce e"), "Eu sou o Next, um camaleão. Eu mudo de cor e de jeito para ajudar cada um a aprender."),
]


def _sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def limpar_dados_pessoais(texto):
    texto = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[e-mail]", texto)
    texto = re.sub(r"\+?\d[\d\s().-]{7,}\d", "[número]", texto)
    return texto[:400]


def resposta_faq(pergunta):
    p = _sem_acento(pergunta)
    for chaves, resposta in FAQ:
        if any(_sem_acento(c) in p for c in chaves):
            return resposta
    return None


def responder(aluno_id, pergunta, historico, contexto, apoios, chamar_ia):
    """Devolve (resposta, origem). `chamar_ia(mensagens, max_tokens)` -> texto ou None."""
    from datetime import date

    chave = f"chat-limite-{aluno_id}-{date.today().isoformat()}"
    usados = cache.get(chave, 0)
    if usados >= LIMITE_DIA:
        return "Por hoje chega de conversa, combinado? Amanhã eu volto. Se precisar, fale com seu professor.", "limite"
    cache.set(chave, usados + 1, 86400)

    pergunta = limpar_dados_pessoais(pergunta.strip())
    if not pergunta:
        return "Pode perguntar! Eu explico como a plataforma funciona.", "vazio"
    pronta = resposta_faq(pergunta)
    if pronta:
        return pronta, "faq"
    if not USAR_IA:
        return ("Essa eu não sei. Eu explico como a plataforma funciona: escolha uma das perguntas abaixo. "
                "Se for sobre a lição ou sobre você, fale com seu professor ou com sua família."), "faq"

    sistema = MANUAL + "\nEstilo da resposta: " + _estilo(apoios).replace("no máximo 14 palavras", "no máximo 40 palavras")
    sistema += f"\nContexto da tela (sem dados pessoais): {contexto}"
    mensagens = [{"role": "system", "content": sistema}]
    mensagens += historico[-HISTORICO:]
    mensagens.append({"role": "user", "content": pergunta})
    texto = chamar_ia(mensagens, 160)
    if texto:
        return texto, "ia"
    return (pronta or "Ainda não sei responder isso. Tente perguntar sobre estrelas, fases, calendário ou treino. "
            "Se for sobre a lição, pergunte ao seu professor."), "reserva"
