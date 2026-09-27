from azure.core.credentials import AzureKeyCredential
from azure.search.documents.aio import SearchClient

from app.core.config import settings

search_client = SearchClient(
    settings.azure_search_endpoint,
    settings.azure_search_index,
    AzureKeyCredential(settings.azure_search_api_key),
)
