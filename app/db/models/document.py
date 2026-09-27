from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, Integer, Unicode, UnicodeText
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Document(Base):
    __tablename__ = "Documents"
    __table_args__ = {"schema": "dbo"}

    document_id: Mapped[UUID] = mapped_column(
        "DocumentId",
        UNIQUEIDENTIFIER,
        primary_key=True,
    )

    file_name: Mapped[str] = mapped_column(
        "FileName",
        Unicode(500),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        "ContentType",
        Unicode(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        "FileSize",
        BigInteger,
        nullable=False,
    )

    container_name: Mapped[str] = mapped_column(
        "ContainerName",
        Unicode(200),
        nullable=False,
    )

    blob_path: Mapped[str] = mapped_column(
        "BlobPath",
        Unicode(1000),
        nullable=False,
    )

    ocr_blob_path: Mapped[str | None] = mapped_column(
        "OcrBlobPath",
        Unicode(1000),
        nullable=True,
    )

    search_document_id: Mapped[str | None] = mapped_column(
        "SearchDocumentId",
        Unicode(200),
        nullable=True,
    )

    document_title: Mapped[str | None] = mapped_column(
        "DocumentTitle",
        Unicode(500),
        nullable=True,
    )

    document_type: Mapped[str | None] = mapped_column(
        "DocumentType",
        Unicode(100),
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        "Language",
        Unicode(20),
        nullable=True,
    )

    page_count: Mapped[int | None] = mapped_column(
        "PageCount",
        Integer,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        "Status",
        Unicode(50),
        nullable=False,
    )

    processing_started_on_utc: Mapped[datetime | None] = mapped_column(
        "ProcessingStartedOnUtc",
        DateTime,
        nullable=True,
    )

    processing_completed_on_utc: Mapped[datetime | None] = mapped_column(
        "ProcessingCompletedOnUtc",
        DateTime,
        nullable=True,
    )

    uploaded_by: Mapped[str] = mapped_column(
        "UploadedBy",
        Unicode(256),
        nullable=False,
    )

    uploaded_on_utc: Mapped[datetime] = mapped_column(
        "UploadedOnUtc",
        DateTime,
        nullable=False,
    )

    last_modified_on_utc: Mapped[datetime | None] = mapped_column(
        "LastModifiedOnUtc",
        DateTime,
        nullable=True,
    )

    deleted_on_utc: Mapped[datetime | None] = mapped_column(
        "DeletedOnUtc",
        DateTime,
        nullable=True,
    )

    ocr_file_path: Mapped[str | None] = mapped_column(
        "OCRFilePath",
        UnicodeText,
        nullable=True,
    )
