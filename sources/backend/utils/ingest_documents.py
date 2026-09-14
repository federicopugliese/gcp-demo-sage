"""Standalone script: chunk the markdown documents in data/ and load them into Firestore.

This is the only ingestion utility in the project. It both computes chunk embeddings and
upserts them into Firestore using the same schema the API queries at request time (see
sage/integrations/firestore/chunks.py) — students query the resulting collection, they
don't need to build this pipeline themselves.

Usage:
    uv run python utils/ingest_documents.py [--data-dir data]

Re-running is safe: each file's existing chunks are deleted and re-written, so editing a
document and re-running the script keeps Firestore in sync with data/.
"""

import argparse
import logging
from pathlib import Path

import sage  # noqa: F401  (triggers the .env bootstrap in sage/__init__.py)
from sage.config import get_app_config
from sage.domain.qa.chunking import split_into_chunks
from sage.integrations.firestore.chunks import add_chunk, delete_chunks_for_source
from sage.integrations.llm.embeddings import embed_text

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ingest_documents")


def ingest_file(path: Path) -> int:
    config = get_app_config()
    source = path.name
    text = path.read_text(encoding="utf-8")
    chunks = split_into_chunks(text, max_chars=config.chunk_max_chars)

    delete_chunks_for_source(source)

    for chunk in chunks:
        embedding = embed_text(chunk.text)
        add_chunk(
            chunk_id=f"{source}-{chunk.chunk_index}",
            text=chunk.text,
            embedding=embedding,
            source=source,
            section=chunk.section,
            chunk_index=chunk.chunk_index,
        )

    log.info("Indicizzato %s: %d chunk", source, len(chunks))
    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data", help="Cartella con i file .md da indicizzare")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    md_files = sorted(data_dir.glob("*.md"))
    if not md_files:
        log.warning("Nessun file .md trovato in %s", data_dir)
        return

    total_chunks = sum(ingest_file(path) for path in md_files)
    log.info("Completato: %d file, %d chunk totali", len(md_files), total_chunks)


if __name__ == "__main__":
    main()
