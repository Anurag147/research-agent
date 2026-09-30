from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependency import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.DocumentResponse import DocumentResponse

router = APIRouter(
    prefix="/api",
    tags=["documents"],
)

@router.get("/documents", response_model=list[DocumentResponse])
async def get_documents(
    db: AsyncSession = Depends(get_db)
):
    repository = DocumentRepository(db)
    documents = await repository.get_all()

    return documents