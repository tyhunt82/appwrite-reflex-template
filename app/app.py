import reflex as rx
from app.components.sidebar import sidebar
from app.components.dashboard_views import dashboard_grid
from app.components.expenses_view import expenses_view
from app.components.categories_view import categories_view
from app.components.reports_view import reports_view
from app.components.settings_view import settings_view
from app.states.dashboard_state import DashboardState
from app.components.theme_toggle import theme_toggle

def dashboard_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Dashboard", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Welcome back, John! Here's what's happening today.",
                class_name="text-sm text-gray-500 mt-1",
            ),
        ),
        rx.el.div(
            theme_toggle(),
            rx.el.button(
                rx.icon("bell", size=20),
                rx.el.span(
                    class_name="absolute top-2.5 right-2.5 w-2 h-2 bg-red-500 rounded-full ring-2 ring-white"
                ),
                class_name="relative p-2.5 bg-white text-gray-600 rounded-xl border border-gray-200 hover:bg-gray-50 transition-colors shadow-sm",
            ),
            rx.el.button(
                rx.icon("plus", size=20, class_name="mr-2"),
                "Add Expense",
                on_click=DashboardState.set_is_add_open(True),
                class_name="flex items-center px-4 py-2.5 bg-teal-600 text-white text-sm font-semibold rounded-xl hover:bg-teal-700 transition-all shadow-sm hover:shadow-md",
            ),
            class_name="flex items-center gap-3",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                dashboard_header(),
                rx.match(
                    DashboardState.current_page,
                    ("Dashboard", dashboard_grid()),
                    ("Expenses", expenses_view()),
                    ("Categories", categories_view()),
                    ("Reports", reports_view()),
                    ("Settings", settings_view()),
                    rx.el.div(
                        rx.el.h2(
                            f"{DashboardState.current_page} - Coming Soon",
                            class_name="text-2xl font-bold text-gray-400",
                        ),
                        class_name="flex items-center justify-center h-64 bg-white rounded-2xl border border-dashed border-gray-300",
                    ),
                ),
                class_name="flex-1 p-6 lg:p-10 overflow-y-auto",
            ),
            class_name="flex-1 bg-gray-50/50 h-screen overflow-hidden flex flex-col",
        ),
        class_name="flex h-screen w-full bg-gray-50 font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="inherit"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
)
app.add_page(index, route="/", on_load=DashboardState.ensure_data)