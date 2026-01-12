"""Main Reflex application entry point."""

import reflex as rx
from fastapi import FastAPI

from app.pages.dashboard import dashboard_page
from app.pages.admin import admin_page
from app.pages.settings import settings_page
from app.server.api import health_router

# Create FastAPI instance for custom routes
api = FastAPI()
api.include_router(health_router)

# Create Reflex app with custom API
app = rx.App(
    theme=rx.theme(
        accent_color="indigo",
        gray_color="slate",
        # Use a static default; Reflex's color mode provider handles toggling.
        appearance="dark",
        radius="small",
        scaling="90%",
        panel_background="translucent",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
    api_transformer=api,
)

# Register pages
app.add_page(dashboard_page, route="/", title="Dashboard")
app.add_page(admin_page, route="/admin", title="Admin")
app.add_page(settings_page, route="/settings", title="Settings")
