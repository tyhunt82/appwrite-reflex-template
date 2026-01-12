"""Theme toggle component for dark/light/system mode."""

import reflex as rx


def theme_toggle() -> rx.Component:
    """Theme toggle button for dark/light mode."""
    return rx.button(
        rx.icon(
            rx.cond(
                rx.color_mode == "light",
                "moon",
                "sun",
            ),
            size=18,
        ),
        on_click=rx.toggle_color_mode,
        variant="ghost",
        class_name="text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg",
    )
