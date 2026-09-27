
from fastapi import APIRouter

from app.infrastructure.azure_search import search_client
from app.schemas.ChunkResponse import ChunkResponse
from app.schemas.SearchRequest import SearchRequest
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
