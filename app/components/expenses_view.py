import reflex as rx
from app.states.dashboard_state import DashboardState, Expense
from app.components.shared import status_badge, category_icon


def form_input(
    label: str, name: str, placeholder: str, type: str = "text", default_value: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type,
            name=name,
            placeholder=placeholder,
            default_value=default_value,
            class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm",
            required=True,
        ),
    )


def form_select(
    label: str, name: str, options: list[str], default_value: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.select(
            rx.foreach(options, lambda opt: rx.el.option(opt, value=opt)),
            name=name,
            default_value=default_value,
            class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm bg-white appearance-none",
        ),
    )


def add_expense_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.el.h2(
                    "Add New Expense", class_name="text-xl font-bold text-gray-900 mb-1"
                ),
                rx.el.p(
                    "Fill in the details for your new transaction.",
                    class_name="text-sm text-gray-500 mb-6",
                ),
                rx.el.form(
                    rx.el.div(
                        form_input("Merchant", "merchant", "e.g. Uber, Amazon"),
                        rx.el.div(
                            form_input("Amount", "amount", "0.00", "number"),
                            form_select(
                                "Category",
                                "category",
                                [
                                    "Office",
                                    "Travel",
                                    "Software",
                                    "Marketing",
                                    "Services",
                                ],
                                "Office",
                            ),
                            class_name="grid grid-cols-2 gap-4",
                        ),
                        form_input("Date", "date", "", "date"),
                        form_input("Description", "description", "What was this for?"),
                        class_name="flex flex-col gap-4 mb-8",
                    ),
                    rx.el.div(
                        rx.dialog.close(
                            rx.el.button(
                                "Cancel",
                                type="button",
                                class_name="px-4 py-2 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 border border-gray-200 transition-colors",
                            )
                        ),
                        rx.el.button(
                            "Add Expense",
                            type="submit",
                            class_name="px-4 py-2 rounded-xl text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 shadow-sm shadow-teal-600/20 transition-all",
                        ),
                        class_name="flex items-center justify-end gap-3",
                    ),
                    on_submit=DashboardState.add_expense,
                    reset_on_submit=True,
                ),
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-lg w-full outline-none",
        ),
        open=DashboardState.is_add_open,
        on_open_change=DashboardState.set_is_add_open,
    )


def edit_expense_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.el.h2(
                    "Edit Expense", class_name="text-xl font-bold text-gray-900 mb-1"
                ),
                rx.el.p(
                    "Update transaction details.",
                    class_name="text-sm text-gray-500 mb-6",
                ),
                rx.el.form(
                    rx.el.input(
                        type="hidden",
                        name="id",
                        value=DashboardState.current_expense["id"],
                    ),
                    rx.el.div(
                        form_input(
                            "Merchant",
                            "merchant",
                            "",
                            default_value=DashboardState.current_expense["merchant"],
                        ),
                        rx.el.div(
                            form_input(
                                "Amount",
                                "amount",
                                "",
                                "number",
                                default_value=DashboardState.current_expense[
                                    "amount"
                                ].to_string(),
                            ),
                            form_select(
                                "Category",
                                "category",
                                [
                                    "Office",
                                    "Travel",
                                    "Software",
                                    "Marketing",
                                    "Services",
                                ],
                                default_value=DashboardState.current_expense[
                                    "category"
                                ],
                            ),
                            class_name="grid grid-cols-2 gap-4",
                        ),
                        form_input(
                            "Date",
                            "date",
                            "",
                            "date",
                            default_value=DashboardState.current_expense["date"],
                        ),
                        form_input(
                            "Description",
                            "description",
                            "",
                            default_value=DashboardState.current_expense["description"],
                        ),
                        class_name="flex flex-col gap-4 mb-8",
                    ),
                    rx.el.div(
                        rx.dialog.close(
                            rx.el.button(
                                "Cancel",
                                type="button",
                                class_name="px-4 py-2 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 border border-gray-200 transition-colors",
                            )
                        ),
                        rx.el.button(
                            "Save Changes",
                            type="submit",
                            class_name="px-4 py-2 rounded-xl text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 shadow-sm shadow-teal-600/20 transition-all",
                        ),
                        class_name="flex items-center justify-end gap-3",
                    ),
                    on_submit=DashboardState.update_expense,
                    key=DashboardState.current_expense["id"],
                ),
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-lg w-full outline-none",
        ),
        open=DashboardState.is_edit_open,
        on_open_change=DashboardState.set_is_edit_open,
    )


def delete_confirm_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.el.div(
                    rx.icon("trending_down", class_name="text-red-500 mb-4", size=48),
                    rx.el.h2(
                        "Delete Expense?",
                        class_name="text-xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        f"Are you sure you want to delete the transaction for ",
                        rx.el.span(
                            DashboardState.current_expense["merchant"],
                            class_name="font-semibold",
                        ),
                        "? This action cannot be undone.",
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
                            "Delete",
                            on_click=DashboardState.delete_expense,
                            class_name="px-4 py-2 rounded-xl text-sm font-medium text-white bg-red-600 hover:bg-red-700 shadow-sm shadow-red-600/20 transition-all w-full",
                        ),
                        class_name="flex items-center gap-3 w-full",
                    ),
                    class_name="flex flex-col items-center",
                )
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-sm w-full outline-none",
        ),
        open=DashboardState.is_delete_open,
        on_open_change=DashboardState.set_is_delete_open,
    )


def table_header_cell(label: str, sort_key: str = "") -> rx.Component:
    return rx.el.th(
        rx.el.div(
            label,
            rx.cond(
                sort_key != "",
                rx.icon(
                    "arrow-up-down",
                    size=14,
                    class_name=rx.cond(
                        DashboardState.sort_value == sort_key,
                        "text-teal-600",
                        "text-gray-300 group-hover:text-gray-500",
                    ),
                ),
            ),
            class_name="flex items-center gap-2 cursor-pointer group select-none",
        ),
        class_name="text-left text-xs font-semibold text-gray-500 pb-4 pl-4 uppercase tracking-wider",
        on_click=lambda: rx.cond(sort_key, DashboardState.toggle_sort(sort_key), None),
    )


def expense_row(expense: Expense) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                category_icon(expense["category"]),
                rx.el.div(
                    rx.el.p(
                        expense["merchant"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        expense["description"],
                        class_name="text-xs text-gray-500 line-clamp-1",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="py-4 pl-4 pr-3",
        ),
        rx.el.td(
            rx.el.span(expense["category"], class_name="text-sm text-gray-600"),
            class_name="px-3 py-4 whitespace-nowrap",
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
            class_name="px-3 py-4 whitespace-nowrap text-right",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", size=16),
                    class_name="p-2 text-gray-400 hover:text-teal-600 hover:bg-teal-50 rounded-lg transition-colors",
                    on_click=lambda: DashboardState.open_edit_modal(expense),
                ),
                rx.el.button(
                    rx.icon("trash-2", size=16),
                    class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                    on_click=lambda: DashboardState.open_delete_modal(expense),
                ),
                class_name="flex items-center justify-end gap-1",
            ),
            class_name="px-3 py-4 pr-4 whitespace-nowrap text-right",
        ),
        class_name="hover:bg-gray-50/80 transition-colors border-b border-gray-100 last:border-0",
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            f"Page {DashboardState.page} of {DashboardState.page_count}",
            class_name="text-sm text-gray-500 font-medium",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("chevron-left", size=18),
                on_click=DashboardState.prev_page,
                disabled=DashboardState.page == 1,
                class_name="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-gray-600",
            ),
            rx.el.button(
                rx.icon("chevron-right", size=18),
                on_click=DashboardState.next_page,
                disabled=DashboardState.page == DashboardState.page_count,
                class_name="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-gray-600",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between mt-6 px-2",
    )


def expenses_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Expenses", class_name="text-xl font-bold text-gray-900"),
                rx.el.p(
                    "Manage and track your financial records.",
                    class_name="text-sm text-gray-500",
                ),
                class_name="mb-4 md:mb-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        size=16,
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search merchant...",
                        on_change=DashboardState.set_search_value.debounce(500),
                        class_name="pl-9 pr-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 outline-none w-full md:w-64",
                        default_value=DashboardState.search_value,
                    ),
                    class_name="relative",
                ),
                rx.el.select(
                    rx.el.option("All Categories", value="All"),
                    rx.el.option("Office", value="Office"),
                    rx.el.option("Travel", value="Travel"),
                    rx.el.option("Software", value="Software"),
                    rx.el.option("Marketing", value="Marketing"),
                    value=DashboardState.category_filter,
                    on_change=DashboardState.set_category_filter,
                    class_name="px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 outline-none appearance-none",
                ),
                rx.el.button(
                    rx.icon("plus", size=18, class_name="mr-2"),
                    "Add Expense",
                    on_click=DashboardState.set_is_add_open(True),
                    class_name="flex items-center px-4 py-2 bg-teal-600 text-white text-sm font-semibold rounded-xl hover:bg-teal-700 shadow-sm transition-all",
                ),
                class_name="flex flex-col md:flex-row gap-3 w-full md:w-auto",
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            table_header_cell("Merchant / Description", "merchant"),
                            table_header_cell("Category", "category"),
                            table_header_cell("Date", "date"),
                            table_header_cell("Status", "status"),
                            table_header_cell("Amount", "amount"),
                            rx.el.th("", class_name="pb-4 pr-4"),
                        )
                    ),
                    rx.el.tbody(
                        rx.cond(
                            DashboardState.paginated_expenses,
                            rx.foreach(DashboardState.paginated_expenses, expense_row),
                            rx.el.tr(
                                rx.el.td(
                                    rx.el.div(
                                        rx.icon(
                                            "inbox",
                                            size=48,
                                            class_name="text-gray-200 mb-2",
                                        ),
                                        rx.el.p(
                                            "No expenses found",
                                            class_name="text-gray-500 font-medium",
                                        ),
                                        class_name="flex flex-col items-center justify-center py-12",
                                    ),
                                    col_span=6,
                                )
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto",
            ),
            pagination_controls(),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
        ),
        add_expense_dialog(),
        edit_expense_dialog(),
        delete_confirm_dialog(),
        class_name="w-full max-w-full mx-auto pb-10",
    )