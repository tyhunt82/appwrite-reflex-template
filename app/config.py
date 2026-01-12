"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "Appwrite & Reflex Template App"
    debug: bool = True

    # Appwrite
    appwrite_endpoint: str = os.getenv("APPWRITE_ENDPOINT")
    appwrite_project_id: str = os.getenv("APPWRITE_PROJECT_ID")

    appwrite_api_key: str = os.getenv("APPWRITE_API_KEY")
    appwrite_dev_api_key: str = os.getenv("APPWRITE_DEV_API_KEY")

    appwrite_database_id: str = os.getenv("APPWRITE_DATABASE_ID")
    appwrite_storage_id: str = os.getenv("APPWRITE_STORAGE_ID")


    # UI Defaults
    default_theme: str = "system"  # "light", "dark", "system"
    sidebar_default_collapsed: bool = False





settings = Settings()
