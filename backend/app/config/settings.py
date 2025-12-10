"""
Application Settings
Loads configuration from environment variables
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str
    
    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "book_chunks"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Agent Configuration
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 2000
    
    # Indexing Configuration
    chunk_size: int = 800
    chunk_overlap: int = 100
    book_url: str = ""
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
