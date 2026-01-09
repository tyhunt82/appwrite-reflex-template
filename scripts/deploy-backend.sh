#!/bin/bash
# deploy-backend.sh - Deploy Reflex backend to Appwrite Functions

set -e

source "$(dirname "$0")/utils.sh"

print_header "Deploying Backend to Appwrite Functions"

# Check environment variables
check_env_var "APPWRITE_ENDPOINT"
check_env_var "APPWRITE_PROJECT_ID"
check_env_var "APPWRITE_FUNCTION_ID"

# Create deployment package
print_step "Preparing backend for deployment..."

# Create temporary deployment directory
DEPLOY_DIR=$(mktemp -d)
print_info "Using temporary directory: $DEPLOY_DIR"

# Copy backend files
cp -r backend/* "$DEPLOY_DIR/"
cp requirements.txt "$DEPLOY_DIR/"
cp rxconfig.py "$DEPLOY_DIR/" 2>/dev/null || true

# Create function entry point
cat > "$DEPLOY_DIR/main.py" << 'EOF'
"""Appwrite Function entry point for Reflex backend."""
import os
from reflex.app import app

def main(req, res):
    """Appwrite Function handler."""
    # Reflex app is available as 'app'
    return res.json({"status": "healthy"})
EOF

print_success "Backend package prepared"

# Deploy to Appwrite Functions
print_step "Deploying to Appwrite Functions..."

appwrite deploy function \
    --function-id "$APPWRITE_FUNCTION_ID" \
    --entrypoint "main.py" \
    --code "$DEPLOY_DIR"

# Cleanup
rm -rf "$DEPLOY_DIR"

print_success "Backend deployed successfully!"
print_info "Function ID: $APPWRITE_FUNCTION_ID"