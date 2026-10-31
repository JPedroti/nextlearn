"""Chamada ao Gemini. É o único arquivo que conhece o provedor de IA: trocar de modelo é mexer só aqui."""

from django.conf import settings
from google import genai
from google.genai import types
from pydantic import BaseModel


class SaidaVersao(BaseModel):
    """Formato que a IA é obrigada a devolver (saída estruturada em JSON)."""

    conteudo: str
    enunciados: list[str]


def configurado():
    """True quando há chave de API. Sem ela, a tela do professor avisa em vez de oferecer a geração."""
    return bool(settings.GEMINI_API_KEY.strip())


def gerar(system_prompt, mensagem):
    """Envia o prompt e devolve um SaidaVersao. Erros da API sobem como exceção para quem chamou."""
    if not configurado():
        raise RuntimeError("GEMINI_API_KEY não está configurada.")
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
