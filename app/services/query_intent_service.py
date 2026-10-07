from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.QueryIntent import QueryIntent


class QueryIntentService:
    def __init__(self, openai_client: AsyncOpenAI):
        self.openai_client = openai_client

    async def get_query_intent(self, query: str):
        instructions = """
        You are a query intent extraction service for a contract research system.

        Your task is to convert the user's natural-language query into:
        1. A semantic query used to search document content.
        2. Zero or more metadata filters used to select documents.

        Available document metadata:

        - document_type
          Type: string
          Allowed values: Logistics, Manufacturing, Supply, Purchase

        - status
          Type: string
          Allowed values: Active, Expired, Terminated

        - effective_date
          Type: date

        - supplier
          Type: string
          Description:
          The supplier, vendor, counterparty, company, or organization
          associated with the agreement.
        
          When the user refers to a named company, vendor, supplier,
          counterparty, or organization in the context of an agreement,
          treat that name as a supplier metadata filter.

        Supported filter operators:

        - eq  : equal to
        - neq : not equal to
        - gt  : greater than
        - gte : greater than or equal to
        - lt  : less than
        - lte : less than or equal to
        - in  : matches one of multiple values

        Rules:

        - Only use metadata fields listed above.
        - Never invent metadata fields.
        - Only create a filter when the user's query explicitly states or
          clearly implies a metadata constraint.
        - Do not invent filter values.
        - Use only the supported operators listed above.
        - Use the exact allowed value when a field defines allowed values.
        - Put document-content concepts into semantic_query.
        - Do not repeat metadata constraints in semantic_query when they
          have already been represented as filters.
        - If the query contains no metadata constraints, return an empty
          filters list.
        - If the query is purely metadata-based and contains nothing that
          requires document-content search, set semantic_query to null.
        - For dates, return values in YYYY-MM-DD format when a specific
          date can be determined.
        - Do not generate SQL.
        - Do not answer the user's question.
        - Only extract the query intent according to the provided output schema.
        - Named suppliers, vendors, counterparties, companies, or
          organizations should be extracted into the supplier field
          when they identify which agreements should be searched.
        - Remove the supplier name from semantic_query after extracting
          it as a metadata filter.
        """

        response = await self.openai_client.responses.parse(
            instructions=instructions,
            input=query,
            text_format=QueryIntent,
            model=settings.chat_deployment,
        )
        return response.output_parsed
