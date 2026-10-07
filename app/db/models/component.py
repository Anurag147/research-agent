from sqlalchemy import String, Boolean, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Component(Base):
    __tablename__ = "Component"
    __table_args__ = {"schema": "research"}

    component_id: Mapped[int] = mapped_column(
        "ComponentId",
        primary_key=True,
    )

    sku: Mapped[str] = mapped_column(
        "SKU",
        String(30),
        nullable=False,
    )

    component_name: Mapped[str] = mapped_column(
        "ComponentName",
        String(400),
        nullable=False,
    )

    supplier_id: Mapped[str] = mapped_column(
        "SupplierId",
        String(20),
        ForeignKey("research.Supplier.SupplierId"),
        nullable=False,
    )

    country_of_origin: Mapped[str] = mapped_column(
        "CountryOfOrigin",
        String(200),
        nullable=False,
    )

    hs_code: Mapped[str | None] = mapped_column(
        "HSCode",
        String(30),
        nullable=True,
    )

    fy26_quantity: Mapped[int] = mapped_column(
        "FY26Quantity",
        Integer,
        nullable=False,
    )

    unit_price_usd: Mapped[float] = mapped_column(
        "UnitPriceUSD",
        Numeric(),
        nullable=False,
    )

    is_tariff_sensitive: Mapped[bool] = mapped_column(
        "IsTariffSensitive",
        Boolean,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        "IsActive",
        Boolean,
        nullable=False,
    )