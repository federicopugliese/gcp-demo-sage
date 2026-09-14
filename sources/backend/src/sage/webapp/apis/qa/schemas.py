"""Request/response models for POST /api/ask."""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class SourceChunk(BaseModel):
    source: str
    section: str | None = None
    chunk_index: int


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
