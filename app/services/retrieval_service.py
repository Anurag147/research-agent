from app.schemas.ChunkResponse import ChunkResponse
from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService


class RetrievalService:
    def __init__(
        self, search_service: SearchService, embedding_service: EmbeddingService
    ):
        self.search_service = search_service
        self.embedding_service = embedding_service

    async def search_vector(self, query: str, top_k: int) -> list[ChunkResponse]:
        vector = await self.embedding_service.generate_embedding(query)
        chunks = await self.search_service.vector_search(vector, top_k)
        return chunks

    async def hybrid_search(self, query: str, top_k: int) -> list[ChunkResponse]:
        vector = await self.embedding_service.generate_embedding(query)
        chunks = await self.search_service.hybrid_search(query, vector, top_k)
        return chunks
