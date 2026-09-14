"""Application settings, loaded from environment variables prefixed with SAGE_."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SAGE_", case_sensitive=False, extra="ignore")

    # GCP
    project_id: str
    region: str = "europe-west6"

    # Firestore
    firestore_collection: str = "chunks"
    top_k: int = 5

    # Vertex AI models
    chat_model: str = "gemini-2.5-flash"
    embedding_model: str = "text-embedding-004"
    embedding_dimension: int = 768

    # BigQuery
    bq_dataset: str = "sage_analytics"
    bq_table: str = "question_log"

    # Ingestion
    chunk_max_chars: int = 1500


@lru_cache
def get_app_config() -> AppConfig:
    return AppConfig()
