from sqlalchemy import String, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Supplier(Base):
    __tablename__ = "Supplier"
    __table_args__ = {"schema": "research"}

    supplier_id: Mapped[str] = mapped_column(
        "SupplierId",
        String(20),
        primary_key=True,
    )

    supplier_name: Mapped[str] = mapped_column(
        "SupplierName",
        String(400),
        nullable=False,
    )

    primary_country: Mapped[str] = mapped_column(
        "PrimaryCountry",
        String(200),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        "Category",
        String(200),
        nullable=False,
    )

    criticality: Mapped[str] = mapped_column(
        "Criticality",
        String(60),
        nullable=False,
    )

    annual_spend_usd: Mapped[float | None] = mapped_column(
        "AnnualSpendUSD",
        Numeric(),
        nullable=True,
    )

    risk_tier: Mapped[str | None] = mapped_column(
        "RiskTier",
        String(60),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        "IsActive",
        Boolean,
        nullable=False,
    )