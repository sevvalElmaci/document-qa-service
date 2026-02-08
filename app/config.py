"""
Uygulama konfigürasyon ayarları
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Uygulama ayarları"""
    
    # Uygulama
    APP_NAME: str = "Document QA Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"  # veya mistral, phi3, vb.
    OLLAMA_TIMEOUT: int = 120
    
    # Embedding
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"


    # Vektör Veritabanı
    VECTOR_DB_TYPE: str = "faiss"
    VECTOR_DB_PATH: str = "./data/vectordb"
    
    # Doküman İşleme
    DOCUMENTS_PATH: str = "./data/documents"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list = [".txt", ".pdf", ".md"]
    
    # RAG
    TOP_K_RESULTS: int = 3  # Kaç doküman parçası döndürülecek
    MIN_RELEVANCE_SCORE: float = 0.5
    
    # LLM
    MAX_TOKENS: int = 512
    TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings
settings = Settings()


def get_settings() -> Settings:
    """Settings instance'ını döndürür (dependency injection)"""
    return settings
