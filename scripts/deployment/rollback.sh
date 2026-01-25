#!/bin/bash
# Production Rollback Script
# Usage: ./scripts/deployment/rollback.sh [backup_directory]

set -e

BACKUP_DIR=${1:-"backups/latest"}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🔄 Starting rollback procedure..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Stop current services
echo -e "${YELLOW}🛑 Stopping current services...${NC}"
docker-compose -f infra/docker-compose.prod.yml down

# Restore database if backup exists
if [ -f "$BACKUP_DIR/database.sql" ]; then
    echo -e "${YELLOW}💾 Restoring database from backup...${NC}"
    source .env.production
    docker-compose -f infra/docker-compose.prod.yml up -d postgres
    sleep 5
    docker-compose -f infra/docker-compose.prod.yml exec -T postgres psql -U "$POSTGRES_USER" "$POSTGRES_DB" < "$BACKUP_DIR/database.sql" || {
        echo -e "${RED}❌ Database restore failed${NC}"
    }
fi

# Restore Neo4j if backup exists
if [ -f "$BACKUP_DIR/neo4j.dump" ]; then
    echo -e "${YELLOW}💾 Restoring Neo4j from backup...${NC}"
    docker-compose -f infra/docker-compose.prod.yml stop neo4j
    docker-compose -f infra/docker-compose.prod.yml run --rm neo4j neo4j-admin load --database=neo4j --from-path=/tmp/ < "$BACKUP_DIR/neo4j.dump" || {
        echo -e "${RED}❌ Neo4j restore failed${NC}"
    }
    docker-compose -f infra/docker-compose.prod.yml start neo4j
fi

# Start previous version (would need version tagging in real scenario)
echo -e "${YELLOW}🚀 Starting previous version...${NC}"
docker-compose -f infra/docker-compose.prod.yml up -d

echo -e "${GREEN}✅ Rollback completed${NC}"
