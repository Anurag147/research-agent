from pydantic import BaseModel, Field


class DocumentSearchRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = Field(default=5, ge=1, le=50)
    document_ids: list[str] = Field(default_factory=list)
