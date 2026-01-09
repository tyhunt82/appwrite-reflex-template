#!/bin/bash
# validate.sh - Validate project setup and configuration
# TODO: Ensure using uv not just pip

set -e

source "$(dirname "$0")/utils.sh"

print_header "Validating Project Setup"

# Check required commands
print_step "Checking required tools..."

check_command "python3" "brew install python3 (macOS) or apt install python3 (Linux)"
check_command "pip" "python3 -m ensurepip"
check_command "git" "brew install git (macOS) or apt install git (Linux)"

print_success "All required tools are installed"

# Check Python version
print_step "Checking Python version..."
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    print_error "Python 3.11+ required, found $PYTHON_VERSION"
    exit 1
fi

print_success "Python version OK: $PYTHON_VERSION"

# Check if virtual environment exists
print_step "Checking for virtual environment..."
if [ -d "venv" ] || [ -d ".venv" ] || [ -n "$VIRTUAL_ENV" ]; then
    print_success "Virtual environment found"
else
    print_warning "No virtual environment found"
    print_info "Consider creating one: python3 -m venv venv"
fi

# Check if dependencies are installed
print_step "Checking Python dependencies..."
if pip show reflex >/dev/null 2>&1; then
    REFLEX_VERSION=$(pip show reflex | grep Version | cut -d' ' -f2)
    print_success "Reflex installed: $REFLEX_VERSION"
else
    print_error "Reflex not installed"
    print_info "Install with: pip install -r requirements.txt"
    exit 1
fi

if pip show appwrite >/dev/null 2>&1; then
    APPWRITE_VERSION=$(pip show appwrite | grep Version | cut -d' ' -f2)
    print_success "Appwrite SDK installed: $APPWRITE_VERSION"
else
    print_warning "Appwrite SDK not installed"
fi

# Check project structure
print_step "Validating project structure..."

REQUIRED_DIRS=(
    ".cursor"
    ".cursor/agents"
    "frontend"
    "backend"
    "appwrite"
    "scripts"
    "docs"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_success "Directory exists: $dir"
    else
        print_error "Missing directory: $dir"
    fi
done

# Check required files
print_step "Checking required files..."

REQUIRED_FILES=(
    ".cursorrules"
    ".cursor/claude.md"
    "rxconfig.py"
    "requirements.txt"
    "README.md"
    ".gitignore"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "File exists: $file"
    else
        print_error "Missing file: $file"
    fi
done

# Check .env file
print_step "Checking environment configuration..."

if [ -f ".env" ]; then
    print_success ".env file exists"
    
    # Check for required variables
    source .env
    
    REQUIRED_VARS=(
        "APPWRITE_ENDPOINT"
        "APPWRITE_PROJECT_ID"
    )
    
    for var in "${REQUIRED_VARS[@]}"; do
        if [ -n "${!var}" ]; then
            print_success "$var is set"
        else
            print_warning "$var is not set in .env"
        fi
    done
else
    print_warning ".env file not found"
    print_info "Copy .env.example to .env and configure it"
fi

# Check if Reflex is initialized
print_step "Checking Reflex initialization..."

if [ -d ".web" ]; then
    print_success "Reflex initialized"
else
    print_warning "Reflex not initialized"
    print_info "Run: reflex init"
fi

# Summary
echo ""
print_header "Validation Complete"

if [ -f ".env" ] && [ -d ".web" ]; then
    print_success "Project setup looks good!"
    echo ""
    print_info "Next steps:"
    echo "  1. Ensure all environment variables in .env are configured"
    echo "  2. Run: reflex run"
    echo "  3. Visit: http://localhost:3000"
else
    print_warning "Setup is incomplete"
    echo ""
    print_info "Complete setup:"
    [ ! -f ".env" ] && echo "  1. Copy .env.example to .env and configure"
    [ ! -d ".web" ] && echo "  2. Run: reflex init"
    echo "  3. Then run: reflex run"
fi