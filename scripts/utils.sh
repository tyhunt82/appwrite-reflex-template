#!/bin/bash
# utils.sh - Utility functions for scripts

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if environment variable is set
check_env_var() {
    if [ -z "${!1}" ]; then
        print_error "Environment variable $1 is not set"
        echo "Please set it in your .env file or export it"
        exit 1
    fi
}

# Load .env file if it exists
load_env() {
    if [ -f .env ]; then
        print_info "Loading environment variables from .env"
        export $(cat .env | grep -v '^#' | xargs)
    else
        print_warning ".env file not found"
    fi
}

# Check if command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_error "$1 is not installed"
        if [ -n "$2" ]; then
            echo "Install it with: $2"
        fi
        exit 1
    fi
}