from azure.search.documents.aio import SearchClient
from azure.search.documents.models import VectorizedQuery

from app.schemas.ChunkResponse import ChunkResponse


class SearchService:
    def __init__(self, search_client: SearchClient):
        self.search_client = search_client

    async def search(
        self,
        query: str,
        top_k: int,
    ) -> list[ChunkResponse]:
        documents = await self.search_client.search(
            search_text=query,
            top=top_k,
        )

        chunks: list[ChunkResponse] = []

        async for document in documents:
            response = ChunkResponse(
                chunk_id=document["ChunkId"],
                document_id=document["DocumentId"],
                sequence_number=document["SequenceNumber"],
                start_page=document["StartPage"],
                end_page=document["EndPage"],
                text=document["Text"],
                character_count=document["CharacterCount"],
                estimated_token_count=document["EstimatedTokenCount"],
                embedding_model=document["EmbeddingModel"],
                score=document.get("@search.score"),
            )

            chunks.append(response)

        return chunks

    async def vector_search(
        self, vector: list[float], top_k: int
    ) -> list[ChunkResponse]:
        vector_query = VectorizedQuery(
            vector=vector, fields="Embedding", k_nearest_neighbors=top_k
        )

        documents = await self.search_client.search(
            search_text=None,
            top=top_k,
            vector_queries=[vector_query],
        )

        chunks: list[ChunkResponse] = []

        async for document in documents:
            response = ChunkResponse(
                chunk_id=document["ChunkId"],
                document_id=document["DocumentId"],
                sequence_number=document["SequenceNumber"],
                start_page=document["StartPage"],
                end_page=document["EndPage"],
                text=document["Text"],
                character_count=document["CharacterCount"],
                estimated_token_count=document["EstimatedTokenCount"],
                embedding_model=document["EmbeddingModel"],
                score=document.get("@search.score"),
            )

            chunks.append(response)

        return chunks

    async def hybrid_search(
        self, query: str, vector: list[float], top_k: int
    ) -> list[ChunkResponse]:
        vector_query = VectorizedQuery(
            vector=vector, fields="Embedding", k_nearest_neighbors=top_k
        )

        documents = await self.search_client.search(
            search_text=query,
            top=top_k,
            vector_queries=[vector_query],
        )

        chunks: list[ChunkResponse] = []

        async for document in documents:
            response = ChunkResponse(
                chunk_id=document["ChunkId"],
                document_id=document["DocumentId"],
                sequence_number=document["SequenceNumber"],
                start_page=document["StartPage"],
                end_page=document["EndPage"],
                text=document["Text"],
                character_count=document["CharacterCount"],
                estimated_token_count=document["EstimatedTokenCount"],
                embedding_model=document["EmbeddingModel"],
                score=document.get("@search.score"),
            )

            chunks.append(response)

        return chunks
    
    async def document_search(
        self, query: str, vector: list[float], top_k: int, document_ids: list[str]
    ) -> list[ChunkResponse]:
        vector_query = VectorizedQuery(
            vector=vector, fields="Embedding", k_nearest_neighbors=top_k
        )

        filter_expression=None

        if len(document_ids) > 0:
            ids = ','.join(document_ids)
            filter_expression = f"search.in(DocumentId, '{ids}', ',')"

        documents = await self.search_client.search(
            search_text=query,
            top=top_k,
            vector_queries=[vector_query],
            filter=filter_expression
        )

        chunks: list[ChunkResponse] = []

        async for document in documents:
            response = ChunkResponse(
                chunk_id=document["ChunkId"],
                document_id=document["DocumentId"],
                sequence_number=document["SequenceNumber"],
                start_page=document["StartPage"],
                end_page=document["EndPage"],
                text=document["Text"],
                character_count=document["CharacterCount"],
                estimated_token_count=document["EstimatedTokenCount"],
                embedding_model=document["EmbeddingModel"],
                score=document.get("@search.score"),
            )

            chunks.append(response)

        return chunks
        
