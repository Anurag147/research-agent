import asyncio

from app.helpers.event_helper import generate_sse_event
from app.services.retrieval_service import RetrievalService


class ChatService:
    def __init__(self, retrieval_service: RetrievalService):
        self.retrieval_service = retrieval_service

    async def generate_chat(self, query: str):
        yield generate_sse_event({"type": "retrieval.started"})
        chunks = await self.retrieval_service.search_vector(query, 10)
        yield generate_sse_event(
            {
                "type": "retrieval.completed",
                "chunk_count": len(chunks),
            }
        )
        await asyncio.sleep(2)
        yield generate_sse_event({"type": "retrieval.finished"})
