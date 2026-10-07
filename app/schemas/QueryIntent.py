from typing import Literal

from pydantic import BaseModel


class QueryFilter(BaseModel):
    table: Literal[
        "ResearchDocument",
        "Supplier",
        "Component",
    ]

    field: str

    value: str | int | float | bool

    operator: Literal[
        "eq",
        "neq",
        "gt",
        "gte",
        "lt",
        "lte",
        "in",
    ]


class QueryIntent(BaseModel):
    semantic_query: str | None = None
    filters: list[QueryFilter]