import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial Document Management API"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    QDRANT_PATH: str = "./qdrant_storage"
    QDRANT_COLLECTION: str = "financial_docs"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
