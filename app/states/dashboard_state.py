import reflex as rx
from typing import TypedDict
from datetime import datetime, timedelta
import random
from collections import defaultdict
import logging
import io
import csv


class Expense(TypedDict):
    id: str
    description: str
    amount: float
    date: str
    category: str
    status: str
    merchant: str


class Category(TypedDict):
    id: str
    name: str
    budget: float
    color: str
    icon: str


class MonthlyTrend(TypedDict):
    name: str
    amount: float


class CategoryBudget(TypedDict):
    name: str
    spent: float
    limit: float
    color: str


class ChartData(TypedDict):
    name: str
    value: float
    fill: str


class DashboardState(rx.State):
    """State for the dashboard and expense management."""
    
    current_page: str = "Dashboard"
    nav_items: list[str] = ["Dashboard", "Expenses", "Categories", "Reports"]
    expenses: list[Expense] = []
    categories: list[Category] = []
    total_budget: float = 5000.0
    search_value: str = ""
    category_filter: str = "All"
    sort_value: str = "date"
    sort_reverse: bool = True
    page: int = 1
    limit: int = 7
    is_add_open: bool = False
    is_edit_open: bool = False
    is_delete_open: bool = False
    is_cat_add_open: bool = False
    is_cat_edit_open: bool = False
    is_cat_delete_open: bool = False
    current_expense: Expense = {
        "id": "",
        "description": "",
        "amount": 0.0,
        "date": "",
        "category": "",
        "status": "",
        "merchant": "",
    }
    current_category: Category = {
        "id": "",
        "name": "",
        "budget": 0.0,
        "color": "bg-gray-500",
        "icon": "tag",
    }
    report_range: str = "This Month"
    chart_range: str = "Last 6 Months"
    user_profile: dict[str, str] = {"name": "John Morgan", "email": "john@example.com"}
    notifications: dict[str, bool] = {
        "email_alerts": True,
        "expense_reminders": False,
        "monthly_reports": True,
    }
    budget_settings: dict[str, float | int] = {
        "default_limit": 1000.0,
        "warning_threshold": 80,
    }
    currency: str = "USD ($)"
    is_clear_data_open: bool = False

    @rx.event
    def update_profile(self, form_data: dict):
        self.user_profile = {
            "name": form_data.get("name", self.user_profile["name"]),
            "email": form_data.get("email", self.user_profile["email"]),
        }
        yield rx.toast("Profile updated successfully", position="bottom-right")

    @rx.event
    def toggle_notification(self, key: str, value: bool):
        self.notifications[key] = value
        yield rx.toast(f"Notification preference updated", position="bottom-right")

    @rx.event
    def update_budget_settings(self, form_data: dict):
        try:
            limit = float(form_data.get("default_limit", 1000.0))
            threshold = int(form_data.get("warning_threshold", 80))
            self.budget_settings = {
                "default_limit": limit,
                "warning_threshold": threshold,
            }
            yield rx.toast("Budget settings saved", position="bottom-right")
        except ValueError as e:
            logging.exception(f"Error updating budget settings: {e}")
            yield rx.toast("Invalid input values", position="bottom-right")

    @rx.event
    def set_currency(self, value: str):
        self.currency = value
        yield rx.toast(f"Currency set to {value}", position="bottom-right")

    @rx.event
    def set_is_clear_data_open(self, value: bool):
        self.is_clear_data_open = value

    @rx.event
    def set_is_add_open(self, value: bool):
        self.is_add_open = value

    @rx.event
    def set_is_edit_open(self, value: bool):
        self.is_edit_open = value

    @rx.event
    def set_is_delete_open(self, value: bool):
        self.is_delete_open = value

    @rx.event
    def set_is_cat_add_open(self, value: bool):
        self.is_cat_add_open = value

    @rx.event
    def set_is_cat_edit_open(self, value: bool):
        self.is_cat_edit_open = value

    @rx.event
    def set_is_cat_delete_open(self, value: bool):
        self.is_cat_delete_open = value

    @rx.event
    def clear_all_data(self):
        self.expenses = []
        self.is_clear_data_open = False
        yield rx.toast("All expenses have been cleared", position="bottom-right")

    @rx.event
    def ensure_data(self):
        if not self.categories:
            self.categories = [
                {
                    "id": "C-1",
                    "name": "Office",
                    "budget": 1200.0,
                    "color": "bg-blue-500",
                    "icon": "building-2",
                },
                {
                    "id": "C-2",
                    "name": "Travel",
                    "budget": 2000.0,
                    "color": "bg-purple-500",
                    "icon": "plane",
                },
                {
                    "id": "C-3",
                    "name": "Software",
                    "budget": 800.0,
                    "color": "bg-green-500",
                    "icon": "laptop",
                },
                {
                    "id": "C-4",
                    "name": "Marketing",
                    "budget": 1500.0,
                    "color": "bg-orange-500",
                    "icon": "megaphone",
                },
                {
                    "id": "C-5",
                    "name": "Services",
                    "budget": 600.0,
                    "color": "bg-teal-500",
                    "icon": "wrench",
                },
            ]
        if not self.expenses:
            cat_names = [c["name"] for c in self.categories]
            statuses = ["Completed", "Pending", "Processing"]
            merchants = [
                "AWS",
                "Uber",
                "Slack",
                "Google Ads",
                "WeWork",
                "Delta",
                "Github",
                "Figma",
            ]
            cat_descriptions = {
                "Office": [
                    "Office supplies purchase",
                    "Printer ink refill",
                    "Desk accessories",
                    "Stationery order",
                    "Office furniture repair",
                ],
                "Travel": [
                    "Client meeting transport",
                    "Conference travel",
                    "Airport parking",
                    "Hotel accommodation",
                    "Flight booking",
                ],
                "Software": [
                    "Monthly subscription renewal",
                    "License upgrade",
                    "Cloud storage",
                    "IDE premium sub",
                    "Security software license",
                ],
                "Marketing": [
                    "Social media campaign",
                    "Print advertising",
                    "Event sponsorship",
                    "Email marketing service",
                    "Promotional materials",
                ],
                "Services": [
                    "Consulting fee",
                    "Professional services",
                    "Maintenance contract",
                    "Technical support fee",
                    "Legal consultation",
                ],
            }
            today = datetime.now()
            new_expenses = []
            for i in range(50):
                days_ago = random.randint(0, 180)
                date = today - timedelta(days=days_ago)
                category = random.choice(cat_names)
                descriptions_pool = cat_descriptions.get(
                    category, ["Miscellaneous expense"]
                )
                description = random.choice(descriptions_pool)
                new_expenses.append(
                    {
                        "id": f"EXP-{1000 + i}",
                        "description": description,
                        "amount": round(random.uniform(20.0, 500.0), 2),
                        "date": date.strftime("%Y-%m-%d"),
                        "category": category,
                        "status": random.choice(statuses)
                        if days_ago < 7
                        else "Completed",
                        "merchant": random.choice(merchants),
                    }
                )
            self.expenses = sorted(new_expenses, key=lambda x: x["date"], reverse=True)

    @rx.event
    def set_page(self, page: str):
        self.current_page = page

    @rx.event
    def set_search_value(self, value: str):
        self.search_value = value
        self.page = 1

    @rx.event
    def set_category_filter(self, value: str):
        self.category_filter = value
        self.page = 1

    @rx.event
    def set_report_range(self, value: str):
        self.report_range = value

    @rx.event
    def set_chart_range(self, value: str):
        self.chart_range = value

    @rx.event
    def toggle_sort(self, field: str):
        if self.sort_value == field:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_value = field
            self.sort_reverse = True

    @rx.event
    def prev_page(self):
        if self.page > 1:
            self.page -= 1

    @rx.event
    def next_page(self):
        if self.page < self.page_count:
            self.page += 1

    @rx.event
    def add_expense(self, form_data: dict):
        new_id = f"EXP-{random.randint(10000, 99999)}"
        new_expense: Expense = {
            "id": new_id,
            "description": form_data.get("description", ""),
            "amount": float(form_data.get("amount", 0) or 0),
            "date": form_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "category": form_data.get("category", "Office"),
            "status": "Pending",
            "merchant": form_data.get("merchant", "Unknown"),
        }
        self.expenses = [new_expense] + self.expenses
        self.is_add_open = False
        yield rx.toast("Expense added successfully", position="bottom-right")

    @rx.event
    def open_edit_modal(self, expense: Expense):
        self.current_expense = expense
        self.is_edit_open = True

    @rx.event
    def update_expense(self, form_data: dict):
        expense_id = form_data.get("id")
        updated_expenses = []
        for expense in self.expenses:
            if expense["id"] == expense_id:
                expense["merchant"] = form_data.get("merchant", expense["merchant"])
                expense["description"] = form_data.get(
                    "description", expense["description"]
                )
                expense["amount"] = float(form_data.get("amount", expense["amount"]))
                expense["date"] = form_data.get("date", expense["date"])
                expense["category"] = form_data.get("category", expense["category"])
            updated_expenses.append(expense)
        self.expenses = updated_expenses
        self.is_edit_open = False
        yield rx.toast("Expense updated successfully", position="bottom-right")

    @rx.event
    def open_delete_modal(self, expense: Expense):
        self.current_expense = expense
        self.is_delete_open = True

    @rx.event
    def delete_expense(self):
        self.expenses = [
            e for e in self.expenses if e["id"] != self.current_expense["id"]
        ]
        self.is_delete_open = False
        yield rx.toast("Expense deleted", position="bottom-right")

    @rx.event
    def open_cat_add_modal(self):
        self.current_category = {
            "id": "",
            "name": "",
            "budget": 0.0,
            "color": "bg-gray-500",
            "icon": "tag",
        }
        self.is_cat_add_open = True

    @rx.event
    def add_category(self, form_data: dict):
        new_id = f"C-{random.randint(100, 999)}"
        new_cat: Category = {
            "id": new_id,
            "name": form_data.get("name", "New Category"),
            "budget": float(form_data.get("budget", 0) or 0),
            "color": form_data.get("color", "bg-gray-500"),
            "icon": "tag",
        }
        self.categories.append(new_cat)
        self.is_cat_add_open = False
        yield rx.toast("Category created", position="bottom-right")

    @rx.event
    def open_cat_edit_modal(self, category: Category):
        self.current_category = category
        self.is_cat_edit_open = True

    @rx.event
    def update_category(self, form_data: dict):
        cat_id = form_data.get("id")
        new_cats = []
        for c in self.categories:
            if c["id"] == cat_id:
                c["name"] = form_data.get("name", c["name"])
                c["budget"] = float(form_data.get("budget", c["budget"]))
                c["color"] = form_data.get("color", c["color"])
            new_cats.append(c)
        self.categories = new_cats
        self.is_cat_edit_open = False
        yield rx.toast("Category updated", position="bottom-right")

    @rx.event
    def open_cat_delete_modal(self, category: Category):
        self.current_category = category
        self.is_cat_delete_open = True

    @rx.event
    def delete_category(self):
        self.categories = [
            c for c in self.categories if c["id"] != self.current_category["id"]
        ]
        self.is_cat_delete_open = False
        yield rx.toast("Category deleted", position="bottom-right")

    @rx.event
    def export_report(self):
        """Generates and downloads a CSV file of the currently filtered report expenses."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["ID", "Date", "Merchant", "Category", "Description", "Amount", "Status"]
        )
        for expense in self.report_expenses:
            writer.writerow(
                [
                    expense["id"],
                    expense["date"],
                    expense["merchant"],
                    expense["category"],
                    expense["description"],
                    expense["amount"],
                    expense["status"],
                ]
            )
        csv_data = output.getvalue()
        output.close()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fintrack_export_{timestamp}.csv"
        yield rx.toast(f"Exporting data to {filename}...", position="bottom-right")
        return rx.download(data=csv_data, filename=filename)

    @rx.var
    def user_avatar(self) -> str:
        name = self.user_profile.get("name", "User")
        return f"https://api.dicebear.com/9.x/notionists/svg?seed={name}"

    @rx.var
    def category_names(self) -> list[str]:
        return [c["name"] for c in self.categories]

    @rx.var
    def filtered_sorted_expenses(self) -> list[Expense]:
        self.ensure_data()
        items = self.expenses
        if self.category_filter != "All":
            items = [i for i in items if i["category"] == self.category_filter]
        if self.search_value:
            term = self.search_value.lower()
            items = [
                i
                for i in items
                if term in i["merchant"].lower() or term in i["description"].lower()
            ]

        @rx.event
        def get_sort_key(item):
            val = item.get(self.sort_value, "")
            if self.sort_value == "amount":
                return float(val)
            return str(val).lower()

        items.sort(key=get_sort_key, reverse=self.sort_reverse)
        return items

    @rx.var
    def page_count(self) -> int:
        return max(
            1, (len(self.filtered_sorted_expenses) + self.limit - 1) // self.limit
        )

    @rx.var
    def paginated_expenses(self) -> list[Expense]:
        start = (self.page - 1) * self.limit
        end = start + self.limit
        return self.filtered_sorted_expenses[start:end]

    @rx.var
    def total_expenses(self) -> float:
        self.ensure_data()
        return sum((e["amount"] for e in self.expenses))

    @rx.var
    def current_month_expenses(self) -> float:
        self.ensure_data()
        current_month = datetime.now().strftime("%Y-%m")
        return sum(
            (e["amount"] for e in self.expenses if e["date"].startswith(current_month))
        )

    @rx.var
    def budget_usage_percent(self) -> float:
        if self.total_budget == 0:
            return 0.0
        return min(
            round(self.current_month_expenses / self.total_budget * 100, 1), 100.0
        )

    @rx.var
    def monthly_trend_data(self) -> list[MonthlyTrend]:
        self.ensure_data()
        monthly_map = defaultdict(float)
        now = datetime.now()
        for i in range(5, -1, -1):
            month_date = now - timedelta(days=i * 30)
            key = month_date.strftime("%b")
            monthly_map[key] = 0.0
        for expense in self.expenses:
            try:
                dt = datetime.strptime(expense["date"], "%Y-%m-%d")
                if (now - dt).days < 180:
                    key = dt.strftime("%b")
                    monthly_map[key] += expense["amount"]
            except Exception as e:
                logging.exception(f"Error parsing date: {e}")
        months_order = []
        for i in range(5, -1, -1):
            month_date = now - timedelta(days=i * 30)
            key = month_date.strftime("%b")
            if key not in months_order:
                months_order.append(key)
        return [{"name": m, "amount": round(monthly_map[m], 2)} for m in months_order]

    @rx.var
    def chart_trend_data(self) -> list[MonthlyTrend]:
        self.ensure_data()
        monthly_map = defaultdict(float)
        now = datetime.now()
        if self.chart_range == "This Year":
            current_year = now.year
            months_labels = []
            for i in range(1, 13):
                d = datetime(current_year, i, 1)
                m_name = d.strftime("%b")
                months_labels.append(m_name)
                monthly_map[m_name] = 0.0
            for expense in self.expenses:
                try:
                    edate = datetime.strptime(expense["date"], "%Y-%m-%d")
                    if edate.year == current_year:
                        key = edate.strftime("%b")
                        monthly_map[key] += expense["amount"]
                except Exception as e:
                    logging.exception(f"Error parsing date: {e}")
            return [
                {"name": m, "amount": round(monthly_map[m], 2)} for m in months_labels
            ]
        else:
            months_order = []
            for i in range(5, -1, -1):
                month_date = now - timedelta(days=i * 30)
                key = month_date.strftime("%b")
                monthly_map[key] = 0.0
                if key not in months_order:
                    months_order.append(key)
            for expense in self.expenses:
                try:
                    dt = datetime.strptime(expense["date"], "%Y-%m-%d")
                    if (now - dt).days < 180:
                        key = dt.strftime("%b")
                        monthly_map[key] += expense["amount"]
                except Exception as e:
                    logging.exception(f"Error parsing date: {e}")
            return [
                {"name": m, "amount": round(monthly_map[m], 2)} for m in months_order
            ]

    @rx.var
    def recent_expenses(self) -> list[Expense]:
        self.ensure_data()
        return self.expenses[:5]

    @rx.var
    def category_budgets(self) -> list[CategoryBudget]:
        self.ensure_data()
        cats = {}
        for c in self.categories:
            cats[c["name"]] = {"spent": 0.0, "limit": c["budget"], "color": c["color"]}
        current_month = datetime.now().strftime("%Y-%m")
        for e in self.expenses:
            if e["date"].startswith(current_month) and e["category"] in cats:
                cats[e["category"]]["spent"] += e["amount"]
        return [
            {
                "name": k,
                "spent": round(v["spent"], 2),
                "limit": v["limit"],
                "color": v["color"],
            }
            for k, v in cats.items()
        ]

    @rx.var
    def report_expenses(self) -> list[Expense]:
        self.ensure_data()
        now = datetime.now()
        filtered = []
        if self.report_range == "This Week":
            start_date = now - timedelta(days=now.weekday())
            start_str = start_date.strftime("%Y-%m-%d")
            filtered = [e for e in self.expenses if e["date"] >= start_str]
        elif self.report_range == "This Month":
            month_prefix = now.strftime("%Y-%m")
            filtered = [e for e in self.expenses if e["date"].startswith(month_prefix)]
        elif self.report_range == "Last Month":
            first_current = now.replace(day=1)
            last_month = first_current - timedelta(days=1)
            month_prefix = last_month.strftime("%Y-%m")
            filtered = [e for e in self.expenses if e["date"].startswith(month_prefix)]
        elif self.report_range == "This Year":
            year_prefix = now.strftime("%Y")
            filtered = [e for e in self.expenses if e["date"].startswith(year_prefix)]
        else:
            filtered = self.expenses
        return filtered

    @rx.var
    def report_total(self) -> float:
        return sum((e["amount"] for e in self.report_expenses))

    @rx.var
    def report_pie_data(self) -> list[ChartData]:
        data = defaultdict(float)
        for e in self.report_expenses:
            data[e["category"]] += e["amount"]
        cat_colors = {c["name"]: c["color"] for c in self.categories}
        color_map = {
            "bg-blue-500": "#3b82f6",
            "bg-purple-500": "#a855f7",
            "bg-green-500": "#22c55e",
            "bg-orange-500": "#f97316",
            "bg-teal-500": "#14b8a6",
            "bg-gray-500": "#6b7280",
            "bg-red-500": "#ef4444",
            "bg-yellow-500": "#eab308",
            "bg-indigo-500": "#6366f1",
            "bg-pink-500": "#ec4899",
        }
        return [
            {
                "name": k,
                "value": round(v, 2),
                "fill": color_map.get(cat_colors.get(k, "bg-gray-500"), "#6b7280"),
            }
            for k, v in data.items()
            if v > 0
        ]

    @rx.var
    def report_trend_data(self) -> list[dict]:
        data = defaultdict(float)
        for e in self.report_expenses:
            data[e["date"]] += e["amount"]
        sorted_dates = sorted(data.keys())
        if not sorted_dates:
            return []
        return [{"name": d[5:], "amount": v} for d, v in data.items()]