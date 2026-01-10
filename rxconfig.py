import reflex as rx
from reflex.plugins import sitemap

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        sitemap.SitemapPlugin(),
    ],
)
