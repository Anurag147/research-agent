from openai import AsyncOpenAI

from app.core.config import settings


class EmbeddingService:
    def __init__(self, openai_client: AsyncOpenAI):
        self.openai_client = openai_client

    async def generate_embedding(self, text: str) -> list[float]:
        response = await self.openai_client.embeddings.create(
            input=text, model=settings.azure_openai_embedding_deployment
        )
        if response:
            return response.data[0].embedding
        else:
            return []
