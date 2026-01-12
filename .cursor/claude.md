# Reflex + Appwrite Template

## Project Overview

A Reflex-based web application template with Appwrite backend services. Currently in setup phase - establishing proper project structure before feature development.

**Stack:**
- Frontend: Reflex (Python) + TailwindCSS v3 + Radix UI
- Backend: Reflex built-in FastAPI
- Services: Appwrite (Database, Auth, Storage, Functions)
- Build: uv (Python), Bun (JavaScript)

---

## Directory Structure

```
app/
├── components/
│   ├── shared/             # Reusable across all pages
│   │   ├── sidebar.py      # Navigation sidebar (collapsible)
│   │   ├── header.py       # Page header
│   │   ├── footer.py       # Page footer
│   │   ├── theme_toggle.py # Dark/light/system mode
│   │   └── common.py       # Badges, buttons, cards, etc.
│   ├── dashboard/          # Dashboard-specific components
│   │   └── ...
│   └── admin/              # Admin-specific components
│       └── ...
├── pages/
│   ├── dashboard/
│   │   ├── index.py        # Main dashboard page
│   │   └── state.py        # Dashboard state (Nuxt-style colocated)
│   ├── admin/
│   │   ├── index.py        # Admin dashboard
│   │   ├── users.py        # User management
│   │   ├── teams.py        # Team management
│   │   └── state.py        # Admin state
│   └── settings/
│       ├── index.py        # Settings page
│       └── state.py        # Settings state
├── server/
│   ├── api/
│   │   ├── __init__.py     # Router registration
│   │   ├── dashboard_routes.py
│   │   └── admin_routes.py
│   └── utils/
│       └── __init__.py
├── states/
│   └── base.py             # Shared/global state (minimal)
├── config.py               # Pydantic Settings
├── app.py                  # Entry point, route registration
└── __init__.py
```

---

## Architecture Principles

### 1. Nuxt-Style Page Organization
Each page folder contains its own `state.py`. State is colocated with the page it serves.

```python
# pages/dashboard/state.py
class DashboardState(rx.State):
    # Dashboard-specific state only
    ...

# pages/dashboard/index.py
from .state import DashboardState

def dashboard_page() -> rx.Component:
    ...
```

### 2. File Size Limit: 500 Lines Max
- Break large components into smaller files
- Place extracted components in the appropriate `components/` subfolder
- Import and compose in the page file

### 3. Component Organization
```
components/
├── shared/     # Used by multiple pages (nav, header, footer)
├── dashboard/  # Only used by dashboard pages
└── admin/      # Only used by admin pages
```

### 4. FastAPI Integration
Reflex includes FastAPI. Custom API routes go in `server/api/`.

```python
# server/api/dashboard_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/health")
async def health_check():
    return {"status": "ok"}
```

Register in `app.py`:
```python
from app.server.api import dashboard_routes
app.api.include_router(dashboard_routes.router)
```

### 5. Configuration with Pydantic Settings
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Reflex App"
    debug: bool = False

    # Appwrite
    appwrite_endpoint: str = ""
    appwrite_project_id: str = ""

    # Theme defaults
    default_theme: str = "system"
    sidebar_collapsed: bool = False

    class Config:
        env_file = ".env.local"

settings = Settings()
```

---

## State Management

### Global State (Minimal)
```python
# states/base.py
class BaseState(rx.State):
    """Shared state - keep minimal"""
    sidebar_collapsed: bool = False

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed
```

### Page State (Nuxt-style)
```python
# pages/settings/state.py
from app.states.base import BaseState

class SettingsState(BaseState):
    """Settings page state - inherits sidebar toggle"""
    theme: str = "system"

    @rx.event
    def set_theme(self, theme: str):
        self.theme = theme
```

---

## Routing

### Page Routes
Define in `app.py` using Reflex's `add_page`:

```python
# app.py
from app.pages.dashboard.index import dashboard_page
from app.pages.admin.index import admin_page
from app.pages.settings.index import settings_page

app = rx.App(theme=rx.theme(appearance="inherit"))

app.add_page(dashboard_page, route="/", title="Dashboard")
app.add_page(admin_page, route="/admin", title="Admin")
app.add_page(settings_page, route="/settings", title="Settings")
```

### API Routes
Register FastAPI routers:

```python
# app.py
from app.server.api import dashboard_routes, admin_routes

app.api.include_router(dashboard_routes.router)
app.api.include_router(admin_routes.router)
```

---

## Styling Conventions

### TailwindCSS
- Use Tailwind utility classes via `class_name`
- Responsive: `md:`, `lg:` prefixes
- Dark mode: `dark:` prefix (handled by Radix theme)

### Color Scheme
- Primary: Teal (`teal-500`, `teal-600`)
- Neutral: Gray scale
- Status: Emerald (success), Amber (warning), Red (error)

### Component Patterns
```python
# Consistent card pattern
rx.box(
    # content
    class_name="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6"
)

# Consistent button pattern
rx.button(
    "Action",
    class_name="bg-teal-500 hover:bg-teal-600 text-white rounded-lg px-4 py-2"
)
```

---

## Development Workflow

### Running Locally
```bash
# Start dev server
reflex run

# Or with hot reload
reflex run --loglevel debug
```

### Building for Production
```bash
# Export frontend
reflex export --frontend-only

# Output: .web/_static/
```

### Deployment
- Frontend: Appwrite Sites
- Backend: Appwrite Functions (Python runtime)

---

## Current Phase

**Phase 1: Project Structure Setup**
- [ ] Reorganize into Nuxt-style structure
- [ ] Simplify to base pages (dashboard, admin, settings)
- [ ] Implement sidebar toggle
- [ ] Implement theme toggle
- [ ] Setup Pydantic Settings
- [ ] Basic FastAPI health endpoints
- [ ] Test locally

**Phase 2: Appwrite Integration**
- [ ] Configure Appwrite project
- [ ] Implement authentication
- [ ] Database collections setup
- [ ] User settings persistence

---

## Code Guidelines

### Imports
```python
# Standard library
from datetime import datetime

# Third party
import reflex as rx
from pydantic_settings import BaseSettings

# Local - absolute imports from app
from app.components.shared.sidebar import sidebar
from app.pages.dashboard.state import DashboardState
```

### Type Hints
Always use type hints for function signatures:
```python
def my_component(title: str, count: int = 0) -> rx.Component:
    ...
```

### Event Handlers
Use `@rx.event` decorator for all state mutations:
```python
@rx.event
def handle_action(self, value: str):
    self.some_state = value
```

### Docstrings
Brief docstrings for non-obvious functions:
```python
def complex_calculation(data: list[dict]) -> float:
    """Calculate weighted average from transaction data."""
    ...
```

---

## File Templates

### New Page Template
```python
# pages/{page_name}/index.py
import reflex as rx
from app.components.shared.sidebar import sidebar
from app.components.shared.header import header
from .state import PageState

def page_name_page() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            header("Page Title"),
            # Page content here
            class_name="flex-1 ml-0 md:ml-72 p-6"
        ),
        class_name="min-h-screen bg-gray-50 dark:bg-gray-900"
    )
```

### New State Template
```python
# pages/{page_name}/state.py
import reflex as rx
from app.states.base import BaseState

class PageState(BaseState):
    """State for {page_name} page."""

    # State variables
    example_var: str = ""

    # Event handlers
    @rx.event
    def handle_example(self, value: str):
        self.example_var = value
```

### New API Route Template
```python
# server/api/{route_name}_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/{route_name}", tags=["{route_name}"])

class ExampleRequest(BaseModel):
    field: str

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/action")
async def action(request: ExampleRequest):
    return {"received": request.field}
```

---

## Appwrite Integration (Future)

### Collections Structure
```
Database: main
├── users           # User profiles
├── settings        # User settings (theme, preferences)
├── teams           # Team/organization data
└── audit_log       # Activity tracking
```

### Environment Variables
```bash
# .env.local
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your-project-id
APPWRITE_API_KEY=your-api-key
APPWRITE_DATABASE_ID=main
```

---

## Quick Reference

| Task | Command/Location |
|------|------------------|
| Run dev server | `reflex run` |
| Add new page | Create `pages/{name}/index.py` + `state.py` |
| Add component | `components/{scope}/{name}.py` |
| Add API route | `server/api/{name}_routes.py` |
| Config settings | `config.py` (Pydantic Settings) |
| Register route | `app.py` → `app.add_page()` |
| Register API | `app.py` → `app.api.include_router()` |
