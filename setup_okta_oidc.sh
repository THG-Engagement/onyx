#!/bin/bash

# This script sets up the environment variables needed for Okta OIDC integration

# Prompt for Okta domain
read -p "Enter your Okta domain (e.g., dev-123456.okta.com): " OKTA_DOMAIN

# Prompt for Okta client ID
read -p "Enter your Okta client ID: " OKTA_CLIENT_ID

# Prompt for Okta client secret
read -p "Enter your Okta client secret: " OKTA_CLIENT_SECRET

# Generate a random secret for USER_AUTH_SECRET if not provided
read -p "Enter a secret for USER_AUTH_SECRET (leave blank to generate one): " USER_AUTH_SECRET
if [ -z "$USER_AUTH_SECRET" ]; then
    USER_AUTH_SECRET=$(openssl rand -hex 32)
    echo "Generated USER_AUTH_SECRET: $USER_AUTH_SECRET"
fi

# Ask for web domain
read -p "Enter your web domain (default: http://localhost:3000): " WEB_DOMAIN
WEB_DOMAIN=${WEB_DOMAIN:-http://localhost:3000}

# Ask for optional scope override
read -p "Enter optional OIDC scope override (comma-separated, leave blank for default): " OIDC_SCOPE_OVERRIDE

# Create .env file with the necessary variables
cat > deployment/.env << EOF
# Authentication type - set to OIDC
AUTH_TYPE=oidc

# Okta OAuth credentials
OAUTH_CLIENT_ID=$OKTA_CLIENT_ID
OAUTH_CLIENT_SECRET=$OKTA_CLIENT_SECRET

# Okta OpenID configuration URL
OPENID_CONFIG_URL=https://$OKTA_DOMAIN/.well-known/openid-configuration

# User authentication secret
SECRET=$USER_AUTH_SECRET

# Web domain for redirect URLs
WEB_DOMAIN=$WEB_DOMAIN

# Session expiration time (7 days)
SESSION_EXPIRE_TIME_SECONDS=604800

# Database configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

EOF

# Add optional scope override if provided
if [ ! -z "$OIDC_SCOPE_OVERRIDE" ]; then
    echo "# OIDC scope override" >> deployment/.env
    echo "OIDC_SCOPE_OVERRIDE=$OIDC_SCOPE_OVERRIDE" >> deployment/.env
fi

echo "Configuration saved to deployment/.env"
echo "To start Onyx with OIDC authentication, run:"
echo "cd deployment && docker-compose -f docker_compose/docker-compose.prod.yml up -d"