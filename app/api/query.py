from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependency import get_db
from app.dependencies.services import get_query_intent_service
from app.repositories.document_repository import DocumentRepository
from app.schemas.QueryIntent import QueryIntent
from app.services.query_intent_service import QueryIntentService

router = APIRouter(
    prefix="/query",
    tags=["query"],
)


@router.post("/intent", response_model=list[str])
async def query_intent(
    query: str,
    query_intent_service: QueryIntentService = Depends(get_query_intent_service),
    db: AsyncSession =  Depends(get_db)
):
    repository = DocumentRepository(db)
    query_intent = await query_intent_service.get_query_intent(query)
    print(query_intent)
    document_ids = await repository.get_document_ids_by_filters(query_intent.filters)
    return document_ids


