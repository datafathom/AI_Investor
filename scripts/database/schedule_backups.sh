#!/bin/bash
# Scheduled Database Backup Script
# Run this via cron for automated backups

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_ROOT/backups}"
KEEP_DAYS="${BACKUP_KEEP_DAYS:-30}"

# Load environment variables
if [ -f "$PROJECT_ROOT/.env.production" ]; then
    export $(cat "$PROJECT_ROOT/.env.production" | grep -v '^#' | xargs)
fi

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
elif [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

# Run backup
cd "$PROJECT_ROOT"
python "$SCRIPT_DIR/backup.py" \
    --all \
    --backup-dir "$BACKUP_DIR" \
    --pg-host "${POSTGRES_HOST:-localhost}" \
    --pg-port "${POSTGRES_PORT:-5432}" \
    --pg-user "${POSTGRES_USER:-postgres}" \
    --pg-password "${POSTGRES_PASSWORD}" \
    --pg-database "${POSTGRES_DB:-ai_investor}" \
    --neo4j-uri "${NEO4J_URI:-bolt://localhost:7687}" \
    --neo4j-user "${NEO4J_USER:-neo4j}" \
    --neo4j-password "${NEO4J_PASSWORD}"

# Cleanup old backups
python "$SCRIPT_DIR/backup.py" --cleanup "$KEEP_DAYS" --backup-dir "$BACKUP_DIR"

# Optional: Upload to S3 or other cloud storage
if [ -n "$BACKUP_S3_BUCKET" ]; then
    echo "Uploading backups to S3..."
    aws s3 sync "$BACKUP_DIR" "s3://$BACKUP_S3_BUCKET/backups/" --exclude "*.json"
fi

echo "Backup completed: $(date)"
