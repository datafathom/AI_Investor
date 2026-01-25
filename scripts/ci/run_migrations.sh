#!/bin/bash
# CI Migration Runner Script
# Runs database migrations in CI/CD pipeline

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🗄️  Running database migrations..."

# Check if migration script exists
if [ ! -f "scripts/database/migrate.py" ]; then
    echo "❌ Migration script not found"
    exit 1
fi

# Run migrations
python scripts/database/migrate.py up

# Verify migration status
python scripts/database/migrate.py status

echo "✅ Migrations completed successfully"
