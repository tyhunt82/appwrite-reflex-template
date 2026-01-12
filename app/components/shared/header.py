"""Page header component."""

import reflex as rx

from app.components.shared.theme_toggle import theme_toggle
from app.states.base import BaseState


def header(title: str = "Dashboard") -> rx.Component:
    """Page header with title, sidebar toggle, and theme toggle."""
    return rx.box(
        rx.flex(
            rx.flex(
                # Header - Left side - Sidebar toggle
                rx.button(
                    rx.icon(
                        rx.cond(
                            BaseState.sidebar_collapsed,
                            "panel-left-open",
                            "panel-left-close",
                        ),
                        size=20,
                        class_name="overflow-visible",
                    ),
                    on_click=BaseState.toggle_sidebar,
                    variant="ghost",
                    class_name="pl-2 light:text-gray-600 dark:text-gray-400 light:hover:bg-gray-100 dark:hover:bg-gray-800",
                ),
                
                # Header - Left side - Title Text
                rx.heading(
                    title,
                    size="6",
                    class_name="light:text-gray-900 dark:text-white font-semibold px-2",
                ),
                align="center",
                gap="3",
            ),
            
            # Header - Right side - Theme toggle
            rx.flex(
                theme_toggle(),
                align="center",
                gap="3",
            ),
            justify="between",
            align="center",
            width="100%",
            height="100%",
        ),
        class_name="sticky top-0 z-10 h-14 pr-3 light:bg-white/80 dark:bg-gray-200 backdrop-blur-sm border-b light:border-gray-200 dark:border-black-900 px-2",
    )
