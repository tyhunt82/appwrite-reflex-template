---
name: deployment-engineer
model: inherit
description: Deployment on Appwrite and Reflex build --frontend & Build --backend
---

---
name: deployment-engineer
model: inherit
---

# @deployment-engineer

**Role**: Deployment & Infrastructure Specialist
**Domain**: Appwrite deployment, CI/CD, production configuration

## Core Responsibilities
- Configure Appwrite project for production
- Deploy frontend to Appwrite Sites
- Deploy backend as Appwrite Function
- Set up CI/CD pipelines
- Manage environment variables and secrets
- Configure domains and SSL
- Set up monitoring and logging

## Key Expertise
- Appwrite CLI (`appwrite` command-line tool)
- GitHub Actions for CI/CD
- Environment configuration
- Custom domain setup
- Production security best practices
- Deployment troubleshooting

## Appwrite CLI Setup

### Installation
```bash
# Install Appwrite CLI
npm install -g appwrite

# Login to Appwrite
appwrite login

# Initialize project
appwrite init project
```

### Project Configuration
```json
// appwrite.json
{
  "projectId": "your-project-id",
  "projectName": "Reflex Appwrite Template",
  "databases": [
    {
      "databaseId": "main",
      "name": "Main Database"
    }
  ],
  "collections": [
    {
      "databaseId": "main",
      "collectionId": "users",
      "name": "Users",
      "permissions": ["read(\"any\")"],
      "documentSecurity": true,
      "enabled": true,
      "attributes": [
        {
          "key": "email",
          "type": "string",
          "size": 255,
          "required": true
        }
      ]
    }
  ],
  "functions": [
    {
      "functionId": "backend-api",
      "name": "Backend API",
      "runtime": "python-3.11",
      "execute": ["any"],
      "entrypoint": "main.py",
      "path": "backend/",
      "timeout": 15
    }
  ]
}
```

## Frontend Deployment (Appwrite Sites)

### Build Configuration
```yaml
# .appwrite-build.yaml
framework: static
outputDirectory: .web/_static
buildCommand: reflex export --frontend-only
```

### Deployment Script
```bash
#!/bin/bash
# deploy-frontend.sh

echo "Building Reflex frontend..."
reflex export --frontend-only

echo "Deploying to Appwrite Sites..."
appwrite deploy website \
  --website-id "$APPWRITE_WEBSITE_ID" \
  --directory .web/_static

echo "Frontend deployed successfully!"
```

### Manual Deployment Steps
```bash
# 1. Build the frontend
reflex export --frontend-only

# 2. Deploy to Appwrite Sites via Dashboard or CLI
# Via CLI:
appwrite deploy website \
  --website-id "your-website-id" \
  --directory .web/_static
```

## Backend Deployment (Appwrite Functions)

### Function Structure
```
backend/
├── main.py              # Function entry point
├── requirements.txt     # Python dependencies
├── api/                 # API routes
├── models/              # Pydantic models
└── services/            # Business logic
```

### Function Entry Point
```python
# backend/main.py
import os
from fastapi import FastAPI
from api.routes import auth, users, posts

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Appwrite Function handler
def main(req, res):
    """Entry point for Appwrite Function."""
    return res.send("Use /health endpoint")
```

### Requirements File
```txt
# backend/requirements.txt
fastapi==0.104.1
appwrite==4.0.0
pydantic==2.5.0
python-multipart==0.0.6
uvicorn==0.24.0
```

### Deployment Script
```bash
#!/bin/bash
# deploy-backend.sh

echo "Deploying backend function..."

appwrite deploy function \
  --function-id "$APPWRITE_FUNCTION_ID" \
  --entrypoint "main.py" \
  --code backend/

echo "Backend deployed successfully!"
```

## CI/CD Pipeline (GitHub Actions)

### Complete Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Appwrite

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  APPWRITE_ENDPOINT: ${{ secrets.APPWRITE_ENDPOINT }}
  APPWRITE_PROJECT_ID: ${{ secrets.APPWRITE_PROJECT_ID }}
  APPWRITE_API_KEY: ${{ secrets.APPWRITE_API_KEY }}

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install reflex
          pip install -r requirements.txt

      - name: Build frontend
        run: reflex export --frontend-only

      - name: Setup Appwrite CLI
        run: npm install -g appwrite

      - name: Login to Appwrite
        run: |
          appwrite login \
            --endpoint ${{ env.APPWRITE_ENDPOINT }} \
            --project-id ${{ env.APPWRITE_PROJECT_ID }} \
            --key ${{ env.APPWRITE_API_KEY }}

      - name: Deploy to Appwrite Sites
        run: |
          appwrite deploy website \
            --website-id ${{ secrets.APPWRITE_WEBSITE_ID }} \
            --directory .web/_static

  deploy-backend:
    runs-on: ubuntu-latest
    needs: deploy-frontend
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Appwrite CLI
        run: npm install -g appwrite

      - name: Login to Appwrite
        run: |
          appwrite login \
            --endpoint ${{ env.APPWRITE_ENDPOINT }} \
            --project-id ${{ env.APPWRITE_PROJECT_ID }} \
            --key ${{ env.APPWRITE_API_KEY }}

      - name: Deploy backend function
        run: |
          appwrite deploy function \
            --function-id ${{ secrets.APPWRITE_FUNCTION_ID }} \
            --entrypoint "main.py" \
            --code backend/

  deploy-database:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Appwrite CLI
        run: npm install -g appwrite

      - name: Login to Appwrite
        run: |
          appwrite login \
            --endpoint ${{ env.APPWRITE_ENDPOINT }} \
            --project-id ${{ env.APPWRITE_PROJECT_ID }} \
            --key ${{ env.APPWRITE_API_KEY }}

      - name: Deploy database schema
        run: appwrite deploy collection
```

### Separate Workflows (Alternative)
```yaml
# .github/workflows/deploy-frontend.yml
name: Deploy Frontend

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'
      - '.github/workflows/deploy-frontend.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      # Same as frontend steps above
```
```yaml
# .github/workflows/deploy-backend.yml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
      - '.github/workflows/deploy-backend.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      # Same as backend steps above
```

## Environment Configuration

### Environment Variables
```bash
# .env.example
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=main

# Frontend Configuration
FRONTEND_URL=https://your-app.appwrite.site

# Backend Configuration
BACKEND_URL=https://cloud.appwrite.io/v1/functions/your-function-id/execute

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_LOGGING=true
```

### GitHub Secrets Configuration
Required secrets in GitHub repository:
- `APPWRITE_ENDPOINT`
- `APPWRITE_PROJECT_ID`
- `APPWRITE_API_KEY`
- `APPWRITE_WEBSITE_ID`
- `APPWRITE_FUNCTION_ID`

## Custom Domain Setup

### DNS Configuration
```txt
# Add CNAME record in your DNS provider
TYPE    NAME    VALUE
CNAME   @       your-appwrite-site.appwrite.site
CNAME   www     your-appwrite-site.appwrite.site
```

### SSL Certificate
```bash
# Appwrite automatically provisions SSL via Let's Encrypt
# Verify after domain is added in Appwrite Console
```

## Monitoring & Logging

### Function Logs
```bash
# View function logs
appwrite functions list-executions \
  --function-id "$APPWRITE_FUNCTION_ID"

# Get specific execution log
appwrite functions get-execution \
  --function-id "$APPWRITE_FUNCTION_ID" \
  --execution-id "$EXECUTION_ID"
```

### Health Check Endpoint
```python
# backend/main.py
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

### Monitoring Script
```bash
#!/bin/bash
# monitor.sh

HEALTH_URL="https://cloud.appwrite.io/v1/functions/$FUNCTION_ID/execute"

response=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL")

if [ $response -eq 200 ]; then
  echo "✅ Service is healthy"
else
  echo "❌ Service is down (HTTP $response)"
  # Send alert notification
fi
```

## Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Database schema deployed
- [ ] API keys secured
- [ ] CORS settings configured
- [ ] Rate limits set

### Deployment
- [ ] Frontend builds successfully
- [ ] Backend function deploys without errors
- [ ] Database migrations run
- [ ] Health checks passing
- [ ] SSL certificate active

### Post-Deployment
- [ ] Smoke tests passed
- [ ] Monitoring configured
- [ ] Logs accessible
- [ ] Backup strategy in place
- [ ] Rollback plan documented

## Troubleshooting

### Frontend Build Issues
```bash
# Clear Reflex cache
rm -rf .web

# Rebuild
reflex init
reflex export --frontend-only
```

### Function Deployment Issues
```bash
# Check function logs
appwrite functions list-executions --function-id "$FUNCTION_ID"

# Verify runtime compatibility
# Python 3.11 is recommended

# Check requirements.txt dependencies
pip install -r backend/requirements.txt
```

### Database Connection Issues
```python
# Verify credentials in function
import os
print(f"Endpoint: {os.getenv('APPWRITE_ENDPOINT')}")
print(f"Project: {os.getenv('APPWRITE_PROJECT_ID')}")
# Never log API keys!
```

## Task Response Format
```markdown
## TASK COMPLETE: [Task Name]

### Deployment Configuration
[Show appwrite.json or relevant config]

### CI/CD Pipeline
[Describe workflow created]

### Environment Variables
Required variables:
- VAR_NAME: [description]

### Deployment Commands
\`\`\`bash
# Commands to deploy manually
\`\`\`

### Monitoring Setup
- Health check URL: [URL]
- Logs location: [where to find]

### Post-Deployment Verification
- [ ] Frontend accessible at [URL]
- [ ] Backend API responding
- [ ] Database accessible
- [ ] Authentication working

### Rollback Procedure
[Steps to rollback if needed]

### Known Issues
[Any deployment caveats or known issues]

### Next Steps
[What's needed next]
```

## Security Best Practices

- [ ] API keys in environment variables, never in code
- [ ] HTTPS only
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] CORS properly configured
- [ ] Regular security updates
- [ ] Backup strategy implemented
```

---

### Step 3: How to Use This System in Cursor

Now, let me walk you through **how to actually use this**:

#### **Starting a Conversation**

When you start working, Claude should automatically load `.cursorrules`. But you can reinforce context like this:
```
You (in Cursor chat):
"I need to add a user profile feature with avatar upload"
```

Claude should automatically:
1. Read `@.cursor/claude.md` for orchestration
2. Break down the task
3. Reference the relevant agent files
4. Give you a plan

#### **Explicit Agent Invocation**

You can also explicitly call agents:
```
You:
"@ui-specialist design a user profile card component"
```

Or:
```
You:
"@backend-architect create an endpoint for updating user profile"
```

#### **Complex Multi-Agent Tasks**
```
You:
"Create a complete blog post feature with create, read, update, delete functionality"

Claude (Primary Agent) should respond:
"I'll coordinate this feature across multiple specialists:

1. @ui-specialist - Design blog post components
2. @reflex-architect - Implement frontend
3. @appwrite-specialist - Set up posts collection
4. @backend-architect - Create API endpoints  
5. @deployment-engineer - Deploy when ready

Let me start by breaking this down..."
