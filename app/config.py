# app/config.py
import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # OpenRouter settings
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "opengvlab/internvl3-14b:free"  
    
    # Database settings
    database_file: str = "recipe_ai.db" 
    
    # CORS settings
    # Can be set as:
    # - "*" for allow all origins
    # - A comma-separated list of allowed origins (e.g., "https://example.com,https://app.example.com")
    # - A list of origins in environment variables (e.g., ["https://example.com"])
    cors_origins: Union[List[str], str] = ["*"]
    
    # Additional CORS settings - these can also be customized in .env
    cors_allow_credentials: bool = True
    cors_allow_methods: Union[List[str], str] = ["*"]
    cors_allow_headers: Union[List[str], str] = ["*"]
    cors_expose_headers: Union[List[str], str] = []
    cors_max_age: int = 600  # 10 minutes

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS environment variable as a list."""
        return self._parse_list_or_str(self.cors_origins)
    
    @property
    def cors_allow_methods_list(self) -> List[str]:
        """Parse CORS_ALLOW_METHODS environment variable as a list."""
        return self._parse_list_or_str(self.cors_allow_methods)
    
    @property
    def cors_allow_headers_list(self) -> List[str]:
        """Parse CORS_ALLOW_HEADERS environment variable as a list."""
        return self._parse_list_or_str(self.cors_allow_headers)
    
    @property
    def cors_expose_headers_list(self) -> List[str]:
        """Parse CORS_EXPOSE_HEADERS environment variable as a list."""
        return self._parse_list_or_str(self.cors_expose_headers)
    
    def _parse_list_or_str(self, value: Union[List[str], str]) -> List[str]:
        """Helper method to parse string or list values."""
        if isinstance(value, str):
            # If it's a single asterisk, return as is
            if value == "*":
                return ["*"]
            # If it's a comma-separated string, split it
            return [item.strip() for item in value.split(",")]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra env variables
    )
