#!/bin/bash
# Production Deployment Script
# Usage: ./scripts/deployment/prod_deploy.sh [environment]

set -e  # Exit on error

ENVIRONMENT=${1:-production}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🚀 Starting production deployment for environment: $ENVIRONMENT"
echo "📁 Project root: $PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running${NC}"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed${NC}"
    exit 1
fi

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo -e "${RED}❌ .env.production file not found${NC}"
    echo -e "${YELLOW}💡 Copy .env.production.template to .env.production and fill in values${NC}"
    exit 1
fi

# Validate environment variables
echo -e "${YELLOW}🔍 Validating environment variables...${NC}"
source .env.production

REQUIRED_VARS=(
    "POSTGRES_PASSWORD"
    "NEO4J_PASSWORD"
    "REDIS_PASSWORD"
    "JWT_SECRET"
    "SECRET_KEY"
    "ENCRYPTION_MASTER_KEY"
    "DOMAIN"
)

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ] || [[ "${!var}" == *"CHANGE_ME"* ]]; then
        echo -e "${RED}❌ Required environment variable $var is not set or contains placeholder${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Backup current deployment (if exists)
if docker-compose -f infra/docker-compose.prod.yml ps | grep -q "Up"; then
    echo -e "${YELLOW}💾 Creating backup of current deployment...${NC}"
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    docker-compose -f infra/docker-compose.prod.yml exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_DIR/database.sql" || true
    
    # Backup Neo4j
    docker-compose -f infra/docker-compose.prod.yml exec -T neo4j neo4j-admin dump --database=neo4j --to-path=/tmp/ > "$BACKUP_DIR/neo4j.dump" || true
    
    echo -e "${GREEN}✅ Backup created: $BACKUP_DIR${NC}"
fi

# Pull latest code (if in git repo)
if [ -d ".git" ]; then
    echo -e "${YELLOW}📥 Pulling latest code...${NC}"
    git pull origin main || echo "⚠️  Git pull failed, continuing with local code"
fi

# Build images
echo -e "${YELLOW}🔨 Building Docker images...${NC}"
docker-compose -f infra/docker-compose.prod.yml build --no-cache

# Run database migrations
echo -e "${YELLOW}🗄️  Running database migrations...${NC}"
docker-compose -f infra/docker-compose.prod.yml run --rm backend python scripts/database/migrate.py up || {
    echo -e "${RED}❌ Migration failed${NC}"
    exit 1
}

# Start services with zero-downtime deployment
echo -e "${YELLOW}🚀 Starting services...${NC}"

# Start infrastructure services first
docker-compose -f infra/docker-compose.prod.yml up -d postgres neo4j redis zookeeper kafka

# Wait for infrastructure to be healthy
echo -e "${YELLOW}⏳ Waiting for infrastructure to be healthy...${NC}"
sleep 10

# Start application services
docker-compose -f infra/docker-compose.prod.yml up -d backend frontend traefik

# Wait for services to be healthy
echo -e "${YELLOW}⏳ Waiting for services to be healthy...${NC}"
sleep 20

# Health check
echo -e "${YELLOW}🏥 Running health checks...${NC}"
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Health check passed${NC}"
        break
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -e "${YELLOW}⏳ Health check attempt $RETRY_COUNT/$MAX_RETRIES...${NC}"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}❌ Health check failed after $MAX_RETRIES attempts${NC}"
    echo -e "${YELLOW}🔄 Rolling back...${NC}"
    ./scripts/deployment/rollback.sh
    exit 1
fi

# Show service status
echo -e "${GREEN}📊 Service Status:${NC}"
docker-compose -f infra/docker-compose.prod.yml ps

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${YELLOW}🌐 Frontend: https://$DOMAIN${NC}"
echo -e "${YELLOW}🔌 Backend API: https://api.$DOMAIN${NC}"
