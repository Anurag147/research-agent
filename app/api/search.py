from fastapi import APIRouter
from fastapi.params import Depends

from app.dependencies.services import get_retrieval_service, get_search_service
from app.schemas.ChunkResponse import ChunkResponse
from app.schemas.SearchRequest import SearchRequest
from app.services.retrieval_service import RetrievalService
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.post("/search", response_model=list[ChunkResponse])
async def search(
    request: SearchRequest, search_service: SearchService = Depends(get_search_service)
) -> list[ChunkResponse]:
    chunks = await search_service.search(
        query=request.query,
        top_k=request.top_k,
    )

    return chunks


@router.post("/vector_search", response_model=list[ChunkResponse])
async def vector_search(
    request: SearchRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
) -> list[ChunkResponse]:
    chunks = await retrieval_service.search_vector(
        query=request.query,
        top_k=request.top_k,
    )
    return chunks


@router.post("/hybrid_search", response_model=list[ChunkResponse])
async def hybrid_search(
    request: SearchRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
) -> list[ChunkResponse]:
    chunks = await retrieval_service.hybrid_search(
        query=request.query,
        top_k=request.top_k,
    )
    return chunks
