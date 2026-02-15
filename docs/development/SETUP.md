# Development Setup Guide

> **Last Updated**: 2026-02-14

This guide covers setting up the Sovereign OS (AI Investor) development environment.

## Prerequisites

- **Python**: 3.11+
- **Node.js**: 23.x (currently running v23.9.0)
- **Docker**: 20.10+ with Docker Compose 2.0+
- **Git**: Latest version

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/ai-investor.git
cd ai-investor
```

### 2. Set Up Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend

```bash
cd Frontend
npm install --legacy-peer-deps
```

### 4. Start Infrastructure Services

```bash
# Start databases and services
docker-compose up -d postgres neo4j redis zookeeper kafka
```

Wait for services to be healthy: `docker-compose ps`.

### 5. Start Development Servers

The project uses a unified CLI for all operations. There are two primary startup modes:

**Full Stack (with databases):**
```powershell
.\venv\Scripts\activate
python cli.py dev
```

**Frontend + Backend Only (no databases):**
```powershell
.\venv\Scripts\activate
python cli.py dev-no-db
```

This starts the FastAPI backend on port `5050` and the Vite dev server on port `5173`.

### 6. Verify Setup

- **Backend**: http://127.0.0.1:5050/api/v1/health
- **Frontend**: http://127.0.0.1:5173

---

## Environment Variables

Create a `.env` file in the project root. See `.env.example` for the full template. Key variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `BACKEND_PORT` | `5050` | FastAPI server port |
| `VITE_PORT` / `PORT` | `5173` | Vite dev server port |
| `POSTGRES_HOST` | `localhost` | PostgreSQL host |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j connection |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis cache |
| `JWT_SECRET` | — | JWT signing key (required) |
| `SECRET_KEY` | — | Application secret (required) |

> **Security**: All local servers bind to `127.0.0.1`. Never use `0.0.0.0`.

---

## Project Structure

```
AI_Investor/
├── Frontend/                    # React 19 + Vite 5 frontend
│   ├── src/
│   │   ├── components/ui/       # shadcn/ui component library
│   │   ├── config/              # departmentRegistry.js
│   │   ├── pages/
│   │   │   ├── admin/           # Admin-only pages
│   │   │   └── workstations/    # Department workstation pages (125+ files)
│   │   ├── services/            # API service layer
│   │   ├── stores/              # Zustand state stores
│   │   └── App.jsx              # Main router (~2000 lines)
│   └── vite.config.js           # Build configuration
├── services/                    # 133 backend service modules
├── web/                         # FastAPI gateway
├── scripts/                     # CLI runners and utilities
├── config/                      # CLI config, color palette
├── cli.py                       # Unified CLI entry point
├── docs/                        # This documentation tree
└── DEBUGGING/                   # Frontend audit tools and results
```

---

## CLI System

All development commands go through `cli.py`. Key commands:

```powershell
# Start development servers
python cli.py dev              # Full stack with databases
python cli.py dev-no-db        # Frontend + backend only

# Frontend verification
python cli.py frontend verify <dept-slug>     # Verify one department
python cli.py frontend verify all-depts       # Verify all departments

# Slack integration
python cli.py slack start      # Start Slack bot
python cli.py slack notify     # Send notification
```

See `docs/cli/CLI_USAGE_GUIDE.md` for the complete command reference.

---

## Running Tests

### Backend Tests

```powershell
.\venv\Scripts\activate

# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=web --cov-report=html

# Run specific test file
pytest tests/unit/test_portfolio_service.py
```

### Frontend Build Verification

```powershell
cd Frontend
npx vite build
```

A successful build transforms 6100+ modules in ~60 seconds.

---

## Database Management

### Apply Migrations

```powershell
python scripts/database/migrate.py up
```

### Rollback Migration

```powershell
python scripts/database/migration_manager.py rollback --migration-id <id>
```

### Check Migration Status

```powershell
python scripts/database/migration_manager.py status
```

### Connect to PostgreSQL

```powershell
psql -h localhost -U investor_user -d investor_db
```

---

## Common Issues

### Port Already in Use

```powershell
# Find process using port (Windows)
netstat -ano | findstr :5050
netstat -ano | findstr :5173

# Kill process or use the workflow
python cli.py stop  # Stops all services
```

### Database Connection Errors

1. Check Docker containers: `docker-compose ps`
2. Verify `.env` variables match Docker config
3. Check database logs: `docker-compose logs postgres`

### Module Not Found Errors

1. Ensure virtual environment is activated (`.\venv\Scripts\activate`)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. For frontend: `cd Frontend && npm install --legacy-peer-deps`

### Frontend Build Failures

See `docs/frontend/vite_build_configuration.md` for the current constraints table and build verification checklist.

---

## IDE Setup

### VS Code (Recommended)

Extensions:
- Python + Pylance
- ESLint + Prettier
- Tailwind CSS IntelliSense
- Docker
- GitLens
