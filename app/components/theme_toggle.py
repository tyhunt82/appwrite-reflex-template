import reflex as rx
from reflex.style import set_color_mode, color_mode


def theme_toggle() -> rx.Component:
    """Toggle between light, dark, and system mode."""
    default_theme = "dark"
    default_accent_color = "teal"
    default_base_color = "gray"
    default_size = 16

    return rx.segmented_control.root(
        rx.segmented_control.item(
            rx.icon(tag="monitor", size=default_size),
            value="system",
        ),
        rx.segmented_control.item(
            rx.icon(tag="sun", size=default_size),
            value="light",
        ),
        rx.segmented_control.item(
            rx.icon(tag="moon", size=default_size),
            value="dark",
        ),
        on_change=set_color_mode,
        variant="classic",
        radius="small",
        value=color_mode,
    )