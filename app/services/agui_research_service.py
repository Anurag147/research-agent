import asyncio
from ag_ui._generated.models import EventType, RunAgentInput, RunFinishedEvent
from ag_ui.core import RunStartedEvent

from app.repositories.document_repository import DocumentRepository
from app.services.llm_service import LLMService
from app.services.query_intent_service import QueryIntentService
from app.services.retrieval_service import RetrievalService


class AguiResearchService:
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
        self.llm_service = llm_service
        self.document_repository = document_repository

    async def research_document(self, input_data: RunAgentInput):
        user_message = next(
            (msg for msg in reversed(input_data.messages) if msg.role == "user"), None
        )
        print(user_message.content if user_message else "No user query")
        run_started = RunStartedEvent(
            type=EventType.RUN_STARTED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id,
        )

        yield run_started
        await asyncio.sleep(2)

        run_finished = RunFinishedEvent(
            type=EventType.RUN_FINISHED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id,
        )
        yield run_finished
