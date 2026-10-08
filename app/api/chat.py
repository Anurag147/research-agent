from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import StreamingResponse

from app.dependencies.services import get_chat_service, get_research_service
from app.schemas.ChatRequest import ChatRequest
from app.services.chat_service import ChatService
from app.services.research_service import ResearchService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("")
async def chat(
    request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)
):
    return StreamingResponse(
        chat_service.generate_chat(request.query),
        media_type="text/event-stream",
    )


@router.post("/research")
async def research(
    request: ChatRequest,
    research_service: ResearchService = Depends(get_research_service),
):
    return StreamingResponse(
        research_service.research_document(request.query),
        media_type="text/event-stream",
    )
