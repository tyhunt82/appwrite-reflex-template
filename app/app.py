"""Main Reflex application entry point."""

import reflex as rx

# Pages
from app.pages.landing import landing_page
from app.pages.dashboard import dashboard_page
from app.pages.admin import admin_page
from app.pages.settings import settings_page

# Routers
from app.server.api import register_health_routes

# Config
from app.config import settings


def create_app(): 
    app = rx.App(
        theme = settings.theme,
        stylesheets=[
            "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
        ],
    )

    # Attach custom API routes to Reflex's internal Starlette app.
    register_health_routes(app._api)


    # Register pages
    app.add_page(landing_page, route="/", title="Landing")
    app.add_page(dashboard_page, route="/dashboard", title="Dashboard")
    app.add_page(admin_page, route="/admin", title="Admin")
    app.add_page(settings_page, route="/settings", title="Settings")

    return app  

# Main entry point
app = create_app()

if __name__ == "__main__":
    app.compile()