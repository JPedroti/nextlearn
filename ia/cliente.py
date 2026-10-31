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


def _gerar_via_gemini(system_prompt, mensagem):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    resposta = client.models.generate_content(
        model=settings.GEMINI_MODEL,
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
                "name": "SaidaVersao",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "conteudo": {"type": "string"},
                        "enunciados": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["conteudo", "enunciados"],
                    "additionalProperties": False,
                },
            },
        },
        temperature=0.7,
        max_tokens=4096,
    )

    conteudo_bruto = resposta.choices[0].message.content or ""
    try:
        return SaidaVersao.model_validate(json.loads(conteudo_bruto))
    except (json.JSONDecodeError, ValueError) as erro:
        logger.warning("Resposta da IA fora do formato JSON esperado: %s. Início: %s", erro, conteudo_bruto[:300])
        raise RuntimeError("A IA devolveu uma resposta em formato inesperado.") from erro


def gerar(system_prompt, mensagem):
    """Envia o prompt ao provedor escolhido e devolve um SaidaVersao. Erros sobem como exceção para quem chamou."""
    if not configurado():
        raise RuntimeError("A chave do provedor de IA não está configurada.")
    if _usa_openai():
        return _gerar_via_openai(system_prompt, mensagem)
    return _gerar_via_gemini(system_prompt, mensagem)
