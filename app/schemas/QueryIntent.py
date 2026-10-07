from typing import Literal

from pydantic import BaseModel


class QueryFilters(BaseModel):
    field: str
    value: str
    operator: Literal["eq", "neq", "gt", "gte", "lt", "lte", "in"]


class QueryIntent(BaseModel):
    semantic_query: str | None = None
    filters: list[QueryFilters]
