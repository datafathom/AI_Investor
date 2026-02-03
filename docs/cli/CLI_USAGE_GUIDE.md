# CLI Usage Guide

Complete guide to using `cli.py` for all operations.

## Overview

All operations are now unified through `cli.py`:

- ✅ **Runtime Operations**: Start/stop frontend, backend
- ✅ **Testing**: All test suites and categories
- ✅ **Deployment**: Production deployment, rollback, health checks
- ✅ **Database**: Migrations, backups, restores
- ✅ **Docker**: Container management
- ✅ **Development**: Dev mode, builds, verification

---

## Quick Reference

### Frontend Operations

```bash
# Start development server
python cli.py frontend dev
python cli.py frontend dev --port 3000

# Build for production
python cli.py frontend build

# Preview production build
python cli.py frontend preview

# Install dependencies
python cli.py frontend install

# Run linter
python cli.py frontend lint

# Verify setup
python cli.py frontend verify
```

### Backend Operations

```bash
# Start development server
python cli.py backend dev
python cli.py backend dev --port 5050 --host 0.0.0.0

# Start production server (Gunicorn)
python cli.py backend prod
python cli.py backend prod --workers 8 --port 5050

# Install dependencies
python cli.py backend install

# Verify setup
python cli.py backend verify
```

### Testing

```bash
# List all test categories
python cli.py test list

# Run all tests
python cli.py test all

# Run specific category
python cli.py test backend
python cli.py test frontend
python cli.py test api
python cli.py test models

# Run with options
python cli.py test all --coverage --verbose
python cli.py test backend --parallel --fail-fast

# Run specific category by name
python cli.py test-category backend-phase1 --coverage
```

### Deployment

```bash
# Deploy to production
python cli.py deploy prod

# Rollback deployment
python cli.py deploy rollback

# Build Docker images
python cli.py deploy build

# Check deployment health
python cli.py deploy health
```

### Database Operations

```bash
# Run migrations
python cli.py db migrate
python cli.py db migrate --direction up

# Rollback migration
python cli.py db migrate --direction down --migration-id phase6_004_legal_documents

# Backup database
python cli.py db backup
python cli.py db backup --type postgres
python cli.py db backup --type neo4j
python cli.py db backup --type all

# Restore database
python cli.py db restore --file /path/to/backup.sql --type postgres

# Check migration status
python cli.py db status
```

### Docker Operations

```bash
# Start containers
python cli.py docker up
python cli.py docker up --build

# Stop containers
python cli.py docker down

# Check status
python cli.py docker status
python cli.py docker ps

# View logs
python cli.py docker logs
python cli.py docker logs --service backend --follow
```

### Development Mode

```bash
# Start dev mode (hot-reload backend + frontend)
python cli.py dev

# Start all services
python cli.py start-all

# Stop all services
python cli.py stop-all

# Check runtime status
python cli.py check-runtimes
```

---

## Common Workflows

### Starting Development Environment

```bash
# Option 1: Use dev mode (recommended)
python cli.py dev

# Option 2: Start individually
python cli.py docker up
python cli.py backend dev
python cli.py frontend dev
```

### Running Tests Before Commit

```bash
# Quick smoke tests
python cli.py test quick

# Full test suite with coverage
python cli.py test all --coverage --verbose
```

### Production Deployment

```bash
# 1. Build images
python cli.py deploy build

# 2. Run migrations
python cli.py db migrate

# 3. Deploy
python cli.py deploy prod

# 4. Check health
python cli.py deploy health
```

### Database Maintenance

```bash
# 1. Backup before changes
python cli.py db backup

# 2. Run new migrations
python cli.py db migrate

# 3. If issues, rollback
python cli.py db migrate --direction down --migration-id <migration_id>

# 4. Check status
python cli.py db status
```

---

## All Available Commands

### Runtime & Development
- `cli.py dev` - Dev mode (hot-reload)
- `cli.py start-all` - Start all services
- `cli.py stop-all` - Stop all services
- `cli.py check-runtimes` - Check dev ports
- `cli.py frontend dev/build/preview/install/lint/verify`
- `cli.py backend dev/prod/install/verify`

### Testing
- `cli.py test list` - List test categories
- `cli.py test all` - Run all tests
- `cli.py test backend` - Backend tests
- `cli.py test frontend` - Frontend tests
- `cli.py test api` - API tests
- `cli.py test models` - Model tests
- `cli.py test quick` - Quick smoke tests
- `cli.py test unit` - Unit tests
- `cli.py test integration` - Integration tests
- `cli.py test-category <name>` - Specific category

### Deployment
- `cli.py deploy prod` - Deploy to production
- `cli.py deploy rollback` - Rollback deployment
- `cli.py deploy build` - Build Docker images
- `cli.py deploy health` - Check deployment health

### Database
- `cli.py db migrate` - Run migrations
- `cli.py db backup` - Backup database
- `cli.py db restore` - Restore database
- `cli.py db status` - Migration status

### Docker
- `cli.py docker up` - Start containers
- `cli.py docker down` - Stop containers
- `cli.py docker status` - Container status
- `cli.py docker logs` - View logs

---

## Help & Discovery

### List All Commands

```bash
python cli.py --help
```

### Get Help for Specific Command

```bash
python cli.py frontend --help
python cli.py test --help
python cli.py deploy --help
```

---

## Examples

### Example 1: Full Development Setup

```bash
# 1. Start infrastructure
python cli.py docker up

# 2. Verify frontend
python cli.py frontend verify

# 3. Install if needed
python cli.py frontend install

# 4. Start frontend
python cli.py frontend dev

# 5. In another terminal, start backend
python cli.py backend dev
```

### Example 2: Pre-Deployment Testing

```bash
# 1. Run all tests
python cli.py test all --coverage

# 2. Build frontend
python cli.py frontend build

# 3. Verify backend
python cli.py backend verify

# 4. Check migration status
python cli.py db status
```

### Example 3: Production Deployment

```bash
# 1. Backup database
python cli.py db backup

# 2. Build images
python cli.py deploy build

# 3. Run migrations
python cli.py db migrate

# 4. Deploy
python cli.py deploy prod

# 5. Health check
python cli.py deploy health
```

---

## Tips

1. **Use `--help`**: Most commands support `--help` flag
2. **Check Status First**: Use `verify` commands before running
3. **Test Before Deploy**: Always run tests before deployment
4. **Backup Before Migrate**: Always backup before running migrations
5. **Use Dev Mode**: `cli.py dev` is fastest for development

---

**Last Updated**: 2026-01-21
