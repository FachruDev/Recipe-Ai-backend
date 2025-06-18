#!/bin/bash

# Exit on error
set -e

# Check if app name is provided
if [ -z "$1" ]; then
  echo "Usage: ./heroku_deploy.sh <app-name>"
  exit 1
fi

APP_NAME=$1

# Login to Heroku
echo "Logging in to Heroku..."
heroku login

# Create Heroku app if it doesn't exist
if heroku apps:info $APP_NAME &> /dev/null; then
  echo "App $APP_NAME already exists"
else
  echo "Creating app $APP_NAME..."
  heroku create $APP_NAME
fi

# Add PostgreSQL addon
echo "Adding PostgreSQL addon..."
heroku addons:create heroku-postgresql:hobby-dev --app $APP_NAME || echo "PostgreSQL addon already exists"

# Prompt for OpenRouter API key
read -p "Enter your OpenRouter API key: " API_KEY

# Set environment variables
echo "Setting environment variables..."
heroku config:set OPENROUTER_API_KEY=$API_KEY --app $APP_NAME

# Ask for frontend URL
read -p "Enter your frontend URL (or * for all origins): " FRONTEND_URL
FRONTEND_URL=${FRONTEND_URL:-"*"}
heroku config:set CORS_ORIGINS=$FRONTEND_URL --app $APP_NAME

# Deploy to Heroku
echo "Deploying to Heroku..."
git push heroku main || git push heroku master

# Run database migrations
echo "Running database migrations..."
heroku run python -c "from app.db import init_db; init_db()" --app $APP_NAME

echo "Deployment complete! Your app is available at: https://$APP_NAME.herokuapp.com"
echo "API documentation is available at: https://$APP_NAME.herokuapp.com/docs" 