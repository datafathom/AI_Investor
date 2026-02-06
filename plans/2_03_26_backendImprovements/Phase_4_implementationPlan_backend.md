# Phase 4: Application Security & Framework Modernization (Implementation Plan)

**Goal**: Harden the application layer against abuse by placing the *entire* legacy FastAPI application behind a modern FastAPI Gateway, ensuring app-wide Rate Limiting, CORS, and Headers.

## 1. Hybrid Architecture Consolidation (App-Wide)
**Context**: `web/app.py` registers 100+ blueprints. We must not "pick and choose". We will mount the *entire* FastAPI WSGI app inside FastAPI.

### 1.1 `web/fastapi_gateway.py` Refactor (The "Outer Shell")
- **Action**: Transform this file into the single entry point.
- **Code Structure**:
    ```python
    # web/fastapi_gateway.py
    from fastapi import FastAPI
    from fastapi.middleware.wsgi import WSGIMiddleware
    from web.app import create_app # The factory

    # 1. Create the Legacy App
    fastapi_app, socketio = create_app()

    # 2. Create the Modern App
    app = FastAPI(title="AI Investor Gateway")

    # 3. Mount Legacy App at Root
    # This ensures EVERY route defined in web/app.py (blueprints list below) is accessible
    app.mount("/fastapi", WSGIMiddleware(fastapi_app)) # Or root "/" if we handle routing carefully
    ```
- **Routing Strategy**:
    - **Option A (Safe)**: Mount FastAPI at `/v1` or root `/`, and let FastAPI handle specific high-performance routes *before* falling back to FastAPI.
    - **Decision**: Mount FastAPI at root `"/"`. FastAPI routes take precedence. If a request matches a FastAPI route, it's handled there. If not, it falls through to FastAPI (WSGI).

### 1.2 Explicit Blueprint Coverage
**Confirmation**: The following 100+ blueprints currently in `web/app.py` will automatically be secured behind the FastAPI Gateway's Middleware stack:
- `dashboard_bp`, `auth_bp`, `market_data_bp`, `trade_bp`... (and 90+ others).
- **Verification**: We do *not* need to migrate them one-by-one yet. The Mount strategy covers them all immediately.

## 2. Strict CORS & Trusted Host (App-Wide)
**Context**: Applying middleware to `app = FastAPI()` protects *everything* inside it, including the mounted FastAPI app.

### 2.1 Configuration
- **File**: `web/fastapi_gateway.py`
- **Origins**:
    - `http://localhost:5173` (Frontend Dev)
    - `http://127.0.0.1:5173`
    - `https://app.aiinvestor.com` (Prod)
- **Middleware**:
    ```python
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"], 
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=...)
    ```
- **Cleanup**: Remove `CORS(app)` from `web/app.py` to avoid double-CORS issues, OR ensure they are compatible. *Recommendation: Remove FastAPI-CORS and let FastAPI handle it at the edge.*

## 3. Rate Limiting (App-Wide)
**Context**: We need to protect specific heavy endpoints and provide a global blanket.

### 3.1 Global Limit
- **Action**: Apply `FastAPILimiter` to the FastAPI app.
- **Note**: This *might* not strictly apply to the `WSGIMiddleware` mounted routes depending on how `fastapi-limiter` hooks in (usually dependency injection).
- **Fallback**: Keep `services.system.security_gateway` (FastAPI-Limiter) for the FastAPI routes inner layer, BUT configure it to use the *same* Redis backend as the outer layer.

## 4. Async Audit (Targeted Services)
**Context**: We identified specific services performing I/O.
- **Audit Targets**:
    - `services/neo4j/neo4j_service.py` (Verify `execute_query` effectively utilizes internal threading or change to `async_driver` if high volume).
    - `web/api/market_data_api.py` (Likely heavy reliance on external requests).
- **Action**: For any *new* FastAPI route, use `async def`. For mounted FastAPI routes, do *not* change `def` to `async def` inside FastAPI (it breaks WSGI).

## 5. Files to Create/Modify
- [MODIFY] [web/fastapi_gateway.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/web/fastapi_gateway.py) (The Master Entry Point)
- [MODIFY] [web/app.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/web/app.py) (Remove conflicting CORS/Server startup logic, expose factory only)
- [MODIFY] [config/cli_configuration.json](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/config/cli_configuration.json) (Point `start-backend` to `web.fastapi_gateway:app` via uvicorn)
