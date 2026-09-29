import logging

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as document_router
from app.api.health import router as health_router
from app.api.search import router as search_router

logging.basicConfig(level=logging.DEBUG)
app = FastAPI(
    title="FastAPI",
    description="FastAPI",
    version="0.0.1",
)

app.include_router(health_router)
app.include_router(document_router)
app.include_router(search_router)
app.include_router(chat_router)
