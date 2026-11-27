from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

POSTGRES_DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.postgres_username,
    password=settings.postgres_password,
    host=settings.postgres_server,
    port=settings.postgres_port,
    database=settings.postgres_db_name,
)
postgres_engine = create_async_engine(POSTGRES_DATABASE_URL, pool_pre_ping=True)

PostgresSessionLocal = async_sessionmaker(
    bind=postgres_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class PostgresBase(DeclarativeBase):
    pass