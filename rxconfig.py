import reflex as rx
from reflex.plugins import sitemap
from app.config import settings

config = rx.Config(
    app_name="app",
    theme= settings.theme,
    frontend_packages=["react-icons"],
    frontend_port=3000,
    backend_port=8000,

    cors_allowed_origins=[
        "http://localhost:3000",
         "http://localhost:8000"
    ],

    plugins=[
        rx.plugins.TailwindV3Plugin(),
        sitemap.SitemapPlugin(),
    ],

    analytics_enabled=True,
    logging_enabled=True,
    error_handling_enabled=True,
)
