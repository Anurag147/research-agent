from uuid import UUID

from pydantic import BaseModel


class ChunkResponse(BaseModel):
    chunk_id: UUID
    document_id: str
    sequence_number: int
    start_page: int
    end_page: int
    text: str
    character_count: int
    estimated_token_count: int
    embedding_model: str
    score: float | None = None