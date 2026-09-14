"""Domain model for a retrieved document chunk."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    source: str
    section: str | None
    chunk_index: int
