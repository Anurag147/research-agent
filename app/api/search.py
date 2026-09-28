from fastapi import APIRouter

from app.infrastructure.azure_openai import openai_client
from app.infrastructure.azure_search import search_client
from app.schemas.ChunkResponse import ChunkResponse
from app.schemas.SearchRequest import SearchRequest
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.post("/search", response_model=list[ChunkResponse])
async def search(request: SearchRequest) -> list[ChunkResponse]:
    search_service = SearchService(search_client)

    chunks = await search_service.search(
        query=request.query,
        top_k=request.top_k,
    )

    return chunks


@router.post("/vector_search", response_model=list[ChunkResponse])
async def vector_search(request: SearchRequest) -> list[ChunkResponse]:
    search_service = SearchService(search_client)
    embedding_service = EmbeddingService(openai_client)
    retrieval_service = RetrievalService(search_service, embedding_service)
    chunks = await retrieval_service.search_vector(
        query=request.query,
        top_k=request.top_k,
    )
    return chunks
