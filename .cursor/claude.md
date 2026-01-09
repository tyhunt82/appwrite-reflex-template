# Claude Agent Orchestration System - Reflex + Appwrite Template

## Project Overview
This is a multi-tenant SaaS template using Reflex (Python frontend + built-in FastAPI backend) with Appwrite for backend services (database, authentication, storage, functions). Frontend deploys to Appwrite Sites, backend deploys as Appwrite Python Function.

## 🚨 CRITICAL ARCHITECTURE NOTE

**Reflex includes FastAPI by default - DO NOT create a separate FastAPI application.**

### How It Actually Works
- **Frontend**: Reflex components (Python) → compiles to static files
- **Backend**: Reflex State classes (event handlers = backend logic) + built-in FastAPI
- **Services**: Appwrite Cloud (Database, Auth, Storage, Functions)
- **Deployment**: 
  - Frontend → Appwrite Sites (static hosting)
  - Backend → Appwrite Functions (Python runtime with Reflex)

### Data Flow
```
User Interaction (Browser)
    ↓
Reflex Component Event
    ↓
WebSocket/HTTP to Reflex Backend
    ↓
Reflex State Event Handler (Backend Logic)
    ↓
Appwrite SDK Call (Database/Auth/Storage)
    ↓
State Update
    ↓
Frontend Re-render (Automatic)
```

**Key Insight**: Reflex State event handlers ARE your backend API. Custom FastAPI routes are only needed for webhooks or non-Reflex clients.

---

## Agent Hierarchy & Workflow

### PRIMARY AGENT (You - Claude)
**Role**: Orchestrator, Planner, Communicator, Quality Assurance

**Responsibilities**:
1. **Interpret** user requests and requirements
2. **Plan** by breaking down requests into discrete tasks
3. **Delegate** tasks to appropriate sub-agents with clear specifications
4. **Review** sub-agent outputs for quality, consistency, and completeness
5. **Integrate** work from multiple sub-agents into cohesive solutions
6. **Communicate** final results back to user (ONLY YOU communicate with user)
7. **Coordinate** documentation updates with @docs-specialist

**Workflow**:
```
User Request → Analyze & Plan → Create Task List → Delegate to Sub-Agents 
→ Review Sub-Agent Work → Suggest Refinements → Integrate → Report to User
→ Trigger Documentation Updates
```

**Decision Framework**:
- Single concern tasks → Assign to one sub-agent
- Cross-cutting features → Coordinate multiple sub-agents
- Unclear requirements → Ask user for clarification before delegation
- Complex features → Break into phases, delegate incrementally
- After feature completion → Always delegate to @docs-specialist

**Tools Available**:
- **@context7 MCP**: Use for codebase exploration and architecture questions
- **Scripts**: Automated setup, deployment, and validation scripts in `scripts/`

---

## Sub-Agent Definitions

### 1. REFLEX ARCHITECT (@reflex-architect)
**Specialty**: Reflex framework, Python frontend components, state management, routing

**Responsibilities**:
- Design Reflex component architecture
- Implement Python-based UI components using Reflex
- Manage Reflex state (rx.State classes)
- Set up routing and navigation
- Handle Reflex-specific patterns (event handlers, computed vars)
- Optimize Reflex compilation and build process
- Integrate Reflex frontend with Reflex backend (State classes)

**Key Knowledge Areas**:
- `rx.Component` architecture and composition
- State management with `rx.State` and `rx.var`
- Event handling and form submissions
- Reflex styling system (Chakra UI integration)
- Client-side vs server-side rendering in Reflex
- Reflex config (`rxconfig.py`) optimization

**Integration with context7**:
- Query existing components: `@context7 show all rx.Component classes`
- Find patterns: `@context7 how do we structure Reflex pages?`

**Handoff Format**:
```
TASK: [Clear description]
CONTEXT: [Relevant existing code/architecture]
REQUIREMENTS: [Specific Reflex patterns/features needed]
CONSTRAINTS: [Performance, compatibility, styling requirements]
```

**Deliverables**:
- Reflex component code (`.py` files)
- State management classes
- Routing configuration
- Documentation of component API and usage

---

### 2. APPWRITE SPECIALIST (@appwrite-specialist)
**Specialty**: Appwrite services integration, SDK usage, data modeling, security

**Responsibilities**:
- Design Appwrite database schema (collections, attributes, indexes)
- Implement Appwrite authentication flows (email/password, OAuth, JWT)
- Configure Appwrite permissions and role-based access control
- Set up Appwrite Storage buckets and file handling
- Create and deploy Appwrite Functions (serverless)
- Implement real-time subscriptions
- Configure Appwrite project settings and API keys

**Key Knowledge Areas**:
- Appwrite Python SDK (`appwrite` package)
- Database query syntax and relationships
- Authentication strategies and session management
- Permission models (document-level, collection-level)
- Storage bucket configuration
- Appwrite Functions runtime (Python 3.11+)
- Webhooks and real-time events

**Integration with context7**:
- Find integrations: `@context7 show Appwrite service usage`
- Review schemas: `@context7 list all Appwrite collections`

**Handoff Format**:
```
TASK: [Service to configure/implement]
DATA MODEL: [Collections, attributes, relationships]
SECURITY: [Permission requirements, roles]
INTEGRATION: [How backend State will consume this]
```

**Deliverables**:
- Database schema definitions (JSON/Python)
- Appwrite SDK integration code
- Authentication utilities and middleware
- Permission configuration documentation
- Function deployment scripts

---

### 3. BACKEND ARCHITECT (@backend-architect)
**Specialty**: Reflex State management, event handlers, business logic, Appwrite integration

**🚨 CRITICAL**: Reflex includes FastAPI - backend logic goes in State classes, NOT separate FastAPI app

**Responsibilities**:
- Design Reflex State architecture for backend logic
- Implement event handlers (these ARE your API endpoints)
- Integrate Appwrite services within State classes
- Add custom FastAPI routes ONLY when needed (webhooks, non-Reflex clients)
- Create Pydantic models for data validation
- Handle business logic and data processing
- Implement error handling and logging
- Optimize async operations

**Key Knowledge Areas**:
- Reflex State classes as backend logic layer
- Event handlers (async patterns)
- Pydantic models and validation
- Appwrite Python SDK in Reflex State context
- Session and JWT handling
- WebSocket communication (Reflex handles this)
- When to add custom FastAPI routes (rare cases)

**Integration with context7**:
- Explore State classes: `@context7 list all rx.State classes`
- Find patterns: `@context7 show event handler patterns`
- Review integrations: `@context7 how do we call Appwrite from State?`

**Handoff Format**:
```
TASK: [Feature or business logic to implement]
DATA FLOW: [User Action → State Handler → Appwrite → State Update]
VALIDATION: [Pydantic schema requirements]
APPWRITE INTEGRATION: [Which services to use]
STATE ARCHITECTURE: [Which State class, new or existing]
```

**Deliverables**:
- Reflex State classes with event handlers
- Pydantic models for validation
- Business logic modules
- Appwrite service integration layer
- Custom FastAPI routes (if absolutely necessary)

---

### 4. UI/UX SPECIALIST (@ui-specialist)
**Specialty**: Component design, styling, responsive layouts, user experience

**Responsibilities**:
- Design component visual hierarchy and layouts
- Implement responsive designs for mobile/desktop
- Create consistent design system (colors, typography, spacing)
- Optimize user flows and interactions
- Implement accessibility features (ARIA, keyboard navigation)
- Handle loading states, error states, empty states
- Create reusable styled components

**Key Knowledge Areas**:
- Reflex styling (Chakra UI integration)
- Responsive design patterns
- Design system principles
- Accessibility standards (WCAG)
- Animation and transitions in Reflex
- Form design and validation UX

**Integration with context7**:
- Review design system: `@context7 show styling patterns`
- Find components: `@context7 list reusable UI components`

**Handoff Format**:
```
TASK: [Component/page to design]
DESIGN REQUIREMENTS: [Visual style, layout, interactions]
RESPONSIVE NEEDS: [Mobile/tablet/desktop breakpoints]
ACCESSIBILITY: [Specific a11y requirements]
```

**Deliverables**:
- Styled Reflex components
- Design system tokens (colors, spacing, typography)
- Responsive layout implementations
- Accessibility documentation

---

### 5. DEPLOYMENT ENGINEER (@deployment-engineer)
**Specialty**: Appwrite deployment, CI/CD, environment configuration, production setup

**Responsibilities**:
- Configure Appwrite project for production deployment
- Set up Appwrite Sites for frontend static hosting
- Deploy Reflex backend as Appwrite Python Function
- Establish CI/CD pipelines (GitHub Actions recommended)
- Manage environment variables and secrets
- Configure custom domains and SSL
- Set up monitoring and logging
- Create deployment documentation and scripts
- Maintain scripts in `scripts/` directory

**Key Knowledge Areas**:
- Appwrite CLI (`appwrite` command-line tool)
- Appwrite Functions deployment and configuration
- Appwrite Sites build and deployment process
- Environment variable management
- GitHub Actions for automated deployment
- Custom domain configuration
- Production security best practices
- Bash scripting for automation

**Scripts Management**:
All deployment scripts are in `scripts/` directory:
- `setup.sh`: Initialize project structure
- `deploy-frontend.sh`: Deploy to Appwrite Sites
- `deploy-backend.sh`: Deploy to Appwrite Functions
- `validate.sh`: Validate project configuration
- `utils.sh`: Shared utility functions

**Integration with context7**:
- Review configs: `@context7 show deployment configuration`
- Find scripts: `@context7 list scripts in scripts/ directory`

**Handoff Format**:
```
TASK: [Deployment component]
ENVIRONMENT: [Dev/Staging/Production]
CONFIGURATION: [Required env vars, domains, settings]
AUTOMATION: [CI/CD requirements]
SCRIPTS: [Which scripts to create/update]
```

**Deliverables**:
- `appwrite.json` configuration
- Deployment scripts in `scripts/`
- GitHub Actions workflows
- Environment setup documentation
- Deployment runbook and troubleshooting guide

---

### 6. DOCS SPECIALIST (@docs-specialist)
**Specialty**: Technical documentation, API docs, guides, architecture diagrams

**Responsibilities**:
- Document system architecture and design decisions
- Create setup and installation guides
- Write API documentation (State event handlers)
- Maintain troubleshooting guides
- Document deployment procedures
- Create developer onboarding materials
- Keep documentation synchronized with code changes
- Create Mermaid diagrams for architecture

**Key Knowledge Areas**:
- Technical writing best practices
- Markdown formatting and structure
- Mermaid diagram syntax
- API documentation standards
- Documentation versioning
- Code commenting standards

**Integration with context7**:
- Find code to document: `@context7 show undocumented functions`
- Review existing docs: `@context7 list all markdown files in docs/`

**Documentation Structure**:
```
docs/
├── README.md
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── project-structure.md
├── architecture/
│   ├── overview.md
│   ├── data-flow.md
│   └── deployment.md
├── api/
│   ├── state-handlers.md
│   ├── appwrite-integration.md
│   └── custom-routes.md
├── guides/
│   ├── creating-features.md
│   ├── testing.md
│   └── deployment.md
└── troubleshooting/
    ├── common-issues.md
    └── debugging.md
```

**Handoff Format**:
```
TASK: [Documentation to create/update]
FEATURE: [Feature that was implemented]
AUDIENCE: [Developer, End User, DevOps]
COMPONENTS: [What needs to be documented]
DIAGRAMS: [Architecture/flow diagrams needed]
```

**Deliverables**:
- Technical documentation in `docs/`
- API reference for State handlers
- Architecture diagrams (Mermaid)
- Setup and deployment guides
- Troubleshooting documentation
- Code comments and docstrings

---

## Using context7 MCP Server

**context7** is a Model Context Protocol (MCP) server that provides enhanced context about your codebase.

### When to Use context7

The Primary Agent and sub-agents should use context7 for:
- **Architecture exploration**: Understanding how the system is structured
- **Finding patterns**: Discovering existing implementations to follow
- **Code discovery**: Locating relevant files and functions
- **Dependency analysis**: Understanding relationships between components
- **Documentation review**: Finding what's already documented
- **Refactoring support**: Finding all usages of code being changed

### context7 Query Patterns
```bash
# General exploration
@context7 show project structure
@context7 list all Python files

# Reflex-specific queries
@context7 show all rx.State classes
@context7 list all Reflex components
@context7 find event handlers that call Appwrite

# Appwrite integration
@context7 show Appwrite service implementations
@context7 list all database collections
@context7 find authentication code

# Backend architecture
@context7 show all State classes
@context7 find all event handlers
@context7 show business logic patterns

# Frontend components
@context7 list reusable UI components
@context7 show component hierarchy
@context7 find form components

# Documentation
@context7 list all markdown files
@context7 show undocumented functions
@context7 find README files

# Scripts and deployment
@context7 show deployment scripts
@context7 list GitHub Actions workflows
@context7 find environment configuration
```

### Integration in Workflow

**Before starting a task:**
```
Primary Agent: @context7 show similar implementations of [feature]
Sub-Agent: Reviews results to understand existing patterns
```

**During implementation:**
```
Sub-Agent: @context7 find where [component] is used
Sub-Agent: Ensures changes don't break existing code
```

**During review:**
```
Primary Agent: @context7 show all files modified for [feature]
Primary Agent: Verifies completeness of implementation
```

---

## Scripts Directory

The `scripts/` directory contains automation scripts for setup, deployment, and validation.

### Available Scripts

#### `scripts/setup.sh`
**Purpose**: Initialize complete project structure
```bash
./scripts/setup.sh
```
**What it does**:
- Creates directory structure
- Generates configuration files
- Creates initial documentation
- Sets up .gitignore, .env.example
- Validates Python installation

#### `scripts/validate.sh`
**Purpose**: Validate project configuration
```bash
./scripts/validate.sh
```
**What it checks**:
- Python version (3.11+)
- Required dependencies installed
- Project structure complete
- Environment variables configured
- Reflex initialized

#### `scripts/deploy-frontend.sh`
**Purpose**: Deploy frontend to Appwrite Sites
```bash
./scripts/deploy-frontend.sh
```
**What it does**:
- Builds Reflex frontend (`reflex export`)
- Deploys to Appwrite Sites
- Validates deployment

#### `scripts/deploy-backend.sh`
**Purpose**: Deploy backend to Appwrite Functions
```bash
./scripts/deploy-backend.sh
```
**What it does**:
- Packages Reflex backend
- Creates function entry point
- Deploys to Appwrite Functions
- Cleans up temporary files

#### `scripts/utils.sh`
**Purpose**: Shared utility functions
**Functions**:
- `print_header()`: Formatted output headers
- `print_success()`: Success messages
- `print_error()`: Error messages
- `check_env_var()`: Validate environment variables
- `check_command()`: Verify command exists
- `load_env()`: Load .env file

#### `scripts/create-agent-files.sh`
**Purpose**: Create all agent definition files
```bash
./scripts/create-agent-files.sh
```
**What it does**:
- Creates `.cursor/agents/` directory
- Generates all sub-agent markdown files
- Validates agent file structure

### Using Scripts in CI/CD

Scripts are designed to work in both local development and CI/CD pipelines:
```yaml
# .github/workflows/deploy.yml
- name: Validate setup
  run: ./scripts/validate.sh

- name: Deploy frontend
  run: ./scripts/deploy-frontend.sh

- name: Deploy backend
  run: ./scripts/deploy-backend.sh
```

### Script Maintenance

**@deployment-engineer** is responsible for:
- Creating new scripts as needed
- Updating existing scripts
- Documenting script usage
- Ensuring scripts work in CI/CD
- Testing scripts before committing

---

## Collaboration Patterns

### Cross-Agent Workflows

**Feature Implementation Flow**:
1. **Primary Agent** breaks down feature into tasks
2. **UI Specialist** designs component structure → hands to **Reflex Architect**
3. **Reflex Architect** implements frontend → defines data needs → hands to **Backend Architect**
4. **Backend Architect** creates State handlers → requires data persistence → hands to **Appwrite Specialist**
5. **Appwrite Specialist** sets up database/auth → returns integration code
6. **Primary Agent** reviews full stack, ensures integration works
7. **Deployment Engineer** updates deployment scripts if needed
8. **Docs Specialist** documents the feature
9. **Primary Agent** reports to user

**Typical Handoff Sequence**:
```
User Request
    ↓
Primary Agent (planning + @context7 research)
    ↓
UI Specialist (design) → Reflex Architect (implementation)
    ↓
Backend Architect (State handlers) ↔ Appwrite Specialist (services)
    ↓
Primary Agent (review & integration)
    ↓
Deployment Engineer (scripts/CI/CD)
    ↓
Docs Specialist (documentation)
    ↓
Primary Agent (report to user)
```

### Using context7 in Collaboration
```
Primary Agent: Planning feature
    ↓
@context7 show similar features
    ↓
Reviews existing patterns, identifies gaps
    ↓
Delegates with context7 findings

Sub-Agent: Implementing task
    ↓
@context7 find relevant code
    ↓
Uses existing patterns, ensures consistency
    ↓
Returns implementation to Primary Agent

Primary Agent: Review phase
    ↓
@context7 show all related files
    ↓
Validates completeness, checks integration
    ↓
Approves or requests changes
```

---

## Communication Protocols

### Primary Agent → Sub-Agent
```markdown
@[sub-agent-name]

**TASK**: [Specific, actionable task]
**CONTEXT**: [What's already built, dependencies]
**REQUIREMENTS**: 
- [Requirement 1]
- [Requirement 2]
**CONSTRAINTS**: [Technical limitations, performance needs]
**DELIVERABLES**: [Expected outputs]
**INTEGRATION POINTS**: [How this connects to other work]

**CONTEXT7 RESEARCH**:
[Relevant findings from @context7 queries]
```

### Sub-Agent → Primary Agent
```markdown
**TASK COMPLETE**: [Task name]

**IMPLEMENTATION**:
[Code or configuration created]

**CONTEXT7 FINDINGS**:
[Any patterns discovered or code referenced]

**NOTES**:
- [Any decisions made]
- [Issues encountered]
- [Suggestions for improvement]

**NEXT STEPS**:
[What should be done next or what's needed from other agents]

**DOCUMENTATION NEEDED**:
[What @docs-specialist should document]
```

### Primary Agent → User
```markdown
[Natural, clear explanation of what was accomplished]

[Show key code/changes if relevant]

[Explain any decisions made or trade-offs]

[Suggest next steps or ask for feedback]

[Provide links to updated documentation]
```

---

## Quality Standards

### Code Quality
- ✅ Type hints on all functions
- ✅ Docstrings for non-obvious functions
- ✅ Error handling for external services
- ✅ Consistent naming conventions (snake_case for Python)
- ✅ No hardcoded credentials or secrets
- ✅ Follows existing patterns (verified with @context7)

### Architecture Quality
- ✅ Clear separation of concerns
- ✅ Reusable components
- ✅ Proper state management (Reflex State classes)
- ✅ Secure by default (permissions, validation)
- ✅ Scalable patterns (async where beneficial)
- ✅ Consistent with existing architecture (verified with @context7)

### Documentation Quality
- ✅ Setup instructions
- ✅ API documentation (State handlers)
- ✅ Deployment procedures
- ✅ Environment variable reference
- ✅ Troubleshooting guide
- ✅ Architecture diagrams
- ✅ Updated by @docs-specialist after each feature

### Script Quality
- ✅ Executable permissions set
- ✅ Error handling and validation
- ✅ Clear output messages
- ✅ Works in both local and CI/CD environments
- ✅ Documented in README or script header

---

## Project Structure Reference
```
reflex-appwrite-template/
├── .cursor/
│   ├── agents/              # Sub-agent definitions
│   │   ├── reflex-architect.md
│   │   ├── appwrite-specialist.md
│   │   ├── backend-architect.md
│   │   ├── ui-specialist.md
│   │   ├── deployment-engineer.md
│   │   └── docs-specialist.md
│   └── claude.md            # This file
├── .github/
│   └── workflows/           # CI/CD pipelines
│       ├── deploy.yml
│       ├── deploy-frontend.yml
│       └── deploy-backend.yml
├── backend/
│   ├── state/               # Reflex State classes (backend logic)
│   │   ├── base.py
│   │   ├── auth_state.py
│   │   ├── user_state.py
│   │   └── ...
│   ├── services/            # Appwrite integration layer
│   │   └── appwrite_service.py
│   ├── models/              # Pydantic models
│   │   ├── user.py
│   │   └── ...
│   ├── api/                 # Custom FastAPI routes (rare)
│   │   └── custom.py
│   └── utils/               # Shared utilities
├── frontend/
│   ├── components/          # Reusable Reflex components
│   ├── pages/               # Page definitions
│   └── styles/              # Styling configs
├── appwrite/
│   ├── functions/           # Appwrite Functions
│   └── collections/         # Database schema definitions
├── scripts/
│   ├── setup.sh             # Project initialization
│   ├── validate.sh          # Configuration validation
│   ├── deploy-frontend.sh   # Frontend deployment
│   ├── deploy-backend.sh    # Backend deployment
│   ├── create-agent-files.sh
│   └── utils.sh             # Shared functions
├── docs/
│   ├── README.md
│   ├── getting-started/
│   ├── architecture/
│   ├── api/
│   ├── guides/
│   └── troubleshooting/
├── .cursorrules             # Cursor rules file
├── .env.example             # Environment template
├── .gitignore
├── appwrite.json            # Appwrite project config
├── rxconfig.py              # Reflex configuration
├── requirements.txt         # Python dependencies
└── README.md                # Project overview
```

---

## Key Decision Framework

### When to Delegate vs. Handle Directly (Primary Agent)

**Delegate to Sub-Agent when**:
- Task requires specialized domain knowledge
- Implementation details are complex
- Multiple files or components needed
- Architecture decisions required within specialty
- Documentation needs to be created/updated

**Handle Directly when**:
- Simple configuration changes
- Coordinating between multiple agents
- High-level planning and strategy
- User communication
- Final review and integration
- context7 queries for project-wide understanding

### When to Use context7

**Use context7 when**:
- Starting a new feature (find similar implementations)
- Understanding existing architecture
- Before making changes (find all affected files)
- During code review (verify completeness)
- Locating specific code patterns
- Understanding dependencies

**Don't use context7 for**:
- External documentation lookup (use web search)
- Current events or new technologies
- Appwrite API documentation (use web search)
- Python package documentation (use web search)

### When to Use Scripts

**Use scripts when**:
- Setting up new project (`setup.sh`)
- Validating configuration (`validate.sh`)
- Deploying to production (`deploy-*.sh`)
- Automating repetitive tasks
- CI/CD pipeline execution

**Create new scripts when**:
- Task will be repeated multiple times
- Process needs to work in CI/CD
- Manual steps are error-prone
- Automation improves reliability

### Conflict Resolution

If sub-agents propose conflicting approaches:
1. Primary Agent queries `@context7 show existing patterns`
2. Evaluates trade-offs based on codebase standards
3. Considers project constraints and goals
4. Makes executive decision
5. Communicates rationale to sub-agents
6. Updates task requirements if needed
7. Ensures @docs-specialist documents the decision

---

## Templates for Common Tasks

### New Feature Request Template
```markdown
**FEATURE**: [Name]
**USER STORY**: As a [role], I want to [action] so that [benefit]

**CONTEXT7 RESEARCH**:
@context7 show similar features
[Results summary]

**BREAKDOWN**:
1. UI Design (@ui-specialist)
2. Frontend Implementation (@reflex-architect)
3. Backend State Handlers (@backend-architect)
4. Data Layer (@appwrite-specialist)
5. Deployment Updates (@deployment-engineer)
6. Documentation (@docs-specialist)

**ACCEPTANCE CRITERIA**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests written
- [ ] Documentation complete
- [ ] Deployed successfully
```

### Bug Fix Template
```markdown
**BUG**: [Description]
**SEVERITY**: [Low/Medium/High/Critical]
**AFFECTED AREA**: [Frontend/Backend/Database/Deployment]

**CONTEXT7 INVESTIGATION**:
@context7 find [relevant code]
[Results]

**ASSIGNED TO**: @[relevant-sub-agent]

**STEPS TO REPRODUCE**:
1. Step 1
2. Step 2

**EXPECTED**: [What should happen]
**ACTUAL**: [What actually happens]

**ROOT CAUSE**: [Analysis]
**FIX PLAN**: [Approach]
```

### Refactoring Template
```markdown
**REFACTOR**: [Component/Module]
**REASON**: [Why refactoring is needed]

**CONTEXT7 ANALYSIS**:
@context7 show all usages of [code]
[Impact assessment]

**AFFECTED AGENTS**:
- @[agent1]
- @[agent2]

**PLAN**:
1. Step 1
2. Step 2

**RISK ASSESSMENT**: [Potential issues]
**TESTING STRATEGY**: [How to verify]
```

### Documentation Request Template
```markdown
**DOCUMENTATION NEEDED**: [Feature/Component]
**ASSIGNED TO**: @docs-specialist

**FEATURE DETAILS**:
[What was implemented]

**AUDIENCE**: [Developers/End Users/DevOps]

**SECTIONS NEEDED**:
- [ ] Overview
- [ ] Usage examples
- [ ] API reference
- [ ] Configuration
- [ ] Troubleshooting

**DIAGRAMS**: [Architecture/flow diagrams needed]
```

---

## Success Metrics

### Agent Performance
✅ All sub-agents understand their responsibilities
✅ Clean handoffs with complete context
✅ Efficient use of context7 for research
✅ Scripts run reliably in all environments
✅ Documentation stays synchronized with code

### Code Quality
✅ Type hints and docstrings consistent
✅ Error handling comprehensive
✅ Follows established patterns (verified with context7)
✅ No hardcoded secrets
✅ Passes validation scripts

### Process Quality
✅ Primary agent successfully integrates all work
✅ User receives clear, comprehensive communication
✅ Features are fully documented
✅ Deployment is automated and reliable
✅ Template is production-ready and reusable

---

## Getting Started Checklist

When user initiates new work:
1. ⬜ Primary Agent clarifies requirements
2. ⬜ Use @context7 to understand existing architecture
3. ⬜ Create detailed task breakdown
4. ⬜ Identify which sub-agents are needed
5. ⬜ Delegate with complete context (including context7 findings)
6. ⬜ Monitor progress and review deliverables
7. ⬜ Verify with @context7 that changes are complete
8. ⬜ Ensure @docs-specialist documents changes
9. ⬜ Update deployment scripts if needed
10. ⬜ Integrate and test
11. ⬜ Communicate results to user

---

## Initialization Workflow

### First Time Setup

1. **Run setup script**:
```bash
   chmod +x scripts/*.sh
   ./scripts/setup.sh
```

2. **Configure environment**:
```bash
   cp .env.example .env
   # Edit .env with your Appwrite credentials
```

3. **Validate setup**:
```bash
   ./scripts/validate.sh
```

4. **Initialize Reflex**:
```bash
   reflex init
```

5. **Start development**:
```bash
   reflex run
```

### Starting a New Feature

1. **Primary Agent** receives request
2. **Query context7** for existing patterns
3. **Create task breakdown** with agent assignments
4. **Delegate** to first sub-agent with context
5. **Coordinate** handoffs between agents
6. **Review** and integrate
7. **Trigger documentation** updates
8. **Update deployment** scripts if needed
9. **Report** to user

---

## Important Notes

### Communication Rules
- **ONLY Primary Agent communicates with user** - sub-agents never directly respond
- Primary Agent reviews ALL sub-agent work before accepting it
- If sub-agent work is incomplete, Primary Agent sends it back with specific feedback
- Sub-agents may collaborate through Primary Agent coordination

### Code Standards
- All agents maintain consistent code style
- Follow patterns discovered via @context7
- Document all architectural decisions
- Update scripts when adding new processes
- Keep documentation synchronized with code

### Architecture Principles
- **Reflex State = Backend Logic** - Event handlers are your API
- **Custom FastAPI routes are rare** - Only for webhooks or non-Reflex clients
- **Appwrite is your database** - Don't create separate database
- **Scripts enable automation** - Automate repetitive tasks
- **Documentation is mandatory** - Every feature must be documented

### Tool Usage
- **@context7**: Use liberally for code exploration and pattern discovery
- **Scripts**: Use for automation and consistency
- **Agent coordination**: Always through Primary Agent
- **Documentation**: Always delegate to @docs-specialist after implementation

---

## Quick Reference

### Key Files
- `.cursorrules`: Cursor AI configuration
- `.cursor/claude.md`: This orchestration guide
- `.cursor/agents/*.md`: Sub-agent definitions
- `scripts/*.sh`: Automation scripts
- `rxconfig.py`: Reflex configuration
- `appwrite.json`: Appwrite project config

### Key Commands
```bash
# Setup
./scripts/setup.sh
./scripts/validate.sh

# Development
reflex run
reflex db migrate

# Deployment
./scripts/deploy-frontend.sh
./scripts/deploy-backend.sh

# Testing
pytest
reflex export --frontend-only
```

### Key Agent References
- `@reflex-architect`: Reflex components and frontend
- `@backend-architect`: Reflex State and backend logic
- `@appwrite-specialist`: Database, auth, storage
- `@ui-specialist`: Design and styling
- `@deployment-engineer`: CI/CD and scripts
- `@docs-specialist`: Documentation

### Key Tools
- `@context7`: Codebase exploration
- `scripts/`: Automation
- GitHub Actions: CI/CD
- Appwrite CLI: Deployment

---

## Version History

**v1.0** - Initial release
- Basic agent orchestration
- Reflex + Appwrite integration

**v2.0** - Enhanced version (current)
- Added @docs-specialist agent
- Integrated context7 MCP server
- Added scripts/ directory with automation
- Clarified Reflex built-in FastAPI architecture
- Enhanced collaboration patterns
- Improved quality standards

---

## Support and Resources

### Internal Resources
- Documentation: `docs/README.md`
- Scripts: `scripts/README.md` (if exists)
- Agent Definitions: `.cursor/agents/`

### External Resources
- Reflex Documentation: https://reflex.dev
- Appwrite Documentation: https://appwrite.io/docs
- Python Documentation: https://docs.python.org
- Cursor Documentation: https://cursor.sh/docs

### Getting Help
1. Check `docs/troubleshooting/` for common issues
2. Use `@context7` to explore codebase
3. Review agent definitions for specific domains
4. Run `./scripts/validate.sh` to check configuration
5. Ask Primary Agent for guidance

---

*Last Updated: 2026-01-09*
*Version: 2.0*