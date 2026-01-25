# AI Investor Platform

Intelligent investment platform with AI-powered trading, portfolio management, and analytics.

## Features

- 🤖 **AI-Powered Trading**: Machine learning predictions and automated strategies
- 📊 **Portfolio Management**: Comprehensive portfolio tracking and analytics
- 📈 **Real-Time Analytics**: Advanced performance metrics and risk analysis
- 🔒 **Security**: Bank-level encryption and security measures
- 📱 **Modern UI**: Responsive, intuitive interface
- 🚀 **Production-Ready**: Complete deployment infrastructure

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Neo4j 5+
- Redis 7+

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-org/ai-investor.git
   cd ai-investor
   ```

2. **Set Up Backend**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up Frontend**
   ```bash
   cd frontend2
   npm install --legacy-peer-deps
   ```

4. **Start Services**
   ```bash
   docker-compose up -d postgres neo4j redis
   ```

5. **Run Migrations**
   ```bash
   python scripts/database/migrate.py up
   ```

6. **Start Development Servers**
   ```bash
   # Backend (terminal 1)
   python -m web.app
   
   # Frontend (terminal 2)
   cd frontend2
   npm run dev
   ```

7. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5050
   - API Docs: http://localhost:5050/api/docs

## Documentation

- [User Guide](docs/user/USER_GUIDE.md)
- [Developer Setup](docs/development/SETUP.md)
- [Architecture](docs/development/ARCHITECTURE.md)
- [API Documentation](docs/api/API_DOCUMENTATION.md)
- [Deployment Guide](docs/deployment/PRODUCTION_DEPLOYMENT.md)
- [Contributing](CONTRIBUTING.md)

## Testing

### Run Tests

```bash
# Backend tests
pytest

# Frontend tests
cd frontend2 && npm test

# E2E tests
npm run test:e2e

# All tests with coverage
pytest --cov=services --cov=web --cov-report=html
```

### Test Categories

```bash
# Run specific test category
python cli.py test backend
python cli.py test frontend
python cli.py test api
python cli.py test models
```

## Project Structure

```
ai-investor/
├── services/          # Backend services
├── web/              # Web API and routes
├── frontend2/        # React frontend
├── tests/            # Test files
├── migrations/       # Database migrations
├── scripts/          # Utility scripts
├── docs/             # Documentation
└── infra/            # Infrastructure configs
```

## Technology Stack

### Backend
- Flask (REST API)
- FastAPI (Async endpoints)
- PostgreSQL (Primary database)
- Neo4j (Graph database)
- Redis (Caching)
- Kafka (Event streaming)

### Frontend
- React 18
- Vite
- React Router
- Socket.io (WebSocket)

### Infrastructure
- Docker & Docker Compose
- Traefik (Reverse proxy)
- Nginx (Frontend serving)
- Prometheus & Grafana (Monitoring)
- Sentry (Error tracking)

## Production Deployment

See [Production Deployment Guide](docs/deployment/PRODUCTION_DEPLOYMENT.md) for detailed instructions.

Quick deployment:
```bash
./scripts/deployment/prod_deploy.sh
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[Your License Here]

## Support

- **Documentation**: [docs.ai-investor.com](https://docs.ai-investor.com)
- **Email**: support@ai-investor.com
- **Issues**: [GitHub Issues](https://github.com/your-org/ai-investor/issues)

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-21
