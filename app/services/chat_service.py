import asyncio

from app.helpers.event_helper import generate_sse_event
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService


class ChatService:
    def __init__(self, retrieval_service: RetrievalService, llm_service: LLMService):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    async def generate_chat(self, query: str):
        yield generate_sse_event({"type": "retrieval.started"})
        chunks = await self.retrieval_service.search_vector(query, 10)
        yield generate_sse_event(
            {
                "type": "retrieval.completed",
                "chunk_count": len(chunks),
            }
        )
        context = ""

        for chunk in chunks:
            context += chunk.text + "\n\n"

        async for event in self.llm_service.generate_chat(query, context):
            yield generate_sse_event(
                {
                    "type": "message.delta",
                    "delta": event,
                }
            )
        await asyncio.sleep(2)
        yield generate_sse_event({"type": "retrieval.finished"})
