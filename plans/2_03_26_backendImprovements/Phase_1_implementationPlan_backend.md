# Phase 1: Dependency & Infrastructure Upgrades (Implementation Plan)

**Goal**: Establish a secure, modern foundation by consolidating dependencies and upgrading all infrastructure components to their 2026 secure baselines.

## 1. Dependency Consolidation
**Context**: Dependencies are dangerously fragmented across 8+ files in `logs/`. We must consolidate them into a single, pinned `requirements.txt` to ensure reproducible and secure builds.

### 1.1 Action Items
1.  **Create Root `requirements.txt`**:
    - **Source Files to Merge & DELETE**:
        - `logs/requirements.txt`
        - `logs/requirements-core.txt`
        - `logs/requirements-dev.txt`
        - `logs/requirements-ml.txt`
        - `logs/requirements-linux-dev.txt`
        - `logs/requirements-linux-storage-host.txt`
        - `logs/requirements-windows-dev.txt`
        - `logs/requirements-windows-storage-host.txt`
    - **Strategy**: Identify the superset of packages. Use `pip-compile` or manual merge to ensure no version conflicts.
    - **Enforce Strict Pinning** (2026 Standards):
        ```text
        fastapi==0.115.0  # (Or latest stable 2026 version)
        pydantic==2.9.0
        uvicorn[standard]==0.34.0
        fastapi-api-key==1.1.0  # Mitigation for CVE-2026-23996
        fastapi-limiter==0.1.6
        asyncpg==0.30.0
        redis==5.2.0
        confluent-kafka==2.8.0
        neo4j==5.25.0
        python-multipart==0.0.12 # For CVE fixes
        bcrypt==4.2.0
        passlib[bcrypt]==1.7.4
        python-jose[cryptography]==3.3.0
        sqlalchemy==2.0.36 # Ensure 2.0+ for future async migration
        flask==3.1.0
        flask-cors==5.0.0
        flask-socketio==5.4.0
        eventlet==0.36.0
        ```

2.  **Clean Up**:
    - **Command**: `rm logs/requirements*.txt`
    - **Verify**: Ensure the `logs/` directory contains only actual logs.

3.  **Update Docker Builds**:
    - **File**: `infra/Dockerfile.backend.prod`
    - **Change**: Ensure `COPY requirements.txt .` and `RUN pip install -r requirements.txt` are the *only* dependency steps. Remove any references to `logs/`.

## 2. Infrastructure Upgrades (Docker)
**Context**: Upgrade all container images in *both* dev and prod compose files to secure 2026 versions.

### 2.1 `infra/docker-compose.yml` (Dev) & `infra/docker-compose.prod.yml` (Prod)
**Apply these changes to BOTH files:**

#### PostgreSQL 18
- **Image**: `postgres:18.1-alpine` (Switching from TimescaleDB due to simpler licensing/security path, unless Timescale features are actively used in `quant` services. If used, find `timescale/timescaledb:latest-pg17`).
- **Environment**:
    ```yaml
    environment:
      POSTGRES_HOST_AUTH_METHOD: "scram-sha-256"
      POSTGRES_INITDB_ARGS: "--auth-host=scram-sha-256 --auth-local=scram-sha-256"
    ```
- **Volumes**:
    ```yaml
    volumes:
      - ./certs/server.crt:/var/lib/postgresql/server.crt:ro
      - ./certs/server.key:/var/lib/postgresql/server.key:ro
    ```

#### Neo4j 2025
- **Image**: `neo4j:2025.10.1-enterprise`
- **Environment**:
    ```yaml
    environment:
      NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
      NEO4J_dbms_security_auth__enabled: "true"
      NEO4J_dbms_security_procedures_allowlist: "apoc.search.*,apoc.coll.*,apoc.util.*" # Restrict APOC
      NEO4J_server_bolt_tls__level: "REQUIRED" # Enforce TLS
    ```

#### Kafka 4.0 (KRaft Mode)
- **Image**: `confluentinc/cp-kafka:7.8.0` (Kafka 3.9/4.0 comp)
- **Environment**:
    ```yaml
    environment:
      KAFKA_ENABLE_KRAFT: "yes"
      KAFKA_PROCESS_ROLES: "broker,controller"
      KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"
      KAFKA_SLF4J_LOG_PERSONALITY: "standard" # Better logging
    ```
- **Removal**: Remove the `zookeeper` service entirely from `docker-compose.yml`.

#### Redis 8
- **Image**: `redis:8.0-alpine`
- **Command**: `redis-server --aclfile /run/secrets/users.acl --include /run/secrets/redis.conf`
- **Volumes**:
    ```yaml
    volumes:
      - ./infra/redis/users.acl:/run/secrets/users.acl:ro
      - ./config/redis_config.json:/run/secrets/redis.conf:ro # Note: json isn't valid redis.conf, we need to create a real redis.conf
    ```

## 3. Verification Plan
### 3.1 Dependency Check
- **Command**:
    ```bash
    python -m venv venv_verify
    source venv_verify/bin/activate
    pip install -r requirements.txt
    pip list | grep -E "fastapi|pydantic|neo4j|redis|confluent-kafka"
    ```
- **Success Criteria**: Versions match the pinned 2026/late 2025 baselines.

### 3.2 Infrastructure Launch
- **Command**: `docker-compose up -d --build`
- **Checks**:
    - `docker-compose logs postgres` -> Look for "database system is ready to accept connections" and "SCRAM-SHA-256".
    - `docker-compose logs neo4j` -> Look for "Bolt enabled on ...".
    - `docker-compose logs kafka` -> Look for "Transitioning to active controller" (KRaft mode).

### 3.3 Application Smoke Test
- **Command**: `python cli.py check-backend`
- **Success Criteria**: Returns 200 OK. (Note: App might fail connecting to DBs until Phase 3 config updates are applied, but the *files* should be in place).

## 4. Files to Create/Modify
- [NEW] [requirements.txt](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/requirements.txt)
- [DELETE] [logs/requirements*.txt](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/logs/)
- [MODIFY] [infra/docker-compose.yml](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/infra/docker-compose.yml)
- [MODIFY] [infra/docker-compose.prod.yml](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/infra/docker-compose.prod.yml)
- [MODIFY] [infra/Dockerfile.backend.prod](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/infra/Dockerfile.backend.prod)
