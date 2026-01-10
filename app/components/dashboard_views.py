import reflex as rx
from app.states.dashboard_state import DashboardState, Expense, CategoryBudget
from app.components.expenses_view import add_expense_dialog
from app.components.shared import status_badge, category_icon


def summary_card(
    title: str, value: str, trend: str, icon: str, color_scheme: str
 )  -> rx.Component:
    """A statistical summary card."""
    colors = {
        "teal": "from-teal-500 to-emerald-500",
        "blue": "from-blue-500 to-indigo-500",
        "purple": "from-purple-500 to-fuchsia-500",
        "orange": "from-orange-500 to-red-500",
    }
    bg_gradient = colors.get(color_scheme, colors["teal"])
    is_negative = trend.startswith("-")
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="text-white", size=24),
                class_name=f"w-12 h-12 rounded-xl bg-gradient-to-br {bg_gradient} flex items-center justify-center shadow-lg opacity-90",
            ),
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    rx.cond(is_negative, "trending-down", "trending-up"),
                    size=14,
                    class_name="mr-1",
                ),
                rx.el.span(trend, class_name="font-semibold"),
                rx.el.span(
                    " vs last month", class_name="text-gray-500 font-medium ml-1"
                ),
                class_name=rx.cond(
                    is_negative,
                    "flex items-center text-xs text-red-600 bg-red-50 px-2 py-1 rounded-full w-fit",
                    "flex items-center text-xs text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full w-fit",
                ),
            ),
            class_name="mt-4",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200",
    )


def spending_chart() -> rx.Component:
    """Area chart showing spending trends."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Spending Analysis", class_name="text-lg font-bold text-gray-900"),
            rx.el.select(
                rx.el.option("Last 6 Months", value="Last 6 Months"),
                rx.el.option("This Year", value="This Year"),
                value=DashboardState.chart_range,
                on_change=DashboardState.set_chart_range,
                class_name="text-sm border-gray-200 rounded-lg focus:ring-teal-500 focus:border-teal-500 outline-none p-1 appearance-none",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", vertical=False, stroke="#e5e7eb"
                ),
                rx.el.defs(
                    rx.el.linear_gradient(
                        rx.el.stop(offset="5%", stop_color="#0d9488", stop_opacity=0.8),
                        rx.el.stop(offset="95%", stop_color="#0d9488", stop_opacity=0),
                        id="colorTeal",
                        x1="0",
                        y1="0",
                        x2="0",
                        y2="1",
                    )
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    axis_line=False,
                    tick_line=False,
                    tick={"fontSize": 12, "fill": "#6b7280"},
                    dy=10,
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    tick={"fontSize": 12, "fill": "#6b7280"},
                ),
                rx.recharts.tooltip(
                    content_style={
                        "borderRadius": "12px",
                        "border": "none",
                        "boxShadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                    },
                    cursor={"stroke": "#0d9488", "strokeWidth": 1},
                ),
                rx.recharts.area(
                    type_="monotone",
                    data_key="amount",
                    stroke="#0d9488",
                    stroke_width=3,
                    fill_opacity=1,
                    fill="url(#colorTeal)",
                ),
                data=DashboardState.chart_trend_data,
                width="100%",
                height="100%",
            ),
            class_name="h-64 w-full",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-full",
    )


def transaction_row(expense: Expense) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                category_icon(expense["category"]),
                rx.el.div(
                    rx.el.p(
                        expense["merchant"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(expense["category"], class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="py-4 pl-4 pr-3",
        ),
        rx.el.td(
            rx.el.span(expense["date"], class_name="text-sm text-gray-600 font-medium"),
            class_name="px-3 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge(expense["status"]), class_name="px-3 py-4 whitespace-nowrap"
        ),
        rx.el.td(
            rx.el.span(
                f"${expense['amount']}", class_name="text-sm font-bold text-gray-900"
            ),
            class_name="px-3 py-4 whitespace-nowrap text-right pr-4",
        ),
        class_name="hover:bg-gray-50/50 transition-colors border-b border-gray-50 last:border-0",
    )


def recent_transactions() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Recent Transactions", class_name="text-lg font-bold text-gray-900"
            ),
            rx.el.button(
                "View All",
                on_click=lambda: DashboardState.set_page("Expenses"),
                class_name="text-sm font-semibold text-teal-600 hover:text-teal-700 hover:underline",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Merchant",
                            class_name="text-left text-xs font-semibold text-gray-500 pb-3 pl-4",
                        ),
                        rx.el.th(
                            "Date",
                            class_name="text-left text-xs font-semibold text-gray-500 pb-3",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="text-left text-xs font-semibold text-gray-500 pb-3",
                        ),
                        rx.el.th(
                            "Amount",
                            class_name="text-right text-xs font-semibold text-gray-500 pb-3 pr-4",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(DashboardState.recent_expenses, transaction_row)
                ),
                class_name="w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex-1",
    )


def budget_item(category: CategoryBudget) -> rx.Component:
    percentage = category["spent"] / category["limit"] * 100
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                category["name"], class_name="text-sm font-medium text-gray-700"
            ),
            rx.el.div(
                rx.el.span(
                    f"${category['spent']}",
                    class_name="text-sm font-bold text-gray-900",
                ),
                rx.el.span(
                    f" / ${category['limit']}", class_name="text-xs text-gray-500 ml-1"
                ),
                class_name="flex items-baseline",
            ),
            class_name="flex justify-between mb-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name=f"h-full rounded-full {category['color']}",
                style={"width": f"{percentage}%"},
            ),
            class_name="w-full h-2 bg-gray-100 rounded-full overflow-hidden",
        ),
        class_name="mb-5 last:mb-0",
    )


def budget_progress() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Monthly Budget", class_name="text-lg font-bold text-gray-900"),
            rx.icon("pie-chart", size=20, class_name="text-gray-400"),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.foreach(DashboardState.category_budgets, budget_item),
        rx.el.div(
            rx.el.p(
                "Total Budget Used",
                class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 mt-6",
            ),
            rx.el.div(
                rx.el.div(
                    f"{DashboardState.budget_usage_percent}%",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.div("of monthly limit", class_name="text-sm text-gray-500 ml-2"),
                class_name="flex items-baseline",
            ),
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-full",
    )


def dashboard_grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            summary_card(
                "Total Expenses",
                f"${DashboardState.total_expenses}",
                "+12.5%",
                "wallet",
                "teal",
            ),
            summary_card(
                "This Month",
                f"${DashboardState.current_month_expenses}",
                "+5.2%",
                "calendar",
                "blue",
            ),
            summary_card(
                "Budget Status",
                f"{DashboardState.budget_usage_percent}%",
                "-2.1%",
                "target",
                "purple",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(spending_chart(), class_name="h-96 mb-6"),
                recent_transactions(),
                class_name="lg:col-span-2 flex flex-col",
            ),
            rx.el.div(
                budget_progress(),
                rx.el.div(
                    rx.el.div(
                        rx.icon("sparkles", class_name="text-amber-500 mb-3", size=24),
                        rx.el.h4(
                            "Pro Tips",
                            class_name="text-base font-bold text-gray-900 mb-1",
                        ),
                        rx.el.p(
                            "You spent 15% less on Travel this month compared to average.",
                            class_name="text-sm text-gray-600 mb-4",
                        ),
                        rx.el.button(
                            "View Insights",
                            on_click=lambda: DashboardState.set_page("Reports"),
                            class_name="w-full py-2 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-800 transition-colors",
                        ),
                    ),
                    class_name="mt-6 bg-gradient-to-br from-amber-50 to-orange-50 p-6 rounded-2xl border border-amber-100",
                ),
                class_name="lg:col-span-1 flex flex-col",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
        add_expense_dialog(),
        class_name="w-full max-w-full mx-auto",
    )