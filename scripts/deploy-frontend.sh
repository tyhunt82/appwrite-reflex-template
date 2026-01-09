#!/bin/bash
# deploy-frontend.sh - Deploy Reflex frontend to Appwrite Sites

set -e

source "$(dirname "$0")/utils.sh"

print_header "Deploying Frontend to Appwrite Sites"

# Check if environment variables are set
check_env_var "APPWRITE_ENDPOINT"
check_env_var "APPWRITE_PROJECT_ID"
check_env_var "APPWRITE_WEBSITE_ID"

# Build frontend
print_step "Building Reflex frontend..."
reflex export --frontend-only

if [ ! -d ".web/_static" ]; then
    print_error "Build failed: .web/_static directory not found"
    exit 1
fi

print_success "Frontend built successfully"

# Deploy to Appwrite Sites
print_step "Deploying to Appwrite Sites..."

appwrite deploy website \
    --website-id "$APPWRITE_WEBSITE_ID" \
    --directory .web/_static

print_success "Frontend deployed successfully!"
print_info "Visit your Appwrite console to see the deployment"