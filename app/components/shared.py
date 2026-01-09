import reflex as rx


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Completed",
                "px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-100",
            ),
            (
                "Pending",
                "px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-100",
            ),
            (
                "Processing",
                "px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-100",
            ),
            "px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-50 text-gray-600 border border-gray-100",
        ),
    )


def category_icon(category: str) -> rx.Component:
    return rx.el.div(
        rx.match(
            category,
            ("Office", rx.icon("building-2", size=16, class_name="text-blue-600")),
            ("Travel", rx.icon("plane", size=16, class_name="text-purple-600")),
            ("Software", rx.icon("laptop", size=16, class_name="text-pink-600")),
            ("Marketing", rx.icon("megaphone", size=16, class_name="text-orange-600")),
            rx.icon("receipt", size=16, class_name="text-gray-600"),
        ),
        class_name="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center",
    )