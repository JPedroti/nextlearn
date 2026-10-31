"""Chamada à IA. Único arquivo que conhece o provedor.

Suporta dois backends, controlados por variáveis de ambiente:

1. Gemini (Google AI Studio):
   GEMINI_API_KEY=...    # chave do Google AI Studio
   GEMINI_MODEL=...      # padrão: gemini-2.0-flash

2. OpenAI-compatible (DeepSeek, Groq, OpenAI, etc.):
   IA_PROVEDOR=openai           # ativa o backend OpenAI-compatible
   IA_API_KEY=...               # chave da API
   IA_BASE_URL=...              # endpoint (ex: https://api.deepseek.com/v1)
   IA_MODEL=...                 # nome do modelo (ex: deepseek-chat)

Se IA_PROVEDOR não for "openai", usa Gemini (compatível com versão anterior).
"""

import json
import logging

from django.conf import settings
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SaidaVersao(BaseModel):
    """Formato que a IA é obrigada a devolver (saída estruturada em JSON)."""

    conteudo: str
    enunciados: list[str]


def _gerar_via_gemini(system_prompt, mensagem):
    from google import genai
    from google.genai import types

    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY não está configurada.")
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    resposta = client.models.generate_content(
        model=getattr(settings, "GEMINI_MODEL", "gemini-2.0-flash"),
        contents=mensagem,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=SaidaVersao,
        ),
    )
    if isinstance(resposta.parsed, SaidaVersao):
        return resposta.parsed
    return SaidaVersao.model_validate_json(resposta.text or "")


def _gerar_via_openai(system_prompt, mensagem):
    from openai import OpenAI

    api_key = getattr(settings, "IA_API_KEY", "")
    base_url = getattr(settings, "IA_BASE_URL", "")
    model = getattr(settings, "IA_MODEL", "deepseek-chat")

    if not api_key:
        raise RuntimeError("IA_API_KEY não está configurada para o provedor OpenAI-compatible.")

    client = OpenAI(api_key=api_key, base_url=base_url or None)

    resposta = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": mensagem},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "SaidaVersao",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "conteudo": {"type": "string"},
                        "enunciados": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["conteudo", "enunciados"],
                    "additionalProperties": False,
                },
            },
        },
        temperature=0.7,
        max_tokens=4096,
    )

    conteudo_raw = resposta.choices[0].message.content
    try:
        dados = json.loads(conteudo_raw)
        return SaidaVersao.model_validate(dados)
    except (json.JSONDecodeError, ValueError) as erro:
        logger.warning("Falha ao parsear JSON da OpenAI: %s. Resposta: %s", erro, conteudo_raw[:300])
        raise RuntimeError("A IA devolveu uma resposta em formato inesperado. Tente de novo.") from erro


def gerar(system_prompt, mensagem):
    """Envia o prompt e devolve um SaidaVersao.

    O provedor é escolhido por settings.IA_PROVEDOR:
    - "openai" → usa OpenAI-compatible (DeepSeek, Groq, etc.)
    - qualquer outro valor ou não definido → usa Gemini
    """
    provedor = getattr(settings, "IA_PROVEDOR", "gemini")
    if provedor == "openai":
        return _gerar_via_openai(system_prompt, mensagem)
    return _gerar_via_gemini(system_prompt, mensagem)