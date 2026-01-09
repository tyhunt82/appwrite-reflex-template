import reflex as rx
from app.states.dashboard_state import DashboardState


def report_stat_card(label: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
        ),
        rx.el.div(
            rx.icon(icon, size=24, class_name=f"text-{color}-600"),
            class_name=f"w-12 h-12 rounded-xl bg-{color}-50 flex items-center justify-center",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center justify-between",
    )


def spending_breakdown_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Category Breakdown", class_name="text-lg font-bold text-gray-900 mb-6"
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=DashboardState.report_pie_data,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    inner_radius=60,
                    outer_radius=80,
                    label=True,
                    stroke="#ffffff",
                    stroke_width=2,
                ),
                rx.recharts.tooltip(),
                height=300,
                width="100%",
            ),
            class_name="h-72 w-full flex items-center justify-center",
        ),
        rx.el.div(
            rx.foreach(
                DashboardState.report_pie_data,
                lambda item: rx.el.div(
                    rx.el.div(
                        class_name="w-3 h-3 rounded-full",
                        style={"backgroundColor": item["fill"]},
                    ),
                    rx.el.span(
                        item["name"], class_name="text-sm text-gray-600 font-medium"
                    ),
                    class_name="flex items-center gap-2",
                ),
            ),
            class_name="flex flex-wrap justify-center gap-x-6 gap-y-2 mt-4",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def spending_trend_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Spending Trend", class_name="text-lg font-bold text-gray-900 mb-6"),
        rx.el.div(
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", vertical=False, stroke="#e5e7eb"
                ),
                rx.el.defs(
                    rx.el.linear_gradient(
                        rx.el.stop(offset="5%", stop_color="#3b82f6", stop_opacity=0.8),
                        rx.el.stop(offset="95%", stop_color="#3b82f6", stop_opacity=0),
                        id="colorBlue",
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
                    }
                ),
                rx.recharts.area(
                    type_="monotone",
                    data_key="amount",
                    stroke="#3b82f6",
                    stroke_width=3,
                    fill_opacity=1,
                    fill="url(#colorBlue)",
                ),
                data=DashboardState.report_trend_data,
                width="100%",
                height="100%",
            ),
            class_name="h-72 w-full",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def insights_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3("AI Insights", class_name="text-lg font-bold text-gray-900 mb-4"),
        rx.el.div(
            rx.el.div(
                rx.icon("trending-up", size=20, class_name="text-amber-600 mt-1"),
                rx.el.div(
                    rx.el.p(
                        "Spending Alert", class_name="text-sm font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "Your 'Travel' spending is 20% higher than last month.",
                        class_name="text-sm text-gray-600",
                    ),
                ),
                class_name="flex gap-3 p-4 bg-amber-50 rounded-xl border border-amber-100",
            ),
            rx.el.div(
                rx.icon(
                    "circle_check_big", size=20, class_name="text-emerald-600 mt-1"
                ),
                rx.el.div(
                    rx.el.p(
                        "Budget on Track", class_name="text-sm font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "You are well within your 'Office' budget for this period.",
                        class_name="text-sm text-gray-600",
                    ),
                ),
                class_name="flex gap-3 p-4 bg-emerald-50 rounded-xl border border-emerald-100",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
        ),
        class_name="mt-8",
    )


def reports_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Reports", class_name="text-xl font-bold text-gray-900"),
                rx.el.p(
                    "Analyze your financial performance.",
                    class_name="text-sm text-gray-500",
                ),
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("This Week"),
                    rx.el.option("This Month"),
                    rx.el.option("Last Month"),
                    rx.el.option("This Year"),
                    value=DashboardState.report_range,
                    on_change=DashboardState.set_report_range,
                    class_name="px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 outline-none appearance-none",
                ),
                rx.el.button(
                    rx.icon("download", size=18, class_name="mr-2"),
                    "Export CSV",
                    on_click=DashboardState.export_report,
                    class_name="flex items-center px-4 py-2 bg-gray-900 text-white text-sm font-semibold rounded-xl hover:bg-gray-800 shadow-sm transition-all",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between mb-8",
        ),
        rx.el.div(
            report_stat_card(
                "Total Spent", f"${DashboardState.report_total}", "dollar-sign", "blue"
            ),
            report_stat_card(
                "Transactions",
                DashboardState.report_expenses.length().to_string(),
                "receipt",
                "purple",
            ),
            report_stat_card(
                "Categories Active",
                DashboardState.report_pie_data.length().to_string(),
                "pie-chart",
                "green",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            spending_trend_chart(),
            spending_breakdown_chart(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        insights_section(),
        class_name="w-full max-w-7xl mx-auto pb-10",
    )