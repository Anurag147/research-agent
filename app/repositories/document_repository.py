from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        statement = select(Document)
        result = await self.db.execute(statement)
        documents = result.scalars().all()
        return documents
