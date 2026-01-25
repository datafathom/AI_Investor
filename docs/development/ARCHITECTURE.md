# AI Investor Architecture Documentation

## Overview

AI Investor is a full-stack investment platform built with modern technologies and best practices.

## System Architecture

### High-Level Architecture

```
┌─────────────┐
│   Frontend  │ (React + Vite)
│  (Port 3000)│
└──────┬──────┘
       │
       │ HTTP/WebSocket
       │
┌──────▼──────┐
│   Backend   │ (Flask + FastAPI)
│  (Port 5050)│
└──────┬──────┘
       │
       ├───► PostgreSQL (TimescaleDB)
       ├───► Neo4j (Graph Database)
       ├───► Redis (Caching)
       ├───► Kafka (Event Streaming)
       └───► External APIs
```

### Technology Stack

#### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **State Management**: React Context + Hooks
- **Routing**: React Router
- **Styling**: CSS Modules
- **Testing**: Playwright (E2E), Jest (Unit)

#### Backend
- **Framework**: Flask (REST API)
- **Async Framework**: FastAPI (for async endpoints)
- **WSGI Server**: Gunicorn (production)
- **Database**: PostgreSQL with TimescaleDB
- **Graph DB**: Neo4j
- **Cache**: Redis
- **Message Queue**: Kafka
- **Testing**: pytest

#### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Traefik / Nginx
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Error Tracking**: Sentry
- **Logging**: CloudWatch / ELK / Loki

---

## Component Architecture

### Backend Services

#### Core Services
- **Portfolio Service**: Portfolio management and calculations
- **Trading Service**: Order execution and management
- **Analytics Service**: Performance and risk analytics
- **Market Data Service**: Real-time and historical market data
- **AI Service**: Machine learning predictions

#### Supporting Services
- **Authentication Service**: User authentication and authorization
- **Notification Service**: Email, SMS, push notifications
- **Document Service**: Document storage and management
- **Integration Service**: Third-party API integrations

### Frontend Components

#### Core Components
- **Dashboard**: Main portfolio view
- **Trading Interface**: Order placement and management
- **Analytics Dashboard**: Performance metrics and charts
- **Settings**: User preferences and account management

#### Shared Components
- **MenuBar**: Navigation menu
- **ErrorBoundary**: Error handling
- **OnboardingFlow**: User onboarding
- **Legal Pages**: Terms, Privacy, etc.

---

## Data Flow

### Request Flow

1. **User Action**: User interacts with frontend
2. **API Request**: Frontend sends HTTP request to backend
3. **Authentication**: Backend validates JWT token
4. **Business Logic**: Service layer processes request
5. **Data Access**: Database queries executed
6. **Response**: JSON response sent to frontend
7. **UI Update**: Frontend updates UI with new data

### Real-Time Updates

1. **Event Occurs**: Backend service generates event
2. **Kafka Producer**: Event published to Kafka topic
3. **WebSocket**: Backend sends update via WebSocket
4. **Frontend**: React component receives update
5. **UI Update**: Component re-renders with new data

---

## Database Schema

### PostgreSQL (Primary Database)

#### Core Tables
- `users`: User accounts
- `portfolios`: Portfolio information
- `positions`: Stock positions
- `orders`: Trading orders
- `transactions`: Transaction history

#### Feature Tables
- `user_workspaces`: Workspace layouts
- `legal_documents`: Legal document versions
- `legal_document_acceptances`: User acceptances
- `user_onboarding`: Onboarding status
- `user_preferences`: User preferences

### Neo4j (Graph Database)

#### Nodes
- Stocks (symbols, companies)
- Users
- Portfolios
- Strategies

#### Relationships
- OWNS (User → Portfolio)
- CONTAINS (Portfolio → Position)
- CORRELATES_WITH (Stock → Stock)
- FOLLOWS (User → Strategy)

---

## Security Architecture

### Authentication & Authorization

1. **JWT Tokens**: Stateless authentication
2. **Refresh Tokens**: Long-lived session management
3. **Role-Based Access Control (RBAC)**: Permission system
4. **API Keys**: For programmatic access

### Data Protection

1. **Encryption at Rest**: Database encryption
2. **Encryption in Transit**: TLS/SSL for all connections
3. **Secrets Management**: Vault / AWS Secrets Manager
4. **Input Validation**: All inputs validated and sanitized

### Security Headers

- Content Security Policy (CSP)
- Strict Transport Security (HSTS)
- X-Frame-Options
- X-Content-Type-Options

---

## Deployment Architecture

### Production Environment

```
┌─────────────┐
│   Traefik   │ (Reverse Proxy + SSL)
└──────┬──────┘
       │
       ├───► Backend (Gunicorn)
       ├───► Frontend (Nginx)
       │
       ├───► PostgreSQL
       ├───► Neo4j
       ├───► Redis
       └───► Kafka
```

### CI/CD Pipeline

1. **Code Push**: Developer pushes to GitHub
2. **CI Trigger**: GitHub Actions runs tests
3. **Build**: Docker images built
4. **Test**: Unit, integration, E2E tests
5. **Security Scan**: Vulnerability scanning
6. **Deploy**: Deploy to staging/production
7. **Health Check**: Verify deployment
8. **Rollback**: Auto-rollback on failure

---

## Monitoring & Observability

### Metrics

- **Application Metrics**: Request rate, latency, errors
- **Business Metrics**: Users, signups, revenue
- **Infrastructure Metrics**: CPU, memory, disk
- **Database Metrics**: Query performance, connections

### Logging

- **Application Logs**: Structured JSON logging
- **Access Logs**: HTTP request logs
- **Error Logs**: Exception tracking
- **Audit Logs**: Security and compliance

### Alerting

- **Error Rate**: Alert on high error rates
- **Latency**: Alert on slow responses
- **Availability**: Alert on service downtime
- **Business Metrics**: Alert on anomalies

---

## Development Workflow

### Local Development

1. **Clone Repository**: `git clone ...`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Start Services**: `docker-compose up`
4. **Run Migrations**: `python scripts/database/migrate.py up`
5. **Start Backend**: `python -m web.app`
6. **Start Frontend**: `cd frontend2 && npm run dev`

### Testing

1. **Unit Tests**: `pytest tests/unit/`
2. **Integration Tests**: `pytest tests/integration/`
3. **E2E Tests**: `npm run test:e2e`
4. **Load Tests**: `k6 run tests/load/load_test_scenarios.js`

### Code Quality

- **Linting**: `flake8`, `eslint`
- **Formatting**: `black`, `prettier`
- **Type Checking**: `mypy`, `typescript`
- **Coverage**: `pytest-cov`, `jest --coverage`

---

## API Design

### REST API

- **Base URL**: `https://api.ai-investor.com/api/v1`
- **Authentication**: Bearer token in Authorization header
- **Response Format**: JSON
- **Error Format**: Standardized error responses

### WebSocket API

- **Endpoint**: `wss://api.ai-investor.com/ws`
- **Authentication**: Token in connection query
- **Events**: Real-time updates (prices, orders, etc.)

---

## Performance Optimization

### Caching Strategy

- **Redis**: Frequently accessed data
- **CDN**: Static assets
- **Browser Cache**: Client-side caching
- **Database Query Cache**: Query result caching

### Database Optimization

- **Indexes**: Strategic indexes on frequently queried columns
- **Connection Pooling**: Reuse database connections
- **Query Optimization**: Optimize slow queries
- **Read Replicas**: Scale read operations

---

## Future Enhancements

### Planned Features

1. **Microservices**: Split monolith into microservices
2. **Kubernetes**: Container orchestration
3. **GraphQL**: Alternative API layer
4. **Event Sourcing**: Event-driven architecture
5. **CQRS**: Command Query Responsibility Segregation

---

**Last Updated**: 2026-01-21  
**Version**: 1.0
