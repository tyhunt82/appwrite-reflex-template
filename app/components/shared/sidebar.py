"""Collapsible sidebar navigation component."""

import reflex as rx

from app.states.base import BaseState


def nav_item(name: str, icon_name: str, href: str, is_active: bool = False) -> rx.Component:
    """Navigation item with icon and label."""
    return rx.link(
        rx.flex(
            # Sidebar Link - Icon (wrapped to normalize alignment across glyphs)
            rx.box(
                rx.icon(
                    icon_name,
                    size=20,
                    class_name=rx.cond(
                        is_active,
                        "text-[var(--accent-11)]",
                        "text-gray-500 dark:text-gray-400",
                    ),
                ),
                class_name="w-8 h-8 flex items-center justify-center",
            ),

            # Sidebar Link - Label
            rx.box(
                rx.text(
                    name,
                    class_name=rx.cond(
                        is_active,
                        "text-sm font-medium leading-none text-[var(--accent-11)]",
                        "text-sm leading-none text-gray-500 dark:text-gray-300",
                    ),
                ),
                # Sidebar Link - Label - Collapsed state
                class_name=rx.cond(
                    BaseState.sidebar_collapsed,
                    "max-w-0 opacity-0 -translate-x-1 overflow-hidden whitespace-nowrap transition-all duration-300 ease-in-out",
                    "max-w-[160px] opacity-100 translate-x-0 overflow-hidden whitespace-nowrap transition-all duration-300 ease-in-out",
                ),
            ),
            align="center",
            gap=rx.cond(BaseState.sidebar_collapsed, "0", "3"),
            class_name=rx.cond(BaseState.sidebar_collapsed, "justify-center", "justify-start"),
        ),
        href=href,

        # Sidebar Link - Active state hover effect
        class_name=rx.cond(
            is_active,
            "block px-2 py-1.5 bg-[var(--accent-3)] no-underline hover:no-underline",
            "block px-2 py-1.5 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors no-underline hover:no-underline",
        ),
    )


def sidebar_section(title: str, children: list[rx.Component]) -> rx.Component:
    """Sidebar section with optional title."""
    return rx.box(
        # Title
        rx.box(
            rx.text(
                title,
                class_name="text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-1 pl-5 pr-3",
            ),
            class_name=rx.cond(
                BaseState.sidebar_collapsed,
                "max-h-0 opacity-0 overflow-hidden transition-all duration-300 ease-in-out",
                "max-h-8 opacity-100 overflow-hidden transition-all duration-300 ease-in-out",
            ),
        ),
        # Children
        rx.flex(
            *children,
            direction="column",
            gap="1",
        ),
        class_name="mb-1 mt-3",
    )


def sidebar_logo() -> rx.Component:
    """Sidebar logo/brand."""
    return rx.box(
        rx.flex(
            # Header Icon
            rx.box(
                rx.icon("layers", size=16, class_name="light:text-gray-900 dark:text-gray-400"),
                class_name="w-8 h-8 rounded-md flex items-center justify-center",
            ),
            # Header Label
            rx.box(
                rx.text(
                    "Reflex App",
                    class_name="text-lg pl-2 font-bold leading-none light:text-gray-900 dark:text-white",
                ),
                class_name=rx.cond(
                    BaseState.sidebar_collapsed,
                    "max-w-0 opacity-0 -translate-x-1 overflow-hidden whitespace-nowrap transition-all duration-300 ease-in-out",
                    "max-w-[250px] opacity-100 translate-x-0 overflow-hidden whitespace-nowrap transition-all duration-300 ease-in-out",
                ),
            ),
            align="center",
            gap=rx.cond(BaseState.sidebar_collapsed, "0", "3"),
            class_name=rx.cond(
                BaseState.sidebar_collapsed,
                "w-full justify-center",
                "w-full justify-start",
            ),
        ),
        class_name=rx.cond(
            BaseState.sidebar_collapsed,
            "h-14 px-0 flex items-center border-b light:border-gray-200 dark:border-black-900",
            "h-14 px-4 flex items-center border-b light:border-gray-200 dark:border-black-900",
        ),
    )


def sidebar(current_page: str = "dashboard") -> rx.Component:
    """Collapsible sidebar navigation."""
    return rx.box(
        rx.flex(
            # Logo
            sidebar_logo(),

            # Main navigation
            sidebar_section(
                "Main",
                [
                    nav_item("Dashboard", "layout-dashboard", "/", current_page == "dashboard"),
                    nav_item("Admin", "shield", "/admin", current_page == "admin"),
                ],
            ),

            # Settings section
            sidebar_section(
                "System",
                [
                    nav_item("Settings", "settings", "/settings", current_page == "settings"),
                ],
            ),

            direction="column",
            class_name="h-full text-sm",
        ),
        class_name=rx.cond(
            BaseState.sidebar_collapsed,
            "fixed left-0 top-0 h-screen w-16 light:bg-white/80 dark:bg-gray-900/80 border-r light:border-gray-200 dark:border-black-900 transition-all duration-300 ease-in-out z-20",
            "fixed left-0 top-0 h-screen w-64 light:bg-white/80 dark:bg-gray-900/80 border-r light:border-gray-200 dark:border-black-900 transition-all duration-300 ease-in-out z-20",
        ),
    )
