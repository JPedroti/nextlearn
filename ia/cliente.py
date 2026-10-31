"""Chamada à IA. Único arquivo que conhece o provedor.

Suporta dois provedores, escolhidos por variáveis de ambiente:

1. Gemini (Google AI Studio), o padrão:
   GEMINI_API_KEY=...    # chave do Google AI Studio
   GEMINI_MODEL=...      # padrão: gemini-flash-latest (o modelo "flash" mais recente)

2. Compatível com a API da OpenAI (DeepSeek, Groq, OpenAI etc.):
   IA_PROVEDOR=openai    # liga este provedor
   IA_API_KEY=...        # chave da API
   IA_BASE_URL=...       # endereço da API (ex.: https://api.deepseek.com/v1); vazio = OpenAI
   IA_MODEL=...          # nome do modelo (ex.: deepseek-chat)

Nos dois casos a IA recebe só o system prompt (apoios) e a aula, e devolve o mesmo JSON (SaidaVersao).
"""

import json
import logging

from django.conf import settings
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Parâmetros da IA — ajustáveis conforme o modelo e o uso
TEMPERATURA = 0.4     # Mais determinístico que 0.7 — adaptações precisam de consistência
MAX_TOKENS = 8192      # Suficiente para aulas longas com várias questões
MAX_CARACTERES = 28000  # ~7K tokens — seguro para DeepSeek (64K), Gemini (128K), Groq (8K)


class SaidaVersao(BaseModel):
    """Formato que a IA é obrigada a devolver (saída estruturada em JSON)."""

    conteudo: str
    enunciados: list[str]


def _usa_openai():
    return settings.IA_PROVEDOR == "openai"


def configurado():
    """True quando o provedor escolhido tem chave. Sem ela, a tela do professor avisa em vez de oferecer a geração."""
    chave = settings.IA_API_KEY if _usa_openai() else settings.GEMINI_API_KEY
    return bool(chave.strip())


def _gerar_via_gemini(system_prompt, mensagem, classe_saida):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    resposta = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=mensagem,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=classe_saida,
        ),
    )
    if isinstance(resposta.parsed, classe_saida):
        return resposta.parsed
    return classe_saida.model_validate_json(resposta.text or "")


def _gerar_via_openai(system_prompt, mensagem, classe_saida):
    from openai import OpenAI

    client = OpenAI(api_key=settings.IA_API_KEY, base_url=settings.IA_BASE_URL or None)
    resposta = client.chat.completions.create(
        model=settings.IA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": mensagem},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": classe_saida.__name__,
                "strict": True,
                "schema": classe_saida.model_json_schema(),
            },
        },
        temperature=TEMPERATURA,
        max_tokens=MAX_TOKENS,
    )

    conteudo_bruto = resposta.choices[0].message.content or ""
    try:
        return classe_saida.model_validate(json.loads(conteudo_bruto))
    except (json.JSONDecodeError, ValueError) as erro:
        logger.warning("Resposta da IA fora do formato JSON esperado: %s. Início: %s", erro, conteudo_bruto[:300])
        raise RuntimeError("A IA devolveu uma resposta em formato inesperado.") from erro


def gerar(system_prompt, mensagem, classe_saida=SaidaVersao):
    """Envia o prompt ao provedor escolhido e devolve uma instância de `classe_saida` (default: SaidaVersao).

    Erros sobem como exceção para quem chamou. Verifica o tamanho do contexto e avisa se estiver muito grande.
    """
    if not configurado():
        raise RuntimeError("A chave do provedor de IA não está configurada.")

    total = len(system_prompt) + len(mensagem)
    if total > MAX_CARACTERES:
        logger.warning(
            "Contexto grande: %s caracteres (limite: %s). Cortando mensagem para caber.",
            total, MAX_CARACTERES,
        )
        # Corta a aula (mensagem) para caber; o system prompt é preservado
        limite_mensagem = MAX_CARACTERES - len(system_prompt) - 500
        if limite_mensagem > 0:
            mensagem = mensagem[:limite_mensagem] + "\n\n[Texto truncado por limite de contexto.]"

    if _usa_openai():
        return _gerar_via_openai(system_prompt, mensagem, classe_saida)
    return _gerar_via_gemini(system_prompt, mensagem, classe_saida)
