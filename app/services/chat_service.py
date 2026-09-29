import asyncio

from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService


class ChatService:
    def __init__(self, retrieval_service: RetrievalService):
        self.retrieval_service = retrieval_service

    async def generate_chat(self, query:str):
        yield 'data: {"type":"started"} \n\n'
        await asyncio.sleep(2)

        yield 'data: {"type":"in-progress"} \n\n'
        await asyncio.sleep(2)

        yield 'data: {"type":"finished"} \n\n'