from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import StreamingResponse

from app.dependencies.services import get_chat_service
from app.infrastructure.azure_openai import openai_client
from app.infrastructure.azure_search import search_client
from app.schemas.ChatRequest import ChatRequest
from app.services.chat_service import ChatService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

@router.post("")
async def chat(request: ChatRequest,chat_service:ChatService = Depends(get_chat_service)):
    return StreamingResponse(
        chat_service.generate_chat(request.query),
        media_type="text/event-stream",
    )