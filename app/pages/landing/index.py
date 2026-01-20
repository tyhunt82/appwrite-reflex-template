"""Landing page."""

import reflex as rx

from app.components.landing import header


def landing_page() -> rx.Component:
    """Main landing page."""
    return rx.box(
        rx.box(
            # Header
            header(),

            # Main content
            rx.box(
                rx.flex(
                    # Hero section card
                    rx.box(
                      
                    ),
               
                ),
                class_name="p-1 m-1",
            ),
        ),
        class_name="min-h-screen",
        style={"font-size": "14px", "overflow": "hidden"},
    )

