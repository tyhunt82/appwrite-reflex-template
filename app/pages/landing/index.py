"""Dashboard page."""

import reflex as rx

from app.components.shared import header, sidebar
from app.states.base import BaseState


def landing_page() -> rx.Component:
    """Main dashboard page."""
    return rx.box(
        sidebar(current_page="landing"),
        rx.box(
            header("Landing"),
            # Main content
            rx.box(
                rx.flex(
                    # Hero section card
                    rx.box(
                        rx.flex(
                            rx.box(
                                rx.icon("home", size=24, class_name="text-[var(--accent-11)]"),
                                class_name="w-8 h-8 rounded bg-[var(--accent-3)] flex items-center justify-center",
                            ),
                            rx.box(
                                rx.heading("Welcome back!", size="5", class_name="text-gray-900 dark:text-white ml-1"),
                                rx.text(
                                    "This is your landing page. Start building something amazing.",
                                    class_name="text-gray-500 dark:text-gray-400 mt-[2px] px-1",
                                ),
                                class_name="ml-2",
                            ),
                            gap="4",
                            align="start",
                        ),
                        class_name="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 px-6 py-5",
                    ),
                    # Stats section grid
                   
                    direction="column",
                    width="100%",
                    gap="2",
                    style={
                        "font-size": "14px",
                        "border-width": "0.5px",
                        "border-color": "rgba(0, 0, 0, 0)",
                        "border-image": "none",
                        "margin-left": "0px",
                        "margin-right": "0px",
                    },
                ),
                class_name="p-1 m-1",
            ),
            class_name=rx.cond(
                BaseState.sidebar_collapsed,
                "ml-16 transition-all duration-300 ease-in-out",
                "ml-64 transition-all duration-300 ease-in-out",
            ),
        ),
        class_name="min-h-screen bg-white dark:bg-gray-950",
        style={"font-size": "14px", "overflow": "hidden"},
    )


def _stat_card(title: str, value: str, icon_name: str, change: str) -> rx.Component:
    """Stat card component."""
    is_positive = change.startswith("+")
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon(icon_name, size=20, class_name="text-gray-600 dark:text-gray-400"),
                class_name="w-10 h-10 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center",
            ),
            rx.box(
                rx.text(title, class_name="text-sm text-gray-500 dark:text-gray-400"),
                rx.flex(
                    rx.text(value, class_name="text-xl font-semibold text-gray-900 dark:text-white"),
                    rx.text(
                        change,
                        class_name=f"text-sm {'text-emerald-600' if is_positive else 'text-red-500'} ml-2",
                    ),
                    align="baseline",
                    class_name="mt-1",
                ),
            ),
            direction="column",
            gap="3",
        ),
        class_name="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 px-4 py-5",
        style={"line-height": "14px"},
    )
