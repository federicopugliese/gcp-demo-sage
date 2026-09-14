"""Retrieval step of the RAG pipeline: embed the question, fetch the nearest chunks."""

import asyncio
import logging

from google.api_core.exceptions import GoogleAPICallError

from sage.domain.qa.models import Chunk
from sage.integrations.firestore.chunks import find_nearest_chunks
from sage.integrations.llm.embeddings import embed_text

log = logging.getLogger(__name__)


async def retrieve_relevant_chunks(question: str) -> list[Chunk]:
    # embed_text and find_nearest_chunks use blocking (sync) GCP SDK clients.
    embedding = await asyncio.to_thread(embed_text, question)

    try:
        chunks = await asyncio.to_thread(find_nearest_chunks, embedding)
    except GoogleAPICallError:
        # Firestore not provisioned yet (database/collection missing), or not reachable: this
        # integration is meant to be added incrementally, so fall back to no context instead
        # of failing the request.
        log.warning(
            "Firestore non raggiungibile: rispondo senza contesto documentale", exc_info=True
        )
        return []

    log.info("Recuperati %d chunk da Firestore", len(chunks))
    return chunks
