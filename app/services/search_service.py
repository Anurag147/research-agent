from azure.search.documents.aio import SearchClient

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
