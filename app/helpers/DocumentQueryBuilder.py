from sqlalchemy import select

from app.db.models.component import Component
from app.db.models.research_document import ResearchDocument
from app.db.models.supplier import Supplier
from app.db.models.supplier_document import SupplierDocument
from app.schemas.QueryIntent import QueryFilter


class DocumentQueryBuilder:
    filter_map = {
        "document_type": ResearchDocument.document_type,
        "is_active": ResearchDocument.is_active,
        "effective_year": ResearchDocument.effective_year,
        "supplier_name": Supplier.supplier_name,
    }

    @classmethod
    def build_query(cls, filters: list[QueryFilter]):
        statement = select(ResearchDocument.document_id)
        tables = {f.table for f in filters}

        if "Component" in tables:
            statement = statement.join(
                SupplierDocument,
                SupplierDocument.document_id == ResearchDocument.document_id,
            )

            statement = statement.join(
                Supplier,
                Supplier.supplier_id == SupplierDocument.supplier_id,
            )

            statement = statement.join(
                Component,
                Component.supplier_id == Supplier.supplier_id,
            )

        elif "Supplier" in tables:
            statement = statement.join(
                SupplierDocument,
                SupplierDocument.document_id == ResearchDocument.document_id,
            )

            statement = statement.join(
                Supplier,
                Supplier.supplier_id == SupplierDocument.supplier_id,
            )

        for f in filters:
            column = cls.filter_map.get(f.field)

            if column is not None:
                if f.operator == "eq":
                    statement = statement.where(column == f.value)

                elif f.operator == "neq":
                    statement = statement.where(column != f.value)

                elif f.operator == "gt":
                    statement = statement.where(column > f.value)

                elif f.operator == "gte":
                    statement = statement.where(column >= f.value)

                elif f.operator == "lt":
                    statement = statement.where(column < f.value)

                elif f.operator == "lte":
                    statement = statement.where(column <= f.value)

        return statement
