from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Manages the central configuration for the test framework.
    It reads environment-specific variables from a .env file or system environment.
    """
    # Default backend API base URL for local development
    api_base_url: str = "http://127.0.0.1:8000/api"

    # Default frontend base URL for local development
    ui_base_url: str = "http://127.0.0.1:5500"

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


# Singleton instance of the settings to be used across the framework
settings = Settings()