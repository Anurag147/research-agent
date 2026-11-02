import uuid

from ag_ui._generated.models import (
    EventType,
    RunAgentInput,
    RunFinishedEvent,
    CustomEvent,
    TextMessageStartEvent,
    TextMessageEndEvent,
    TextMessageContentEvent,
    RunErrorEvent,
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

        try:
            user_message = next(
                (msg for msg in reversed(input_data.messages) if msg.role == "user"),
                None,
            )
            print(user_message.content if user_message else "No user query")
            run_started = RunStartedEvent(
                type=EventType.RUN_STARTED,
                thread_id=input_data.thread_id,
                run_id=input_data.run_id,
            )

            yield run_started

            intent_task = {
                "taskId": "intent-analysis",
                "title": "Analyzing research query",
                "status": "running",
                "summary": "Identifying search intent and document filters",
            }

            yield CustomEvent(
                name="research.task.updated",
                value=intent_task,
            )
            intent = await self.query_intent_service.get_query_intent(
                user_message.content
            )

            yield CustomEvent(
                name="research.task.updated",
                value={
                    **intent_task,
                    "status": "completed",
                    "summary": "Research query analyzed successfully",
                },
            )

            context = ""
            if intent.semantic_query is not None:
                if len(intent.filters) > 0:
                    print("Generated filters:", intent.filters)
                    filter_task = {
                        "taskId": "document-filtering",
                        "title": "Filtering documents",
                        "status": "running",
                        "summary": "Identifying documents matching the research criteria",
                    }
                    filter_task_event = CustomEvent(
                        name="research.task.updated",
                        value=filter_task,
                    )
                    yield filter_task_event
                    document_ids = (
                        await self.document_repository.get_document_ids_by_filters(
                            intent.filters
                        )
                    )
                    print("Document ids:", document_ids)
                    yield CustomEvent(
                        name="research.task.updated",
                        value={
                            **filter_task,
                            "status": "completed",
                            "summary": f"Identified {len(document_ids)} matching documents",
                        },
                    )
                    retrieval_task = {
                        "taskId": "semantic-retrieval",
                        "title": "Searching document content",
                        "status": "running",
                        "summary": "Retrieving relevant passages using semantic and hybrid search",
                    }

                    yield CustomEvent(
                        name="research.task.updated",
                        value=retrieval_task,
                    )
                    chunks = await self.retrieval_service.document_search(
                        intent.semantic_query, 10, document_ids
                    )
                    yield CustomEvent(
                        name="research.task.updated",
                        value={
                            **retrieval_task,
                            "status": "completed",
                            "summary": f"Retrieved {len(chunks)} relevant document passages",
                        },
                    )
                else:
                    retrieval_task = {
                        "taskId": "semantic-retrieval",
                        "title": "Searching document content",
                        "status": "running",
                        "summary": "Retrieving relevant passages using semantic and hybrid search",
                    }

                    yield CustomEvent(
                        name="research.task.updated",
                        value=retrieval_task,
                    )
                    chunks = await self.retrieval_service.hybrid_search(
                        intent.semantic_query,10
                    )
                    yield CustomEvent(
                        name="research.task.updated",
                        value={
                            **retrieval_task,
                            "status": "completed",
                            "summary": f"Retrieved {len(chunks)} relevant document passages",
                        },
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
            run_finished = RunFinishedEvent(
                type=EventType.RUN_FINISHED,
                thread_id=input_data.thread_id,
                run_id=input_data.run_id,
            )
            yield run_finished
        except Exception as e:
            print(e)
            yield RunErrorEvent(
                message="unable to run research document",
            )
