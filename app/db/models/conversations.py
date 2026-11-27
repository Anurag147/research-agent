from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres_database import PostgresBase

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.message import Message


class Conversation(PostgresBase):
    __tablename__ = "conversations"
    __table_args__ = {"schema": "chat"}

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[UUID] = mapped_column(
        "user_id",
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    messages: Mapped[list[Message]] = relationship(
        back_populates="conversation",
        lazy="raise",
    )