# Development Setup Guide

This guide will help you set up your development environment for AI Investor.

## Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
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

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend

```bash
cd frontend2
npm install --legacy-peer-deps
```

### 4. Start Infrastructure Services

```bash
# Start databases and services
docker-compose up -d postgres neo4j redis zookeeper kafka
```

Wait for services to be healthy (check with `docker-compose ps`).

### 5. Run Database Migrations

```bash
# Set environment variables
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=investor_user
export POSTGRES_PASSWORD=investor_password
export POSTGRES_DB=investor_db

# Run migrations
python scripts/database/migrate.py up
```

### 6. Start Development Servers

**Backend** (in one terminal):
```bash
python -m web.fastapi_gateway
```

**Frontend** (in another terminal):
```bash
cd frontend2
npm run dev
```

### 7. Verify Setup

- Backend: http://localhost:5050/api/v1/health
- Frontend: http://localhost:3000

---

## Environment Variables

Create a `.env` file in the project root:

```env
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=investor_user
POSTGRES_PASSWORD=investor_password
POSTGRES_DB=investor_db

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_password

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your-secret-key-here
SECRET_KEY=your-secret-key-here

# Email (optional)
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=your-api-key

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

---

## Running Tests

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=web --cov-report=html

# Run specific test file
pytest tests/unit/test_portfolio_service.py

# Run integration tests
pytest tests/integration/
```

### Frontend Tests

```bash
cd frontend2

# Run unit tests
npm test

# Run E2E tests
npm run test:e2e

# Run E2E in headed mode
npm run test:e2e:headed
```

---

## Development Tools

### Code Formatting

**Python**:
```bash
black .
isort .
```

**JavaScript**:
```bash
cd frontend2
npm run format
```

### Linting

**Python**:
```bash
flake8 .
mypy .
```

**JavaScript**:
```bash
cd frontend2
npm run lint
```

---

## Database Management

### Create Migration

```bash
python scripts/database/migration_manager.py create --name my_migration --description "Description"
```

### Apply Migrations

```bash
python scripts/database/migrate.py up
```

### Rollback Migration

```bash
python scripts/database/migration_manager.py rollback --migration-id phase6_004_legal_documents
```

### Check Migration Status

```bash
python scripts/database/migration_manager.py status
```

---

## Debugging

### Backend Debugging

Use VS Code debugger or add breakpoints:

```python
import pdb; pdb.set_trace()
```

### Frontend Debugging

Use React DevTools and browser DevTools.

### Database Debugging

Connect to PostgreSQL:
```bash
psql -h localhost -U investor_user -d investor_db
```

---

## Common Issues

### Port Already in Use

If port 5050 or 3000 is in use:

```bash
# Find process using port
lsof -i :5050  # macOS/Linux
netstat -ano | findstr :5050  # Windows

# Kill process or change port in .env
```

### Database Connection Errors

1. Check Docker containers are running: `docker-compose ps`
2. Verify environment variables
3. Check database logs: `docker-compose logs postgres`

### Module Not Found Errors

1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check PYTHONPATH is set correctly

---

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- ESLint
- Prettier
- Docker

### PyCharm

1. Open project
2. Configure Python interpreter (venv)
3. Set up run configurations
4. Enable code inspections

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

---

**Last Updated**: 2026-01-21  
**Version**: 1.0
