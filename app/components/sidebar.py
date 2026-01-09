import reflex as rx
from app.states.dashboard_state import DashboardState


def nav_item(name: str, icon_name: str) -> rx.Component:
    """A single navigation item in the sidebar."""
    is_active = DashboardState.current_page == name
    return rx.el.button(
        rx.icon(
            icon_name,
            class_name=rx.cond(
                is_active, "text-teal-600", "text-gray-400 group-hover:text-teal-500"
            ),
            size=20,
        ),
        rx.el.span(
            name,
            class_name=rx.cond(
                is_active,
                "font-semibold text-gray-900",
                "font-medium text-gray-500 group-hover:text-gray-900",
            ),
        ),
        on_click=lambda: DashboardState.set_page(name),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-4 py-3 rounded-xl bg-teal-50 border border-teal-100 transition-all duration-200 w-full text-left relative overflow-hidden",
            "flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-gray-50 transition-all duration-200 w-full text-left group",
        ),
    )


def user_profile() -> rx.Component:
    return rx.el.div(
        rx.image(
            src=DashboardState.user_avatar,
            class_name="w-10 h-10 rounded-full border border-gray-200 bg-gray-100",
        ),
        rx.el.div(
            rx.el.p(
                DashboardState.user_profile["name"],
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.p("Admin Workspace", class_name="text-xs text-gray-500"),
            class_name="flex flex-col",
        ),
        rx.icon("chevron-up", class_name="ml-auto text-gray-400", size=16),
        class_name="mt-auto flex items-center gap-3 p-4 rounded-xl border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all duration-200 cursor-pointer bg-white",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("wallet", class_name="text-white", size=24),
                class_name="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-emerald-600 flex items-center justify-center shadow-lg shadow-teal-500/20",
            ),
            rx.el.span(
                "FinTrack", class_name="text-xl font-bold text-gray-900 tracking-tight"
            ),
            class_name="flex items-center gap-3 px-4 py-6 mb-6",
        ),
        rx.el.nav(
            rx.el.div(
                rx.el.p(
                    "MAIN MENU",
                    class_name="text-xs font-bold text-gray-400 px-4 mb-4 tracking-wider",
                ),
                rx.el.div(
                    nav_item("Dashboard", "layout-dashboard"),
                    nav_item("Expenses", "receipt"),
                    nav_item("Categories", "pie-chart"),
                    nav_item("Reports", "bar-chart-3"),
                    class_name="flex flex-col gap-1 px-2",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "PREFERENCES",
                        class_name="text-xs font-bold text-gray-400 px-4 mb-4 tracking-wider",
                    ),
                    rx.el.div(
                        nav_item("Settings", "settings-2"),
                        class_name="flex flex-col gap-1 px-2 mb-6",
                    ),
                ),
                user_profile(),
                class_name="px-2 pb-6",
            ),
            class_name="flex flex-col h-full overflow-y-auto",
        ),
        class_name="hidden lg:flex flex-col w-72 h-screen border-r border-gray-100 bg-white sticky top-0 shrink-0 z-20",
    )