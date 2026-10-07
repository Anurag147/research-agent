from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SupplierDocument(Base):
    __tablename__ = "SupplierDocument"
    __table_args__ = {"schema": "research"}

    supplier_id: Mapped[str] = mapped_column(
        "SupplierId",
        String(20),
        ForeignKey("research.Supplier.SupplierId"),
        primary_key=True,
    )

    document_id: Mapped[str] = mapped_column(
        "DocumentId",
        ForeignKey("research.ResearchDocument.DocumentId"),
        primary_key=True,
    )

    relationship_type: Mapped[str] = mapped_column(
        "RelationshipType",
        String(100),
        nullable=False,
    )