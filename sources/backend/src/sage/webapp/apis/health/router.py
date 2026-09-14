"""GET /health — used by Cloud Run and by local `docker run` health checks."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
