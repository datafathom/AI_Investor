# Production Deployment Guide

This guide covers deploying the AI Investor platform to production.

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured
- SSL certificates (Let's Encrypt via Traefik)
- Production environment variables configured

## Quick Start

1. **Copy environment template**:
   ```bash
   cp .env.production.template .env.production
   ```

2. **Fill in all environment variables** in `.env.production`:
   - Database passwords
   - API keys
   - Secrets (JWT_SECRET, SECRET_KEY, ENCRYPTION_MASTER_KEY)
   - Domain names

3. **Deploy**:
   ```bash
   ./scripts/deployment/prod_deploy.sh
   ```

## Manual Deployment Steps

### 1. Start Infrastructure Services

```bash
docker-compose -f infra/docker-compose.prod.yml up -d postgres neo4j redis zookeeper kafka
```

Wait for services to be healthy (check with `docker-compose ps`).

### 2. Run Database Migrations

```bash
docker-compose -f infra/docker-compose.prod.yml run --rm backend python scripts/database/migrate.py up
```

### 3. Start Application Services

```bash
docker-compose -f infra/docker-compose.prod.yml up -d backend frontend traefik
```

### 4. Verify Deployment

```bash
# Check service status
docker-compose -f infra/docker-compose.prod.yml ps

# Check health endpoints
curl http://localhost/health
curl https://yourdomain.com/health
```

## Rollback Procedure

If deployment fails:

```bash
./scripts/deployment/rollback.sh [backup_directory]
```

Or manually:

```bash
docker-compose -f infra/docker-compose.prod.yml down
# Restore from backup
docker-compose -f infra/docker-compose.prod.yml up -d
```

## Health Checks

- **Basic Health**: `GET /health` - Returns 200 if service is up
- **Readiness**: `GET /health/readiness` - Checks database connectivity
- **Liveness**: `GET /health/liveness` - Verifies service is alive
- **Detailed**: `GET /health/detailed` - Full system status

## Monitoring

- Traefik Dashboard: `https://traefik.yourdomain.com`
- Service logs: `docker-compose -f infra/docker-compose.prod.yml logs -f [service]`

## Troubleshooting

### Services won't start
- Check environment variables are set correctly
- Verify Docker has enough resources
- Check logs: `docker-compose logs [service]`

### Database connection errors
- Verify POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD are correct
- Check postgres container is healthy: `docker-compose ps postgres`

### SSL certificate issues
- Verify ACME_EMAIL is set
- Check Traefik logs for certificate generation errors
- Ensure domain DNS points to server

## Security Checklist

- [ ] All secrets are in `.env.production` (not committed to git)
- [ ] Strong passwords for all services
- [ ] SSL certificates configured
- [ ] Firewall rules configured
- [ ] Rate limiting enabled
- [ ] Security headers configured
