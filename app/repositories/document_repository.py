from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.helpers.DocumentQueryBuilder import DocumentQueryBuilder
from app.schemas.QueryIntent import QueryFilter


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        statement = select(Document)
        result = await self.db.execute(statement)
        documents = result.scalars().all()
        return documents

    async def get_document_ids_by_filters(
        self,
        filters: list[QueryFilter],
    ):
        statement = DocumentQueryBuilder.build_query(filters)
        result = await self.db.execute(statement)
        document_ids = result.scalars().all()
        return document_ids
