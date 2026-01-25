#!/bin/bash
# Run Load Tests using k6
# Usage: ./scripts/testing/run_load_tests.sh [scenario]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
    echo "k6 is not installed. Installing..."
    # Install k6 (adjust for your OS)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo gpg -k
        sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E8915D6B6A4C5D5D5D5D5D5D5D5D5D
        echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
        sudo apt-get update
        sudo apt-get install k6
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install k6
    else
        echo "Please install k6 manually from https://k6.io/docs/getting-started/installation/"
        exit 1
    fi
fi

# Set environment variables
export API_URL="${API_URL:-http://localhost:5050}"
export TEST_EMAIL="${TEST_EMAIL:-loadtest@example.com}"
export TEST_PASSWORD="${TEST_PASSWORD:-TestPassword123!}"

# Select scenario
SCENARIO="${1:-load_test_scenarios}"

echo "Running load test: $SCENARIO"
echo "API URL: $API_URL"

# Run k6 test
k6 run "tests/load/${SCENARIO}.js" \
    --out json=test-results/load-test-results.json \
    --out csv=test-results/load-test-results.csv

echo "Load test completed! Results saved to test-results/"
