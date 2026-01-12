"""Admin dashboard page."""

import reflex as rx

from app.components.shared import header, sidebar
from app.states.base import BaseState


def admin_page() -> rx.Component:
    """Admin dashboard page."""
    return rx.box(
        sidebar(current_page="admin"),
        rx.box(
            header("Admin"),
            # Main content
            rx.box(
                rx.flex(
                    # Admin header card
                    rx.box(
                        rx.flex(
                            rx.box(
                                rx.icon("shield", size=24, class_name="text-purple-600"),
                                class_name="w-8 h-8 rounded bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center",
                            ),
                            rx.box(
                                rx.heading("Admin Dashboard", size="5", class_name="text-gray-900 dark:text-white"),
                                rx.text(
                                    "Manage users, teams, and system settings.",
                                    class_name="text-gray-500 dark:text-gray-400 mt-[2px] px-1",
                                ),
                                class_name="ml-2",
                            ),
                            gap="4",
                            align="start",
                        ),
                        class_name="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 px-6 py-5",
                    ),
                    # Quick links grid
                    rx.box(
                        rx.grid(
                            _admin_card("Users", "Manage user accounts", "users", "/admin/users"),
                            _admin_card("Teams", "Manage teams and permissions", "users-round", "/admin/teams"),
                            _admin_card("System", "System configuration", "settings-2", "/admin/system"),
                            columns="3",
                            gap="2",
                            width="100%",
                            style={"row-gap": "8px", "column-gap": "8px"},
                        ),
                        class_name="mt-3",
                        style={
                            "display": "flex",
                            "flex-wrap": "wrap",
                        },
                    ),
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


def _admin_card(title: str, description: str, icon_name: str, href: str) -> rx.Component:
    """Admin quick link card."""
    return rx.link(
        rx.box(
            rx.flex(
                rx.box(
                    rx.icon(icon_name, size=20, class_name="light:text-gray-600 dark:text-gray-400"),
                    class_name="w-10 h-10 rounded-md bg-gray-100 dark:bg-gray-800 flex items-center justify-center",
                ),
                rx.box(
                    rx.text(title, class_name="text-md font-semibold light:text-gray-900 dark:text-white"),
                    rx.text(description, class_name="text-sm light:text-gray-500 dark:text-gray-400 mt-1"),
                ),
                direction="column",
                gap="2",
            ),
            class_name="light:bg-white dark:bg-gray-800 rounded-md border border-gray-200 dark:border-gray-700 px-4 py-5 hover:border-[var(--accent-3)] dark:hover:border-[var(--accent-7)] hover:shadow-md transition-all cursor-pointer",
            style={"line-height": "14px"},
        ),
        href=href,
        class_name="no-underline hover:no-underline",
    )
