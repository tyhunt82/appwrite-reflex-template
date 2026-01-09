import reflex as rx
from app.states.dashboard_state import DashboardState


def section_header(title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-gray-900"),
        rx.el.p(description, class_name="text-sm text-gray-500"),
        class_name="mb-6",
    )


def profile_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "Profile Information", "Update your account details and profile."
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Full Name",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="name",
                        default_value=DashboardState.user_profile["name"],
                        class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Email Address",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="email",
                        type="email",
                        default_value=DashboardState.user_profile["email"],
                        class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
            ),
            rx.el.div(
                rx.el.button(
                    "Save Profile",
                    type="submit",
                    class_name="px-4 py-2 bg-teal-600 text-white text-sm font-semibold rounded-xl hover:bg-teal-700 shadow-sm transition-all",
                ),
                class_name="flex justify-end",
            ),
            on_submit=DashboardState.update_profile,
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def toggle_item(
    label: str, description: str, checked: bool, on_change: callable
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-900"),
            rx.el.p(description, class_name="text-xs text-gray-500"),
        ),
        rx.switch(checked=checked, on_change=on_change, color_scheme="teal"),
        class_name="flex items-center justify-between py-4 border-b border-gray-50 last:border-0",
    )


def notifications_section() -> rx.Component:
    return rx.el.div(
        section_header("Notifications", "Manage how you receive alerts and reports."),
        rx.el.div(
            toggle_item(
                "Email Alerts",
                "Receive emails about unusual spending activity.",
                DashboardState.notifications["email_alerts"],
                lambda v: DashboardState.toggle_notification("email_alerts", v),
            ),
            toggle_item(
                "Expense Reminders",
                "Get reminded to log expenses every Friday.",
                DashboardState.notifications["expense_reminders"],
                lambda v: DashboardState.toggle_notification("expense_reminders", v),
            ),
            toggle_item(
                "Monthly Reports",
                "Receive a monthly summary of your financial status.",
                DashboardState.notifications["monthly_reports"],
                lambda v: DashboardState.toggle_notification("monthly_reports", v),
            ),
            class_name="flex flex-col",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def budget_settings_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "Budget Settings", "Configure global budget parameters and limits."
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Default Category Budget ($)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="default_limit",
                        type="number",
                        default_value=DashboardState.budget_settings[
                            "default_limit"
                        ].to_string(),
                        class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Warning Threshold (%)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.div(
                        rx.el.input(
                            name="warning_threshold",
                            type="number",
                            max="100",
                            min="1",
                            default_value=DashboardState.budget_settings[
                                "warning_threshold"
                            ].to_string(),
                            class_name="w-full pl-4 pr-12 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm",
                        ),
                        rx.el.span(
                            "%",
                            class_name="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 text-sm",
                        ),
                        class_name="relative",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
            ),
            rx.el.div(
                rx.el.button(
                    "Update Settings",
                    type="submit",
                    class_name="px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-xl hover:bg-gray-800 shadow-sm transition-all",
                ),
                class_name="flex justify-end",
            ),
            on_submit=DashboardState.update_budget_settings,
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def display_section() -> rx.Component:
    return rx.el.div(
        section_header("Display", "Customize your dashboard experience."),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Currency Format",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.el.option("USD ($)", value="USD ($)"),
                    rx.el.option("EUR (€)", value="EUR (€)"),
                    rx.el.option("GBP (£)", value="GBP (£)"),
                    rx.el.option("JPY (¥)", value="JPY (¥)"),
                    value=DashboardState.currency,
                    on_change=DashboardState.set_currency,
                    class_name="w-full md:w-64 px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm bg-white appearance-none",
                ),
            ),
            class_name="flex flex-col",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def clear_data_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.icon("trending_down", class_name="text-red-500 mb-4", size=48),
                rx.el.h2(
                    "Clear All Data?", class_name="text-xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Are you sure you want to delete all expenses? This action is irreversible and cannot be undone.",
                    class_name="text-center text-sm text-gray-500 mb-8",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            class_name="px-4 py-2 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 border border-gray-200 transition-colors w-full",
                        )
                    ),
                    rx.el.button(
                        "Yes, Clear All",
                        on_click=DashboardState.clear_all_data,
                        class_name="px-4 py-2 rounded-xl text-sm font-medium text-white bg-red-600 hover:bg-red-700 shadow-sm shadow-red-600/20 transition-all w-full",
                    ),
                    class_name="flex items-center gap-3 w-full",
                ),
                class_name="flex flex-col items-center",
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-sm w-full outline-none",
        ),
        open=DashboardState.is_clear_data_open,
        on_open_change=DashboardState.set_is_clear_data_open,
    )


def data_management_section() -> rx.Component:
    return rx.el.div(
        section_header("Data Management", "Export or reset your account data."),
        rx.el.div(
            rx.el.div(
                rx.el.h4("Export Data", class_name="text-sm font-bold text-gray-900"),
                rx.el.p(
                    "Download a CSV file of all your expenses and categories.",
                    class_name="text-xs text-gray-500 mb-3",
                ),
                rx.el.button(
                    rx.icon("download", size=16, class_name="mr-2"),
                    "Export All Data",
                    on_click=DashboardState.export_report,
                    class_name="flex items-center px-4 py-2 border border-gray-200 text-gray-700 text-sm font-medium rounded-xl hover:bg-gray-50 transition-all",
                ),
                class_name="pb-6 border-b border-gray-100",
            ),
            rx.el.div(
                rx.el.h4(
                    "Danger Zone", class_name="text-sm font-bold text-red-600 mt-6"
                ),
                rx.el.p(
                    "Irreversibly clear all your expense data.",
                    class_name="text-xs text-gray-500 mb-3",
                ),
                rx.el.button(
                    rx.icon("trash-2", size=16, class_name="mr-2"),
                    "Clear All Expenses",
                    on_click=DashboardState.set_is_clear_data_open(True),
                    class_name="flex items-center px-4 py-2 border border-red-200 text-red-600 bg-red-50 text-sm font-medium rounded-xl hover:bg-red-100 transition-all",
                ),
            ),
            class_name="flex flex-col",
        ),
        clear_data_dialog(),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def settings_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Settings", class_name="text-xl font-bold text-gray-900"),
            rx.el.p(
                "Manage your preferences and account settings.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            profile_section(),
            notifications_section(),
            budget_settings_section(),
            display_section(),
            data_management_section(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        class_name="w-full max-w-full mx-auto pb-10",
    )