"""Unit tests for the markdown chunker — pure logic, no GCP calls."""

from sage.domain.qa.chunking import split_into_chunks


def test_splits_by_heading_and_keeps_section_label() -> None:
    text = "# Intro\nHello world\n\n# Details\nMore text here"

    chunks = split_into_chunks(text, max_chars=1000)

    assert [chunk.section for chunk in chunks] == ["Intro", "Details"]
    assert chunks[0].text == "Hello world"
    assert chunks[1].text == "More text here"


def test_splits_long_section_into_multiple_chunks() -> None:
    paragraph = "word " * 400
    text = f"# Section\n{paragraph}\n\n{paragraph}"

    chunks = split_into_chunks(text, max_chars=500)

    assert len(chunks) > 1
    assert all(chunk.section == "Section" for chunk in chunks)
