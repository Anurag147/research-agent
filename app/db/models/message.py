from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres_database import PostgresBase

if TYPE_CHECKING:
    from app.db.models.conversations import Conversation

class Message(PostgresBase):
    __tablename__ = "messages"
    __table_args__ = {"schema": "chat"}

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    conversation_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("chat.conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    role : Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'completed'"),
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("''"),
    )

    message_metadata: Mapped[dict] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    conversation: Mapped[Conversation] = relationship(
        back_populates="messages",
        lazy="raise",
    )