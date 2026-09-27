from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

DATABASE_URL = URL.create(
    drivername="mssql+aioodbc",
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_server,
    port=settings.db_port,
    database=settings.db_name,
    query={
        "driver": settings.db_driver,
        "Encrypt": "yes",
        "TrustServerCertificate": "no",
    },
)

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass