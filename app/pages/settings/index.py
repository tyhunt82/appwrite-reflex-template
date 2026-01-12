"""Settings page."""

import reflex as rx

from app.components.shared import header, sidebar
from app.pages.settings.state import SettingsState
from app.states.base import BaseState


def settings_page() -> rx.Component:
    """Settings page."""
    return rx.box(
        sidebar(current_page="settings"),
        rx.box(
            header("Settings"),
            # Main content
            rx.box(
                rx.flex(
                    # Profile section
                    _settings_section(
                        "Profile",
                        "Manage your account information",
                        "user",
                        _profile_form(),
                        width_class="w-full",
                    ),
                    # Notifications section
                    _settings_section(
                        "Notifications",
                        "Configure how you receive updates",
                        "bell",
                        _notifications_form(),
                        width_class="w-full",
                    ),
                    # Appearance section
                    _settings_section(
                        "Appearance",
                        "Customize the look and feel",
                        "palette",
                        _appearance_settings(),
                        width_class="w-full lg:w-[calc(50%-4px)]",
                    ),
                    direction="row",
                    width="100%",
                    max_width="1100px",
                    style={
                        "font-size": "14px",
                        "border-width": "0.5px",
                        "border-color": "rgba(0, 0, 0, 0)",
                        "flex-wrap": "wrap",
                        "gap": "8px",
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


def _settings_section(
    title: str,
    description: str,
    icon_name: str,
    content: rx.Component,
    *,
    width_class: str = "w-full",
) -> rx.Component:
    """Settings section card."""
    return rx.box(
        rx.flex(
            rx.flex(
                rx.box(
                    rx.icon(icon_name, size=20, class_name="text-gray-600 dark:text-gray-400"),
                    class_name="w-10 h-10 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center",
                ),
                rx.box(
                    rx.text(title, class_name="pl-2 font-semibold text-gray-900 dark:text-white"),
                    rx.text(description, class_name="pl-2 text-sm text-gray-500 dark:text-gray-400"),
                ),
                gap="3",
                align="center",
            ),
            rx.box(
                content,
                class_name="mt-3",
            ),
            direction="column",
        ),
        class_name=f"bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 px-6 py-5 {width_class}",
        style={"line-height": "14px"},
    )


def _profile_form() -> rx.Component:
    """Profile settings form."""
    return rx.form(
        rx.flex(
            rx.box(
                rx.text("Name", class_name="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"),
                rx.input(
                    name="name",
                    default_value=SettingsState.profile_name,
                    placeholder="Your name",
                    class_name="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white",
                ),
                class_name="flex-1 min-w-[220px]",
            ),
            rx.box(
                rx.text("Email", class_name="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"),
                rx.input(
                    name="email",
                    type="email",
                    default_value=SettingsState.profile_email,
                    placeholder="your@email.com",
                    class_name="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white",
                ),
                class_name="flex-1 min-w-[220px]",
            ),
            gap="4",
            direction="row",
            width="100%",
            style={"flex-wrap": "wrap"},
        ),
        rx.button(
            "Save Changes",
            type="submit",
            class_name="mt-4 px-4 py-2 bg-[var(--accent-9)] hover:bg-[var(--accent-10)] text-[var(--accent-contrast)] rounded-lg font-medium",
        ),
        on_submit=SettingsState.update_profile,
        reset_on_submit=False,
    )


def _notifications_form() -> rx.Component:
    """Notifications settings form."""
    return rx.flex(
        _toggle_setting(
            "Email Alerts",
            "Receive email notifications for important updates",
            SettingsState.email_alerts,
            SettingsState.toggle_email_alerts,
        ),
        _toggle_setting(
            "Push Notifications",
            "Receive push notifications on your devices",
            SettingsState.push_notifications,
            SettingsState.toggle_push_notifications,
        ),
        _toggle_setting(
            "Weekly Digest",
            "Receive a weekly summary of activity",
            SettingsState.weekly_digest,
            SettingsState.toggle_weekly_digest,
        ),
        direction="column",
        gap="4",
    )


def _toggle_setting( 
    title: str, description: str, checked: rx.Var[bool], on_change: rx.EventHandler
 ) -> rx.Component:
    """Toggle setting row."""
    return rx.flex(
        rx.box(
            rx.text(title, class_name="font-medium text-gray-900 dark:text-white"),
            rx.text(description, class_name="text-sm text-gray-500 dark:text-gray-400"),
        ),
        rx.switch(
            checked=checked,
            on_change=on_change,
        ),
        justify="between",
        align="center",
        width="100%",
    )


def _appearance_settings() -> rx.Component:
    """Appearance settings."""
    return rx.flex(
        rx.flex(
            rx.box(
                rx.text("Theme", class_name="font-medium text-gray-900 dark:text-white"),
                rx.text("Toggle between light and dark mode", class_name="text-sm text-gray-500 dark:text-gray-400"),
            ),
            rx.button(
                rx.icon(
                    rx.cond(rx.color_mode == "light", "moon", "sun"),
                    size=18,
                ),
                rx.text(rx.cond(rx.color_mode == "light", "Dark", "Light")),
                on_click=rx.toggle_color_mode,
                variant="outline",
                class_name="gap-2",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        _toggle_setting(
            "Compact Sidebar",
            "Use a collapsed sidebar by default",
            BaseState.sidebar_collapsed,
            BaseState.set_sidebar_collapsed,
        ),
        rx.flex(
            rx.box(
                rx.text("Theme panel", class_name="font-medium text-gray-900 dark:text-white"),
                rx.text(
                    "Adjust accent, radius, scaling, and more",
                    class_name="text-sm text-gray-500 dark:text-gray-400",
                ),
            ),
            rx.theme_panel(),
            justify="between",
            align="center",
            width="100%",
        ),
        direction="column",
        gap="4",
    )
