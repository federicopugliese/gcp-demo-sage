"""HTTP boundary for the question-answering endpoint. No business logic here: the router
only calls the service and translates domain errors into HTTPException.
"""

from fastapi import APIRouter, HTTPException

from sage.domain.qa.exceptions import SageError
from sage.webapp.apis.qa.schemas import AskRequest, AskResponse
from sage.webapp.apis.qa.service import ask_question

router = APIRouter(tags=["qa"])


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    try:
        return await ask_question(request.question)
    except SageError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
