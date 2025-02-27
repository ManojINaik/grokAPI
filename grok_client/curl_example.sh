#!/bin/bash

# Load environment variables from .env file
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
    echo "Environment variables loaded from .env file"
else
    echo "Warning: .env file not found"
    exit 1
fi

# Check if SSO tokens are available
if [ -z "$GROK_SSO" ] || [ -z "$GROK_SSO_RW" ]; then
    echo "Error: SSO tokens not found in environment variables."
    echo "Please make sure GROK_SSO and GROK_SSO_RW are set in your .env file."
    exit 1
fi

# Set API configuration from environment variables
API_HOST=${API_HOST:-127.0.0.1}
API_PORT=${API_PORT:-8000}
MODEL_NAME=${MODEL_NAME:-grok-3}

# Get user input
echo "=== Grok API Curl Example ==="
echo "API Server: http://${API_HOST}:${API_PORT}"
echo "Model: ${MODEL_NAME}"
echo 

read -p "Enter your question for Grok: " USER_QUERY

read -p "Do you want a streaming response? (y/n): " STREAM_RESPONSE

# Format the request body
if [ "$STREAM_RESPONSE" = "y" ]; then
    REQUEST_BODY='{"model":"'"$MODEL_NAME"'","messages":[{"role":"user","content":"'"$USER_QUERY"'"}],"stream":true}'
    echo "Sending streaming request to Grok API..."
else
    REQUEST_BODY='{"model":"'"$MODEL_NAME"'","messages":[{"role":"user","content":"'"$USER_QUERY"'"}]}'
    echo "Sending request to Grok API..."
fi

# Make the API call
curl -X POST "http://${API_HOST}:${API_PORT}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Cookie: sso=${GROK_SSO}; sso-rw=${GROK_SSO_RW}" \
  -d "$REQUEST_BODY"

echo ""
