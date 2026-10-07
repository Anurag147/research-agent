from app.helpers.event_helper import generate_sse_event
from app.repositories.document_repository import DocumentRepository
from app.services.llm_service import LLMService
from app.services.query_intent_service import QueryIntentService
from app.services.retrieval_service import RetrievalService


class ResearchService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        query_intent_service: QueryIntentService,
        llm_service: LLMService,
        document_repository: DocumentRepository,
    ):
        self.retrieval_service = retrieval_service
        self.query_intent_service = query_intent_service
        self.llm_service = llm_service
        self.document_repository = document_repository

    async def research_document(self, query: str):
        yield generate_sse_event({"type": "retrieval.started"})
        intent = await self.query_intent_service.get_query_intent(query)
        yield generate_sse_event({"type": "intent.generated", "intent": intent})
        context=''
        if intent.semantic_query is not None:
            yield generate_sse_event({"type": "intent.semantic_query"})
            if len(intent.filters) > 0:
                document_ids = (
                    await self.document_repository.get_document_ids_by_filters(intent.filters)
                )
                yield generate_sse_event(
                    {"type": "intent.document_ids", "document_ids": document_ids}
                )
                chunks = await self.retrieval_service.document_search(
                    intent.semantic_query, document_ids
                )
            else:
                chunks = await self.retrieval_service.hybrid_search(intent.semantic_query)

            yield generate_sse_event({"type": "intent.chunks", "chunks": chunks})
            for chunk in chunks:
                context += chunk.text + "\n\n"

            async for event in self.llm_service.generate_chat(query, context):
                yield generate_sse_event(
                    {
                        "type": "message.delta",
                        "delta": event,
                    }
                )
            yield generate_sse_event({"type": "retrieval.finished"})

        else:
            yield generate_sse_event({"type": "intent.non_semantic_query"})
