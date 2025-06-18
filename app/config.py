# app/config.py
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "opengvlab/internvl3-14b:free"  
    database_file: str = "recipe_ai.db" 
    cors_origins: List[str] = ["*"]  # Default to allow all for development

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS environment variable as a list."""
        if isinstance(self.cors_origins, str):
            # If it's a comma-separated string, split it
            if self.cors_origins == "*":
                return ["*"]
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra env variables
    )
