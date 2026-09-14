"""Adapters for external services: Vertex AI (LLM + embeddings), Firestore, BigQuery.

Main areas:
- llm: Google Gen AI SDK client, in Vertex AI mode (text generation + embeddings).
- firestore: chunk storage and vector search (find_nearest).
- bigquery: best-effort analytics logging of questions.
"""
