"""Sage: assistente Q&A RAG del corso ITS ICT GCP."""

from pathlib import Path

from dotenv import load_dotenv

_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
if _ENV_FILE.exists():
    load_dotenv(_ENV_FILE, override=False)
