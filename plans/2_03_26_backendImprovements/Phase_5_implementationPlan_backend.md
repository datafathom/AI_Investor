# Phase 5: Verification, Monitoring & Rollout (Implementation Plan)

**Goal**: Validate that all security improvements are active, performance is stable, and no regressions were introduced across the entire application stack.

## 1. Automated Verification Suite (App-Wide)
**Context**: We need a single "Master Script" that validates every layer we hardened.

### 1.1 `scripts/verify_backend_security.py`
- **Scope**:
    - **Network**: Check ports 5432, 7474, 9092 are CLOSED to external (simulated via checking `docker port`).
    - **Postgres**: Attempt connection using `psycopg2` with `sslmode='disable'`. MUST fail.
    - **Neo4j**: Attempt connection as `neo4j` (default admin). MUST fail. Attempt as `app_user` w/o TLS. MUST fail.
    - **Redis**: Attempt `FLUSHALL`. MUST fail (ACL check).
    - **API Gateway**:
        - Hit `/flask/health` (Mounted) -> Expect 200.
        - Hit `/api/health` (FastAPI) -> Expect 200.
        - Hit `/` with `Origin: http://evil.com` -> Expect 403/Error (CORS).

## 2. Load Testing (Performance)
**Context**: Mitigation for Timing Attacks (CVE-2026-23996) and Async refactors must not degrade speed.

### 2.1 Latency & Throughput
- **Tool**: `locust`
- **File**: `tests/performance/locustfile.py`
- **Scenarios**:
    1.  **Auth Storm**: 500 users logging in simultaneously. Check for "Jitter" implementation (headers or response time distribution).
    2.  **Market Data Stream**: High throughput on `/api/market-data`.
    3.  **Graph Traversal**: Complex query on `/api/assets/graph`.
- **Success Criteria**:
    - P95 Latency < 200ms for API.
    - Zero timeouts at 100 RPS.

## 3. Security Scanning (CI Prevention)
**Context**: Prevent regression.

### 3.1 Static Analysis
- **Tool**: `bandit`
- **Command**: `bandit -r web/ -r services/ -ll -ii`
- **Focus**: Hardcoded passwords, unsafe deserialization (`pickle`), shell injection.

## 4. Rollout Strategy (Zero Downtime Attempt)
**Context**: Switching architectures (Flask -> FastAPI Mount) is risky.

### 4.1 Deployment Steps
1.  **Preparation**:
    - Back up all volumes: `docker-compose exec postgres pg_dump -U investor_user investor_db > backup.sql`.
    - Generate new SSL certs: `scripts/infra/cert_runner.py`.
2.  **Infrastructure Swap**:
    - `docker-compose down`.
    - `docker-compose build --no-cache`.
    - `docker-compose up -d`.
3.  **Database Migration**:
    - Run `scripts/db/setup_neo4j_roles.py`.
    - Run ACL placement for Redis.
4.  **Application Launch**:
    - Start Gateway: `python cli.py start-backend --host 127.0.0.1`.
5.  **Verification**:
    - Run `scripts/verify_backend_security.py`.

## 5. Files to Create/Modify
- [NEW] [scripts/verify_backend_security.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/verify_backend_security.py) (The Master Verification Script)
- [NEW] [tests/performance/locustfile.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/performance/locustfile.py)
