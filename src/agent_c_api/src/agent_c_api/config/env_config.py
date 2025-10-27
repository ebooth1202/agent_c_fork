# config.py
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ## Application metadata
    APP_NAME: str = "Agent C FastAPI Backend"
    APP_DESCRIPTION: str = "A FastAPI backend for Agent C"
    CONTACT_NAME: str = "Joseph Ours"
    CONTACT_EMAIL: str = "joseph.ours@centricconsulting.com"
    LICENSE_NAME: str = "BSL 1.1"
    APP_VERSION: str = "0.1.0"

    # FastAPI and CORS settings
    ALLOWED_ORIGINS: list[str] = ["*"]
    HOST: str = os.environ.get("AGENT_C_API_HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("AGENT_C_API_PORT", 8000))
    RELOAD: bool = False

    # Agent settings
    CALLBACK_TIMEOUT: float = 300.0  # Timeout in seconds for stream callbacks

    # Profile API App
    PROFILING_ENABLED: bool = False

    # Session Configuration
    SESSION_TTL: int = 24 * 60 * 60  # 24 hours
    SESSION_CLEANUP_INTERVAL: int = 60 * 60  # 1 hour
    SESSION_CLEANUP_BATCH_SIZE: int = 100

# Can use getattr(settings, "SECRET_KEY", None) to get the value of SECRET_KEY
# Instantiate the settings
settings = Settings()