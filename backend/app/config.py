"""
Configuration de l'application.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Configuration de l'application.
    """
    # Application
    APP_NAME: str = "Calcule Heure API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Base de données
    DATABASE_URL: str = "sqlite:///./horaires.db"

    # API
    API_V1_PREFIX: str = "/api"

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8501"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
