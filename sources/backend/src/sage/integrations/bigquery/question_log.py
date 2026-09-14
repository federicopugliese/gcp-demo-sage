"""Writes one row per question to BigQuery for analytics (see devops/cloud/bigquery.tf).

Called synchronously from the request path (see webapp/apis/qa/service.py) rather than as a
FastAPI background task: on Cloud Run, CPU is only guaranteed to be allocated while a request
is in flight, so a background write could be frozen or killed once the response is sent.

This integration is meant to be added incrementally: any failure here (dataset/table not
provisioned yet, no permissions, ...) is logged and swallowed rather than propagated, so it
never turns a working answer into a 502 for the caller.
"""

import json
import logging
from datetime import UTC, datetime

from google.api_core.exceptions import GoogleAPICallError

from sage.config import get_app_config
from sage.domain.qa.models import Chunk
from sage.integrations.bigquery.client import get_bigquery_client

log = logging.getLogger(__name__)


def log_question(question: str, chunks: list[Chunk], latency_ms: int) -> None:
    config = get_app_config()
    table_ref = f"{config.project_id}.{config.bq_dataset}.{config.bq_table}"

    row = {
        "created_at": datetime.now(UTC).isoformat(),
        "question": question,
        "sources": json.dumps([chunk.source for chunk in chunks]),
        "latency_ms": latency_ms,
    }

    try:
        client = get_bigquery_client()
        errors = client.insert_rows_json(table_ref, [row])
        if errors:
            log.error("BigQuery insert errors on %s: %s", table_ref, errors)
        else:
            log.info("Question logged to BigQuery (%s, latency_ms=%d)", table_ref, latency_ms)
    except GoogleAPICallError:
        # Dataset/table not provisioned yet, or no permissions: this integration is meant to
        # be added incrementally, so skip logging instead of failing the request.
        log.warning(
            "BigQuery non raggiungibile (%s non ancora creata?): logging saltato",
            table_ref,
            exc_info=True,
        )
    except Exception:
        log.exception("Failed to log question to BigQuery (%s)", table_ref)
