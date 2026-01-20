"""Application configuration using Pydantic Settings."""

from __future__ import annotations

from typing import Any, ClassVar

import reflex as rx
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    appwrite_endpoint: str | None = Field(default=None, validation_alias="APPWRITE_ENDPOINT")
    appwrite_project_id: str | None = Field(default=None, validation_alias="APPWRITE_PROJECT_ID")

    appwrite_api_key: str | None = Field(default=None, validation_alias="APPWRITE_API_KEY")
    appwrite_dev_api_key: str | None = Field(default=None, validation_alias="APPWRITE_DEV_API_KEY")

    appwrite_database_id: str | None = Field(default=None, validation_alias="APPWRITE_DATABASE_ID")
    appwrite_storage_id: str | None = Field(default=None, validation_alias="APPWRITE_STORAGE_ID")


    # UI Defaults
    sidebar_default_collapsed: bool = False
    theme: ClassVar[Any] = rx.theme(
        accent_color="blue",
        gray_color="slate",
        appearance="dark",
        radius="small",
        scaling="90%",
        panel_background="translucent",
    )



settings = Settings()
