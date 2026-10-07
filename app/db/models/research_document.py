from sqlalchemy import String, Boolean, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ResearchDocument(Base):
    __tablename__ = "ResearchDocument"
    __table_args__ = {"schema": "research"}

    document_id: Mapped[str] = mapped_column(
        "DocumentId",
        primary_key=True,
    )

    file_name: Mapped[str] = mapped_column(
        "FileName",
        String(510),
        nullable=False,
    )

    document_type: Mapped[str] = mapped_column(
        "DocumentType",
        String(200),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        "SourceType",
        String(20),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        "Category",
        String(200),
        nullable=False,
    )

    effective_year: Mapped[int | None] = mapped_column(
        "EffectiveYear",
        SmallInteger,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        "IsActive",
        Boolean,
        nullable=False,
    )