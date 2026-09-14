"""BigQuery client factory."""

from functools import lru_cache

from google.cloud import bigquery

from sage.config import get_app_config


@lru_cache
def get_bigquery_client() -> bigquery.Client:
    config = get_app_config()
    return bigquery.Client(project=config.project_id)
