import asyncio
import uuid

from ag_ui._generated.models import (
    EventType,
    RunAgentInput,
    RunFinishedEvent,
    CustomEvent,
    TextMessageStartEvent,
    TextMessageEndEvent,
    TextMessageContentEvent,
)
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

        intent = await self.query_intent_service.get_query_intent(user_message.content)
        intent_event = CustomEvent(
            name="research.intent.generated",
            value=intent.model_dump(mode="json"),
        )

        yield intent_event
        await asyncio.sleep(2)

        context = ""
        if intent.semantic_query is not None:
            if len(intent.filters) > 0:
                document_ids = (
                    await self.document_repository.get_document_ids_by_filters(
                        intent.filters
                    )
                )
                document_event = CustomEvent(
                    name="research.document_ids.generated",
                    value=document_ids,
                )
                yield document_event
                chunks = await self.retrieval_service.document_search(
                    intent.semantic_query, 10, document_ids
                )
                for chunk in chunks:
                    context += chunk.text + "\n\n"

                message_id = str(uuid.uuid4())
                message_started = TextMessageStartEvent(
                    type=EventType.TEXT_MESSAGE_START,
                    message_id=message_id,
                    role="assistant",
                )

                yield message_started

                async for event in self.llm_service.generate_chat(
                    user_message.content, context
                ):
                    message_content = TextMessageContentEvent(
                        type=EventType.TEXT_MESSAGE_CONTENT,
                        message_id=message_id,
                        delta=event,
                    )
                    yield message_content

                message_ended = TextMessageEndEvent(
                    type=EventType.TEXT_MESSAGE_END, message_id=message_id
                )
                yield message_ended
            else:
                chunks = await self.retrieval_service.hybrid_search(
                    intent.semantic_query
                )

        run_finished = RunFinishedEvent(
            type=EventType.RUN_FINISHED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id,
        )
        yield run_finished
