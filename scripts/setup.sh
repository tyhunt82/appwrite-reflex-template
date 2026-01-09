#!/bin/bash
# setup.sh - Initialize Reflex + Appwrite template structure
# TODO: Ensure checking before creating new or over writing existing files/folders

set -e

echo "🚀 Setting up Reflex + Appwrite Template..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create .cursor directory structure
echo -e "${BLUE}📁 Creating .cursor directory structure...${NC}"
mkdir -p .cursor/agents

# Create scripts directory
mkdir -p scripts

# Create project structure
echo -e "${BLUE}📁 Creating project structure...${NC}"
mkdir -p {frontend,backend,appwrite}/{components,pages,state,styles,api,models,services,utils,functions,collections}
mkdir -p .github/workflows
mkdir -p docs/{getting-started,architecture,api,guides,troubleshooting}

# Create main files
echo -e "${BLUE}📝 Creating configuration files...${NC}"

# .cursorrules
cat > .cursorrules << 'EOF'
# Reflex + Appwrite Template - Multi-Agent System

You are the PRIMARY ORCHESTRATOR AGENT for this Reflex + Appwrite template project.

## Core Directive
- You MUST read @.cursor/claude.md at the start of EVERY conversation
- You coordinate specialized sub-agents but ONLY YOU communicate with the user
- Follow the agent hierarchy and handoff protocols defined in claude.md

## Critical Architecture Note
- Reflex INCLUDES FastAPI built-in - do NOT create a separate FastAPI app
- Backend logic goes in Reflex State classes as event handlers
- Custom REST endpoints can be added to Reflex's app.api if needed

## Quick Reference
- Main orchestration: @.cursor/claude.md
- Sub-agents: @.cursor/agents/
- Process: analyze → plan → delegate → review → integrate → communicate

## Project Stack
- Frontend: Reflex (Python components)
- Backend: Reflex State + FastAPI (built-in)
- Services: Appwrite (Database, Auth, Storage, Functions)
- Frontend Deploy: Appwrite Sites (static)
- Backend Deploy: Appwrite Functions (Python runtime)

## Important
- Always reference claude.md for detailed protocols
- Never let sub-agents communicate directly with user
- Maintain consistent code quality across all agents
EOF

# .env.example
cat > .env.example << 'EOF'
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=main

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# Backend Configuration
BACKEND_URL=http://localhost:8000

# Feature Flags
ENABLE_ANALYTICS=false
ENABLE_LOGGING=true
EOF

# .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Reflex
.web/
*.db
*.db-shm
*.db-wal

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Build
dist/
build/
*.egg-info/

# Appwrite
.appwrite/
EOF

# rxconfig.py
cat > rxconfig.py << 'EOF'
"""Reflex configuration file."""
import reflex as rx

config = rx.Config(
    app_name="reflex_appwrite_template",
    api_url="http://localhost:8000",
    frontend_port=3000,
    backend_port=8000,
    db_url="sqlite:///reflex.db",
)
EOF

# requirements.txt
cat > requirements.txt << 'EOF'
reflex>=0.6.0
appwrite>=5.0.0
pydantic>=2.5.0
python-dotenv>=1.0.0
httpx>=0.27.0
EOF

# Create README.md
cat > README.md << 'EOF'
# Reflex + Appwrite Template

Multi-tenant SaaS template using Reflex (Python) and Appwrite (Backend-as-a-Service).

## Stack

- **Frontend**: Reflex (Python-based React alternative)
- **Backend**: Reflex State + FastAPI (built-in)
- **Services**: Appwrite (Database, Auth, Storage, Functions)
- **Deployment**: Appwrite Sites (frontend) + Appwrite Functions (backend)

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your Appwrite credentials

# Initialize Reflex
reflex init

# Run development server
reflex run
```

Visit http://localhost:3000

## Documentation

See `docs/` folder for detailed documentation.

## Project Structure
```
reflex-appwrite-template/
├── .cursor/              # Claude Code agent definitions
├── frontend/             # Reflex components and pages
├── backend/              # Reflex State and custom API routes
├── appwrite/             # Appwrite configuration
├── scripts/              # Setup and deployment scripts
└── docs/                 # Project documentation
```

## Architecture

Reflex handles both frontend (Python components) and backend (FastAPI + State).
Appwrite provides database, authentication, and storage services.

## Deployment

See `docs/guides/deployment.md` for deployment instructions.
EOF

# Create initial Python files
cat > frontend/__init__.py << 'EOF'
"""Frontend package."""
EOF

cat > backend/__init__.py << 'EOF'
"""Backend package."""
EOF

# Create appwrite.json
cat > appwrite.json << 'EOF'
{
  "projectId": "",
  "projectName": "Reflex Appwrite Template",
  "databases": [
    {
      "databaseId": "main",
      "name": "Main Database"
    }
  ],
  "collections": [],
  "functions": []
}
EOF

echo -e "${GREEN}✅ Project structure created${NC}"

# Create documentation files
echo -e "${BLUE}📚 Creating initial documentation...${NC}"

cat > docs/README.md << 'EOF'
# Documentation

## Getting Started
- [Installation](getting-started/installation.md)
- [Quick Start](getting-started/quick-start.md)
- [Project Structure](getting-started/project-structure.md)

## Architecture
- [System Overview](architecture/overview.md)
- [Data Flow](architecture/data-flow.md)
- [Deployment](architecture/deployment.md)

## API
- [Authentication](api/authentication.md)
- [Endpoints](api/endpoints.md)

## Guides
- [Creating Features](guides/creating-features.md)
- [Testing](guides/testing.md)
- [Deployment](guides/deployment.md)

## Troubleshooting
- [Common Issues](troubleshooting/common-issues.md)
- [Debugging](troubleshooting/debugging.md)
EOF

echo -e "${GREEN}✅ Documentation structure created${NC}"

# Check for required tools
echo -e "${BLUE}🔍 Checking for required tools...${NC}"

command -v python3 >/dev/null 2>&1 || { 
    echo -e "${YELLOW}⚠️  Python 3 not found. Please install Python 3.11+${NC}"
}

command -v pip >/dev/null 2>&1 || { 
    echo -e "${YELLOW}⚠️  pip not found. Please install pip${NC}"
}

command -v git >/dev/null 2>&1 || { 
    echo -e "${YELLOW}⚠️  git not found. Please install git${NC}"
}

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Copy .env.example to .env and add your Appwrite credentials"
echo "2. Run: pip install -r requirements.txt"
echo "3. Run: reflex init"
echo "4. Run: reflex run"
echo ""
echo -e "${BLUE}📖 See README.md for more information${NC}"