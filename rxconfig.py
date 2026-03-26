import reflex as rx
from reflex.plugins.sitemap import SitemapPlugin

config = rx.Config(
    app_name='projects',
    api_url='http://localhost:9001',
    frontend_port=9000,
    backend_port=9001,
    disable_plugins=[SitemapPlugin],
)
