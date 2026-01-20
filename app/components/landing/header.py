"""Page header component."""

import reflex as rx

from app.components.shared.theme_toggle import theme_toggle
from app.states.base import BaseState


def header(title: str = "App Title") -> rx.Component:
    """Landing page header with title, and theme toggle."""
    return rx.box(
        rx.flex(
            rx.flex(
                
                # Header - Left side - Title Text
                rx.heading(
                    title,
                    size="6",
                    class_name="font-semibold px-2",
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
        class_name="sticky top-0 z-10 h-14 pr-3 backdrop-blur-sm border-b dark:border-gray-900 px-2",
    )
