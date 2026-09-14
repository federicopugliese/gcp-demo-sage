"""Thin async wrapper around the Gemini text-generation call."""

from sage.config import get_app_config
from sage.integrations.llm.client import get_genai_client


async def generate_text(prompt: str) -> str:
    config = get_app_config()
    client = get_genai_client()
    response = await client.aio.models.generate_content(model=config.chat_model, contents=prompt)
    return response.text
