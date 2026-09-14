"""Errors raised by the QA pipeline. Plain Python exceptions, no FastAPI imports."""


class SageError(Exception):
    """Base class for QA-pipeline failures. Translated to HTTPException at the API boundary."""
