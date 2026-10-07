from fastapi import APIRouter
from fastapi.params import Depends

from app.dependencies.services import get_query_intent_service
from app.schemas.QueryIntent import QueryIntent
from app.services.query_intent_service import QueryIntentService

router = APIRouter(
    prefix="/query",
    tags=["query"],
)


@router.post("/intent", response_model=QueryIntent)
async def query_intent(
    query: str,
    query_intent_service: QueryIntentService = Depends(get_query_intent_service),
):
    return await query_intent_service.get_query_intent(query)
