from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    document_id: UUID
    file_name: str
    document_title: str | None
    document_type: str | None
    page_count: int | None
    status: str
    uploaded_on_utc: datetime

    model_config = ConfigDict(from_attributes=True)