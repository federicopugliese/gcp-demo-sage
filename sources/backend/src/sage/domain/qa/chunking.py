"""Markdown chunking, shared by the ingestion script (utils/ingest_documents.py) and
tests. Pure logic, no I/O and no GCP calls, so it stays trivially testable.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RawChunk:
    text: str
    section: str | None
    chunk_index: int


def split_into_chunks(markdown_text: str, max_chars: int = 1500) -> list[RawChunk]:
    """Split markdown into chunks, using the nearest heading above each chunk as its section."""
    chunks: list[RawChunk] = []

    for heading, body in _split_by_heading(markdown_text):
        for piece in _split_by_size(body, max_chars):
            if not piece.strip():
                continue
            chunks.append(RawChunk(text=piece.strip(), section=heading, chunk_index=len(chunks)))

    return chunks


def _split_by_heading(markdown_text: str) -> list[tuple[str | None, str]]:
    sections: list[tuple[str | None, str]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in markdown_text.splitlines():
        if line.startswith("#"):
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines)))
            current_heading = line.lstrip("#").strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, "\n".join(current_lines)))

    return sections or [(None, markdown_text)]


def _split_by_size(text: str, max_chars: int) -> list[str]:
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    pieces: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) > max_chars and current:
            pieces.append(current)
            current = paragraph
        else:
            current = candidate
    pieces.append(current)

    return pieces
