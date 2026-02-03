# Phase 3: Database Logic & Hardening (Implementation Plan)

**Goal**: Move from "Trust/Default" authentication to "Zero Trust" (SCRAM-SHA-256 / PBAC / ACLs) for ALL persistent stores, ensuring NO service connects insecurely.

## 1. PostgreSQL 18 Security (App-Wide)
**Context**: `config/database.py` is the single source of truth for `create_engine`.

### 1.1 Hardening `config/database.py`
- **Mandate**: The connection string construction MUST detect the environment and append `?sslmode=verify-full&sslrootcert=...` if in production or strict-dev mode.
- **Code Change**:
    ```python
    # config/database.py
    def get_db_url():
        base = os.getenv("DATABASE_URL", "postgresql://...")
        if os.getenv("DB_SSL_REQUIRED", "false").lower() == "true":
             return f"{base}?sslmode=verify-full&sslrootcert={os.getenv('DB_ROOT_CERT', './certs/server.crt')}"
        return base
    engine = create_engine(get_db_url(), ...)
    ```

### 1.2 `pg_hba.conf` Injection
- **Action**: Create `infra/postgres/pg_hba.conf` with `hostssl ... scram-sha-256`.
- **Apply**: Mount this file in BOTH `infra/docker-compose.yml` and `infra/docker-compose.prod.yml`.

## 2. Neo4j 2025 Security (PBAC)
**Context**: `services/neo4j/neo4j_service.py` manages the driver.

### 2.1 Update `Neo4jService`
- **File**: `services/neo4j/neo4j_service.py`
- **Change**:
    - Enforce specific user environment variables (`NEO4J_APP_USER`) instead of defaulting to `neo4j`.
    - Set `encrypted=True` and `trust=TRUST_SYSTEM_CA_SIGNED_CERTIFICATES` (or custom CA) in the driver config.

### 2.2 Role Application
- **Script**: `scripts/db/setup_neo4j_roles.py`
    - Creates `fastapi_user`.
    - Assigns `architect` role.
    - run `DENY WRITE ON GRAPH neo4j NODES System TO architect` (example PBAC).

## 3. Redis 8 ACLs (App-Wide)
**Context**: Redis is used in `web/app.py` (Flask-SocketIO), `services/system/cache_service.py`, and `services/caching/performance_cache.py`.

### 3.1 ACL File Creation
- **File**: `infra/redis/users.acl`
    ```text
    user default off
    user admin on >ADMIN_PASS ~* +@all
    user app_user on >APP_PASS ~cache:* ~session:* +@read +@write
    user queue_user on >QUEUE_PASS ~celery:* +@all
    ```

### 3.2 Updating Usages
1.  **`config/redis_config.json`**: Add `"username": "app_user"` field.
2.  **`web/app.py`**: Update `redis_url` string interpolation to include `:{password}@{host}` -> `{username}:{password}@{host}`.
3.  **`services/system/cache_service.py`**:
    - Audit how it connects. If it uses `redis.Redis(...)`, inject `username="app_user"`.
4.  **`services/caching/performance_cache.py`**:
    - Same audit. Ensure it loads credentials from `config/redis_config.json` or `os.getenv` and NOT hardcoded defaults.

## 4. Verification Plan
### 4.1 Application Connectivity Check
- **Context**: Must verify *every* service type.
- **Command**: `python cli.py verify-pipeline`
- **Success Criteria**:
    - Pipeline runs without "Authentication Failed" errors.
    - Logs show successful SSL handshakes.

### 4.2 Security Negative Testing
- **Script**: `scripts/tests/verify_db_security.py`
    - **Test 1**: Connect to PG with `sslmode=disable` -> Must Raise ConnectionError.
    - **Test 2**: Connect to Neo4j as `neo4j` (admin) with default pass -> Must Fail (if password rotated).
    - **Test 3**: Connect to Redis as `default` user -> Must Fail (User is `off`).

## 5. Files to Create/Modify
- [NEW] [infra/postgres/pg_hba.conf](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/infra/postgres/pg_hba.conf)
- [NEW] [infra/redis/users.acl](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/infra/redis/users.acl)
- [MODIFY] [config/database.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/config/database.py)
- [MODIFY] [services/neo4j/neo4j_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/neo4j/neo4j_service.py)
- [MODIFY] [web/app.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/web/app.py)
- [MODIFY] [services/system/cache_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/system/cache_service.py)
- [MODIFY] [services/caching/performance_cache.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/caching/performance_cache.py)
