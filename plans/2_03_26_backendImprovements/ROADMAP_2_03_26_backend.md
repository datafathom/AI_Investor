# Backend Security & Performance Roadmap (2026 Edition)

**Status**: Planning
**Target Completion**: Q1 2026
**Owner**: Backend Engineering Team

## Executive Summary
This roadmap outlines the steps to elevate the AI Investor backend to 2026 industry standards. It focuses on "Secure by Design" principles, leveraging the latest features of our stack (PostgreSQL 18, Neo4j 2025, Kafka 4.0, Redis 8), and optimizing FastAPI performance.

---

## Phase 1: Dependency & Infrastructure Upgrades
**Goal**: Bring all underlying infrastructure to the latest secure versions.

### 1.1 Python Dependencies
- [ ] **Action**: Update `requirements.txt` (or equivalent dependency manager) with strict version pinning.
- [ ] **Target Packages**:
    - `fastapi-api-key >= 1.1.0` (Critical for timing attack mitigation)
    - `uvicorn[standard]` (Ensures `uvloop` is installed)
    - `pydantic >= 2.0` (Ensure V2 strict mode is active)
    - `fastapi-limiter` (For Rate Limiting)
- [ ] **File**: `requirements.txt` / `infra/Dockerfile.backend.prod`

### 1.2 Docker Service Upgrades
- [ ] **Action**: Update `infra/docker-compose.yml` images.
- [ ] **Changes**:
    - **PostgreSQL**: `timescale/timescaledb:latest-pg15` -> `postgres:18.1` (or latest Timescale compatible with PG18 if available, otherwise latest stable PG). *Note: Verify Timescale compatibility.*
    - **Neo4j**: `neo4j:5.12.0` -> `neo4j:2025.10.1` (or latest Enterprise/Community release).
    - **Kafka**: `confluentinc/cp-kafka:7.4.0` -> `confluentinc/cp-kafka:7.8.0` (or Kafka 4.0 equivalent).
    - **Redis**: `redis:7-alpine` -> `redis:8.0-alpine` (if available, else latest 7.x with ACLs).
- [ ] **File**: `infra/docker-compose.yml`

---

## Phase 2: Network Security (Zero Trust LAN)
**Goal**: Restrict access to services so they are mutually authenticated and not exposed to the entire LAN.

### 2.1 Docker Network Isolation
- [ ] **Action**: Define an internal bridge network in `infra/docker-compose.yml`.
- [ ] **Implementation**:
    ```yaml
    networks:
      investor-network:
        internal: true  # Prevents external access to containers on this net
    ```
- [ ] **Exception**: Explicitly bind the FastAPI application (running on host) to the LAN IP, NOT `0.0.0.0`.
- [ ] **Files**: `infra/docker-compose.yml`

### 2.2 Host Firewall (UFW)
- [ ] **Action**: Configure UFW on the host machine.
- [ ] **Rules**:
    - Allow SSH (Port 22)
    - Allow Docker Management (Port 2376) from trusted IPs only.
    - Allow Application Port (e.g., 5050) from LAN.
    - Deny everything else.
- [ ] **Documentation**: implementation details in `docs/infrastructure/security_hardening.md`.

---

## Phase 3: Database Hardening
**Goal**: Move from "Trust Authentication" to strict, encrypted storage and access control.

### 3.1 PostgreSQL Security
- [ ] **Action**: Enable SCRAM-SHA-256 and SSL.
- [ ] **Config**:
    - Update `pg_hba.conf` inside the container (via volume mount).
    - Change `host all all all trust` to `hostssl all all 0.0.0.0/0 scram-sha-256`.
- [ ] **File**: `config/database.py` (Update connection string to support SSL mode).

### 3.2 Neo4j PBAC
- [ ] **Action**: Implement Property-Based Access Control.
- [ ] **Config**:
    - Disable APOC export procedures in `neo4j.conf` (via env vars in compose).
    - Create roles with restricted access to sensitive node properties (e.g., PII).
- [ ] **Refactor**: Update `neo4j/` connector scripts to use specific service users, not `neo4j` admin.

### 3.3 Redis ACLs
- [ ] **Action**: Replace global password with User ACLs.
- [ ] **Implementation**:
    - Create `users.acl` file.
    - Define `fastapi_user` with restricted command access (`-@admin`, `+@read`, `+@write`).
    - Rename dangerous commands like `FLUSHALL`.
- [ ] **File**: `config/redis_config.json` and `infra/docker-compose.yml`.

---

## Phase 4: Application Security & Performance
**Goal**: Harden the FastAPI application against abuse and optimize concurrency.

### 4.1 Global Async Audit & Refactor
- [ ] **Audit**: Scan `services/` and `apis/` for mixed async/sync usage.
- [ ] **Rule**:
    - **I/O Bound** (DB, External API): Must use `async def` AND async libraries (`httpx`, `asyncpg`).
    - **CPU Bound** (Calculations, Data Processing): Use `def` (runs in threadpool).
- [ ] **Specific Targets**:
    - `services/portfolio/assets_service.py` (Currently `def`, uses file I/O. Keep as `def` or move to `aiofiles` if high throughput needed).
    - `config/database.py` (Uses synchronous SQLAlchemy `create_engine`. MAJOR REFACTOR required to switch to `AsyncEngine` if we want full async benefits).

### 4.2 Rate Limiting
- [ ] **Action**: Integrate `fastapi-limiter` backed by Redis.
- [ ] **Implementation**:
    - Apply global limits (e.g., 100 req/min).
    - Apply strict limits on Auth endpoints (5 req/min).
- [ ] **File**: `apis/main.py` (or where `app` is initialized), `apis/auth_routes.py`.

### 4.3 Middlewares & CORS
- [ ] **Action**: Strict CORS configuration.
- [ ] **Changes**:
    - Remove `allow_origins=["*"]`.
    - List specific frontend domains/IPs.
- [ ] **Action**: Ensure `TrustedHostMiddleware` is active.
- [ ] **File**: `apis/main.py`.

---

## Phase 5: Verification & Monitoring
**Goal**: Validate improvements and ensure observability.

### 5.1 Load Testing
- [ ] **Action**: Run `locust` or `k6` tests to benchmark performance before/after `uvloop` and async refactors.
- [ ] **Command**: `python cli.py test speed` (Expand to include load tests).

### 5.2 Security Scanning
- [ ] **Action**: Run `bandit` and `safety` checks in CI/CD.
- [ ] **Tool**: `pip install bandit safety`.

### 5.3 Monitoring
- [ ] **Action**: Connect Sentry performance monitoring.
- [ ] **Integration**: Trace DB queries to identify N+1 problems or slow synchronous calls.

## Implementation Plan Overview

| Step | Task | Complexity | Impact |
|------|------|------------|--------|
| 1 | Upgrade Docker Images & Deps | Low | High (Security) |
| 2 | Network/Firewall Config | Medium | High (Security) |
| 3 | Postgres SCRAM & SSL | Medium | High (Protection) |
| 4 | Redis ACLs | Low | Medium |
| 5 | Async/Sync Audit | High | High (Performance) |
| 6 | Rate Limiting | Low | High (Anti-Abuse) |
