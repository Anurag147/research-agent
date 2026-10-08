from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependency import get_db
from app.infrastructure.azure_openai import openai_client
from app.infrastructure.azure_search import search_client
from app.repositories.document_repository import DocumentRepository
from app.services.chat_service import ChatService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.query_intent_service import QueryIntentService
from app.services.research_service import ResearchService
from app.services.retrieval_service import RetrievalService
from app.services.search_service import SearchService


def get_search_service():
    search_service = SearchService(search_client)
    return search_service


def get_embedding_service():
    embedding_service = EmbeddingService(openai_client)
    return embedding_service


def get_llm_service():
    llm_service = LLMService(openai_client)
    return llm_service


def get_query_intent_service():
    query_intent_service = QueryIntentService(openai_client)
    return query_intent_service


def get_retrieval_service(
    search_service: SearchService = Depends(get_search_service),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
):
    retrieval_service = RetrievalService(search_service, embedding_service)
    return retrieval_service


def get_chat_service(
    llm_service: LLMService = Depends(get_llm_service),
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
):
    chat_service = ChatService(retrieval_service, llm_service)
    return chat_service


def get_document_repository(
    db: AsyncSession = Depends(get_db),
) -> DocumentRepository:
    return DocumentRepository(db)


def get_research_service(
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    query_intent_service: QueryIntentService = Depends(get_query_intent_service),
    llm_service: LLMService = Depends(get_llm_service),
    document_repository: DocumentRepository = Depends(get_document_repository),
):
    research_service = ResearchService(
        retrieval_service, query_intent_service, llm_service, document_repository
    )
    return research_service
