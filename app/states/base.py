"""Base state shared across all pages."""

import reflex as rx

from app.config import settings


class BaseState(rx.State):
    """Base state with shared functionality."""

    # Sidebar
    sidebar_collapsed: bool = settings.sidebar_default_collapsed

    # Theme managed by Reflex's color_mode

    @rx.event
    def toggle_sidebar(self):
        """Toggle sidebar collapsed state."""
        self.sidebar_collapsed = not self.sidebar_collapsed

    @rx.event
    def set_sidebar_collapsed(self, collapsed: bool):
        """Set sidebar collapsed state explicitly."""
        self.sidebar_collapsed = collapsed
