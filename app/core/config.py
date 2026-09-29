from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    entra_tenant_id: str
    entra_audience: str
    entra_scope: str
    entra_client_id: str
    db_server: str
    db_port: int = 1433
    db_name: str
    db_username: str
    db_password: str
    db_driver: str = "ODBC Driver 18 for SQL Server"
    azure_search_endpoint: str
    azure_search_index: str
    azure_search_api_key: str
    azure_openai_endpoint:str
    azure_openai_api_key:str
    azure_openai_embedding_deployment:str
    chat_deployment :str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()
