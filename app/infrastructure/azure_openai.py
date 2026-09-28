from openai import AsyncOpenAI

from app.core.config import settings

openai_client = AsyncOpenAI(
    base_url=settings.azure_openai_endpoint, api_key=settings.azure_openai_api_key
)
