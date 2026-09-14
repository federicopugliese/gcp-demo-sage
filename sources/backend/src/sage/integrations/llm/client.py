"""Google Gen AI SDK client, in Vertex AI mode (ADC-based, no API key)."""

from functools import lru_cache

from google import genai

from sage.config import get_app_config


@lru_cache
def get_genai_client() -> genai.Client:
    config = get_app_config()
    return genai.Client(vertexai=True, project=config.project_id, location=config.region)
