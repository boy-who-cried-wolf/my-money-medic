from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    # API settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Psychology Question Generator"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:@localhost/psych_questions"
    )

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # CORS settings
    ORIGINS: List[str] = ["*"]

    # LLM settings - Updated to use latest Gemini 2.5 Flash Preview by default
    LLM_PROVIDER: str = os.getenv(
        "LLM_PROVIDER", "gemini"
    )  # "openai", "anthropic", or "gemini" - now defaults to Gemini
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gemini-2.5-flash-preview-05-20")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    # Question generator settings
    MAX_QUESTIONS_PER_REQUEST: int = int(os.getenv("MAX_QUESTIONS_PER_REQUEST", "5"))
    MIN_BOOK_EXCERPT_LENGTH: int = int(os.getenv("MIN_BOOK_EXCERPT_LENGTH", "100"))

    # Book storage settings
    BOOK_DIRECTORY: str = os.getenv(
        "BOOK_DIRECTORY",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "books"
        ),
    )

    # Model configuration for Pydantic v2
    model_config = ConfigDict(
        env_file=".env", extra="allow"  # Allow extra fields from .env file
    )


settings = Settings()
