from openai import AsyncOpenAI

from app.core.config import settings


class LLMService:
    def __init__(self, openai_client: AsyncOpenAI):
        self.openai_client = openai_client

    async def generate_chat(self, query: str, context: str):
        response = await self.openai_client.responses.create(
            model=settings.chat_deployment,
            instructions=(
                "You are a research assistant. "
                "Answer the user's question using only the provided context. "
                "If the context does not contain enough information, say so."
            ),
            stream=True,
            input=f"""
       Context:
       {context}

       Question:
       {query}
       """,
        )

        async for event in response:
            if event.type == "response.output_text.delta":
                yield event.delta
