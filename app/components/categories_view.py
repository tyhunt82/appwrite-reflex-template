import reflex as rx
from app.states.dashboard_state import DashboardState, Category


def category_card(category: Category) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(category["icon"], class_name="text-white", size=20),
                class_name=f"w-10 h-10 rounded-xl {category['color']} flex items-center justify-center shadow-md opacity-90",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", size=16),
                    class_name="p-2 text-gray-400 hover:text-teal-600 hover:bg-teal-50 rounded-lg transition-colors",
                    on_click=lambda: DashboardState.open_cat_edit_modal(category),
                ),
                rx.el.button(
                    rx.icon("trash-2", size=16),
                    class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                    on_click=lambda: DashboardState.open_cat_delete_modal(category),
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-start justify-between mb-4",
        ),
        rx.el.h3(category["name"], class_name="text-lg font-bold text-gray-900 mb-1"),
        rx.el.p(
            f"Budget Limit: ${category['budget']:,.0f}",
            class_name="text-sm text-gray-500 font-medium",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-all",
    )


def category_form_dialog(
    header: str, submit_handler: callable, is_edit: bool = False
) -> rx.Component:
    return rx.el.form(
        rx.cond(
            is_edit,
            rx.el.input(
                type="hidden", name="id", value=DashboardState.current_category["id"]
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Category Name",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    name="name",
                    placeholder="e.g. Utilities",
                    default_value=DashboardState.current_category["name"],
                    class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm",
                    required=True,
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Monthly Budget Limit ($)",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    type="number",
                    name="budget",
                    placeholder="0.00",
                    default_value=DashboardState.current_category["budget"].to_string(),
                    class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm",
                    required=True,
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Color Theme",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.el.option("Blue", value="bg-blue-500"),
                    rx.el.option("Purple", value="bg-purple-500"),
                    rx.el.option("Green", value="bg-green-500"),
                    rx.el.option("Orange", value="bg-orange-500"),
                    rx.el.option("Red", value="bg-red-500"),
                    rx.el.option("Teal", value="bg-teal-500"),
                    rx.el.option("Yellow", value="bg-yellow-500"),
                    rx.el.option("Indigo", value="bg-indigo-500"),
                    rx.el.option("Pink", value="bg-pink-500"),
                    rx.el.option("Gray", value="bg-gray-500"),
                    name="color",
                    default_value=DashboardState.current_category["color"],
                    class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition-all text-sm bg-white appearance-none",
                ),
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
                "Save Category",
                type="submit",
                class_name="px-4 py-2 rounded-xl text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 shadow-sm shadow-teal-600/20 transition-all",
            ),
            class_name="flex items-center justify-end gap-3",
        ),
        on_submit=submit_handler,
        reset_on_submit=True,
    )


def add_category_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.h2("New Category", class_name="text-xl font-bold text-gray-900 mb-6"),
            category_form_dialog(
                "New Category", DashboardState.add_category, is_edit=False
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-md w-full outline-none",
        ),
        open=DashboardState.is_cat_add_open,
        on_open_change=DashboardState.set_is_cat_add_open,
    )


def edit_category_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.h2(
                "Edit Category", class_name="text-xl font-bold text-gray-900 mb-6"
            ),
            category_form_dialog(
                "Edit Category", DashboardState.update_category, is_edit=True
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-md w-full outline-none",
        ),
        open=DashboardState.is_cat_edit_open,
        on_open_change=DashboardState.set_is_cat_edit_open,
    )


def delete_category_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.icon("cigarette", class_name="text-red-500 mb-4", size=48),
                rx.el.h2(
                    "Delete Category?",
                    class_name="text-xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    f"Are you sure you want to delete ",
                    rx.el.span(
                        DashboardState.current_category["name"],
                        class_name="font-semibold",
                    ),
                    "? This will not delete expenses but may affect reporting.",
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
                        on_click=DashboardState.delete_category,
                        class_name="px-4 py-2 rounded-xl text-sm font-medium text-white bg-red-600 hover:bg-red-700 shadow-sm shadow-red-600/20 transition-all w-full",
                    ),
                    class_name="flex items-center gap-3 w-full",
                ),
                class_name="flex flex-col items-center",
            ),
            class_name="bg-white p-6 rounded-2xl shadow-xl max-w-sm w-full outline-none",
        ),
        open=DashboardState.is_cat_delete_open,
        on_open_change=DashboardState.set_is_cat_delete_open,
    )


def categories_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Categories", class_name="text-xl font-bold text-gray-900"),
                rx.el.p(
                    "Manage spending categories and budget limits.",
                    class_name="text-sm text-gray-500",
                ),
            ),
            rx.el.button(
                rx.icon("plus", size=18, class_name="mr-2"),
                "New Category",
                on_click=DashboardState.open_cat_add_modal,
                class_name="flex items-center px-4 py-2 bg-teal-600 text-white text-sm font-semibold rounded-xl hover:bg-teal-700 shadow-sm transition-all",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.foreach(DashboardState.categories, category_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
        ),
        add_category_dialog(),
        edit_category_dialog(),
        delete_category_dialog(),
        class_name="w-full max-w-full mx-auto pb-10",
    )