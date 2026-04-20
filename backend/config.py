from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings validated via Pydantic.
    Reads from environment variables or a .env file.
    """
    # Use Optional and default to empty string if not provided in env
    gemini_api_key: Optional[str] = Field(default="", description="Google Gemini API Key")
    environment: str = Field(default="development", description="App environment (development/production)")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Global settings instance
settings = Settings()
