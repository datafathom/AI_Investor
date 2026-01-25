#!/bin/bash
# CI Health Check Script
# Verifies services are healthy after deployment

set -e

HEALTH_URL=${1:-"http://localhost/health"}
MAX_RETRIES=${2:-30}
RETRY_INTERVAL=${3:-2}

echo "🏥 Running health check on: $HEALTH_URL"

RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f "$HEALTH_URL" > /dev/null 2>&1; then
        echo "✅ Health check passed"
        exit 0
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "⏳ Health check attempt $RETRY_COUNT/$MAX_RETRIES..."
    sleep $RETRY_INTERVAL
done

echo "❌ Health check failed after $MAX_RETRIES attempts"
exit 1
