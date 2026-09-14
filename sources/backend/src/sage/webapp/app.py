"""FastAPI app instance for Sage."""

import logging

from fastapi import FastAPI

from sage.webapp.apis.health.router import router as health_router
from sage.webapp.apis.qa.router import router as qa_router

# Cloud Run collects container stdout/stderr as logs: without an explicit level, Python's
# root logger defaults to WARNING and INFO-level messages (e.g. "question logged to
# BigQuery") would silently never be emitted, even though the code path ran fine.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(
    title="Sage",
    description="Assistente Q&A RAG del corso ITS ICT GCP. Nessuna memoria di conversazione: "
    "ogni domanda è indipendente dalle altre.",
)

app.include_router(health_router)
app.include_router(qa_router, prefix="/api")
