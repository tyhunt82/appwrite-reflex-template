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
        class_name="rounded-md",
    )
