#!/bin/bash
# Run E2E Tests
# Usage: ./scripts/testing/run_e2e_tests.sh [--headed] [--grep pattern]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT/frontend2"

# Check if Playwright is installed
if ! command -v npx playwright &> /dev/null; then
    echo "Installing Playwright..."
    npm install -D @playwright/test
    npx playwright install
fi

# Parse arguments
HEADED=false
GREP=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --headed)
            HEADED=true
            shift
            ;;
        --grep)
            GREP="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Set environment variables
export E2E_BASE_URL="${E2E_BASE_URL:-http://localhost:3000}"
export E2E_API_URL="${E2E_API_URL:-http://localhost:5050}"
export E2E_TEST_EMAIL="${E2E_TEST_EMAIL:-test@example.com}"
export E2E_TEST_PASSWORD="${E2E_TEST_PASSWORD:-TestPassword123!}"

# Build command
CMD="npx playwright test"

if [ "$HEADED" = true ]; then
    CMD="$CMD --headed"
fi

if [ -n "$GREP" ]; then
    CMD="$CMD --grep \"$GREP\""
fi

# Run tests
echo "Running E2E tests..."
echo "Command: $CMD"
eval $CMD

echo "E2E tests completed!"
