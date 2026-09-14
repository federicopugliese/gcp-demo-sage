"""Orchestrates retrieval-augmented answering for a single question."""

import asyncio
import time

from sage.domain.qa.generation import generate_answer
from sage.domain.qa.retrieval import retrieve_relevant_chunks
from sage.integrations.bigquery.question_log import log_question
from sage.webapp.apis.qa.schemas import AskResponse, SourceChunk


async def ask_question(question: str) -> AskResponse:
    start = time.monotonic()

    chunks = await retrieve_relevant_chunks(question)
    answer = await generate_answer(question, chunks)

    latency_ms = int((time.monotonic() - start) * 1000)

    # Cloud Run only guarantees CPU while a request is in flight (unless "CPU always
    # allocated" is on): a fire-and-forget background task can get frozen mid-write once the
    # response is sent. Awaiting it here keeps the write inside the request's CPU window.
    # log_question already logs and swallows its own failures (e.g. BigQuery not provisioned
    # yet), so it never turns into a 502 for the caller.
    await asyncio.to_thread(log_question, question, chunks, latency_ms)

    return AskResponse(
        answer=answer,
        sources=[
            SourceChunk(source=chunk.source, section=chunk.section, chunk_index=chunk.chunk_index)
            for chunk in chunks
        ],
    )
