# CLI Complete Reference

**All operations unified through `cli.py`**

---

## 🚀 Quick Start

```bash
# Start frontend
python cli.py frontend dev

# Start backend
python cli.py backend dev

# Run tests
python cli.py test all

# Deploy
python cli.py deploy prod
```

---

## 📋 All Commands

### Frontend Operations

| Command | Description | Example |
|---------|-------------|---------|
| `frontend dev` | Start dev server | `python cli.py frontend dev --port 3000` |
| `frontend build` | Build for production | `python cli.py frontend build` |
| `frontend preview` | Preview production build | `python cli.py frontend preview` |
| `frontend install` | Install dependencies | `python cli.py frontend install` |
| `frontend lint` | Run linter | `python cli.py frontend lint` |
| `frontend verify` | Verify setup | `python cli.py frontend verify` |

### Backend Operations

| Command | Description | Example |
|---------|-------------|---------|
| `backend dev` | Start dev server | `python cli.py backend dev --port 5050` |
| `backend prod` | Start production (Gunicorn) | `python cli.py backend prod --workers 8` |
| `backend install` | Install dependencies | `python cli.py backend install` |
| `backend verify` | Verify setup | `python cli.py backend verify` |

### Testing

| Command | Description | Example |
|---------|-------------|---------|
| `test list` | List all categories | `python cli.py test list` |
| `test all` | Run all tests | `python cli.py test all --coverage` |
| `test backend` | Backend tests | `python cli.py test backend --verbose` |
| `test frontend` | Frontend tests | `python cli.py test frontend` |
| `test api` | API tests | `python cli.py test api --parallel` |
| `test models` | Model tests | `python cli.py test models` |
| `test quick` | Quick smoke tests | `python cli.py test quick` |
| `test unit` | Unit tests | `python cli.py test unit` |
| `test integration` | Integration tests | `python cli.py test integration` |
| `test-category <name>` | Specific category | `python cli.py test-category backend-phase1` |

### Deployment

| Command | Description | Example |
|---------|-------------|---------|
| `deploy prod` | Deploy to production | `python cli.py deploy prod` |
| `deploy rollback` | Rollback deployment | `python cli.py deploy rollback` |
| `deploy build` | Build Docker images | `python cli.py deploy build` |
| `deploy health` | Check deployment health | `python cli.py deploy health` |

### Database

| Command | Description | Example |
|---------|-------------|---------|
| `db migrate` | Run migrations | `python cli.py db migrate` |
| `db migrate --direction down` | Rollback | `python cli.py db migrate --direction down --migration-id phase6_004` |
| `db backup` | Backup database | `python cli.py db backup --type all` |
| `db restore` | Restore from backup | `python cli.py db restore --file backup.sql` |
| `db status` | Migration status | `python cli.py db status` |

### Docker

| Command | Description | Example |
|---------|-------------|---------|
| `docker up` | Start containers | `python cli.py docker up --build` |
| `docker down` | Stop containers | `python cli.py docker down` |
| `docker status` | Container status | `python cli.py docker status` |
| `docker logs` | View logs | `python cli.py docker logs --service backend` |
| `docker ps` | Formatted status | `python cli.py docker ps` |

### Development

| Command | Description | Example |
|---------|-------------|---------|
| `dev` | Dev mode (hot-reload) | `python cli.py dev` |
| `start-all` | Start all services | `python cli.py start-all` |
| `stop-all` | Stop all services | `python cli.py stop-all` |
| `check-runtimes` | Check dev ports | `python cli.py check-runtimes` |
| `check-backend` | Check backend health | `python cli.py check-backend` |

---

## 🎯 Common Workflows

### Daily Development

```bash
# Start everything
python cli.py dev

# Or individually
python cli.py docker up
python cli.py backend dev
python cli.py frontend dev
```

### Before Committing

```bash
# Run tests
python cli.py test all --coverage

# Lint frontend
python cli.py frontend lint

# Verify everything
python cli.py frontend verify
python cli.py backend verify
```

### Production Deployment

```bash
# 1. Backup
python cli.py db backup

# 2. Build
python cli.py deploy build
python cli.py frontend build

# 3. Migrate
python cli.py db migrate

# 4. Deploy
python cli.py deploy prod

# 5. Health check
python cli.py deploy health
```

### Database Maintenance

```bash
# Check status
python cli.py db status

# Backup before changes
python cli.py db backup

# Run migrations
python cli.py db migrate

# If issues, rollback
python cli.py db migrate --direction down --migration-id <id>
```

---

## 📖 Help

Get help for any command:

```bash
python cli.py --help
python cli.py frontend --help
python cli.py test --help
python cli.py deploy --help
```

---

## ✅ Verification

Verify your setup:

```bash
# Frontend
python cli.py frontend verify

# Backend
python cli.py backend verify

# Check runtimes
python cli.py check-runtimes
```

---

**All operations now go through `cli.py`!** 🎉

---

**Last Updated**: 2026-01-21
