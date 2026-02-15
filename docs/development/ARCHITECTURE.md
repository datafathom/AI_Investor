# AI Investor Architecture

> **Last Updated**: 2026-02-14

## System Overview

AI Investor (Sovereign OS) is a full-stack autonomous investment platform with an 18-department AI workforce, 125+ frontend workstation pages, and 133 backend service modules.

## High-Level Architecture

```
┌────────────────────┐
│   Frontend (React)  │   React 19 + Vite 5
│   Port: 5173        │   125+ workstation pages
│   Tailwind + shadcn │   18 department dashboards
└─────────┬──────────┘
          │  HTTP / WebSocket / Socket.io
          │  Proxied via vite.config.js
┌─────────▼──────────┐
│   Backend (FastAPI)  │   Python 3.11+ / FastAPI
│   Port: 5050         │   133 service modules
└─────────┬──────────┘
          │
          ├───► PostgreSQL (TimescaleDB)
          ├───► Neo4j (Graph Database)
          ├───► Redis (Caching)
          ├───► Kafka (Event Streaming)
          └───► External APIs
```

## Technology Stack

### Frontend

| Layer | Technology |
|-------|-----------|
| Framework | React 19 |
| Build Tool | Vite 5 |
| Routing | React Router 6 + `DynamicWorkstation` (auto-loaded via `import.meta.glob`) |
| State Management | Zustand stores + React Context |
| UI Components | shadcn/ui (source-owned) + Radix UI primitives |
| Styling | Tailwind CSS + `cn()` utility (`clsx` + `tailwind-merge`) |
| Icons | Lucide React |
| Animations | Framer Motion |
| 3D Visualization | Three.js + React Three Fiber |
| Charts | Recharts |

### Backend

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI |
| CLI Orchestration | `cli.py` (command registry in `config/cli_configuration.json`) |
| Services | 133 modules in `services/` using singleton pattern |
| Database ORM | SQLAlchemy / Direct PostgreSQL |
| Graph Database | Neo4j (lazy-loaded connections) |
| Cache | Redis |
| Message Queue | Kafka |
| Testing | pytest |

### Infrastructure

| Layer | Technology |
|-------|-----------|
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Error Tracking | Sentry |
| Notifications | Slack Bot integration |

---

## Frontend Architecture

### Department System

The frontend is organized around **18 departments**, each with its own dashboard and set of workstation pages:

| ID | Department | Slug | Workstation Pages |
|----|-----------|------|------------------|
| 1 | Orchestrator | `orchestrator` | Fleet, Singularity, System Health, etc. |
| 2 | Data Scientist | `data-scientist` | Backtest Engine, Crypto Analytics, etc. |
| 3 | Strategist | `strategist` | Strategy Lab, Risk Dashboard, etc. |
| 4 | Trader | `trader` | Order Management, Smart Router, etc. |
| 5 | Physicist | `physicist` | Greeks Surface, PnL Modeler, etc. |
| 6 | Hunter | `hunter` | Opportunity Tracker, Watchlist, etc. |
| 7 | Sentry | `sentry` | Security Center, Fraud Center, etc. |
| 8 | Steward | `steward` | Asset Inventory, Exit Planner, etc. |
| 9 | Guardian | `guardian` | Portfolio Guardian, etc. |
| 10 | Architect | `architect` | Legacy Planning, Tax Strategy, etc. |
| 11 | Lawyer | `lawyer` | Compliance, Filing Manager, etc. |
| 12 | Auditor | `auditor` | Attribution, Fee Auditor, etc. |
| 13 | Envoy | `envoy` | Philanthropy, Impact Scorecard, etc. |
| 14 | Front Office | `front-office` | Executive Summary |
| 15 | Historian | `historian` | Timeline, Archive |
| 16 | Stress Tester | `stress-tester` | Black Swan, Crash Simulator, etc. |
| 17 | Refiner | `refiner` | AutoCoder, Evolution, etc. |
| 18 | Banker | `banker` | Treasury, Crypto Wallet, etc. |

### Routing Architecture

```
departmentRegistry.js  ──────►  MenuBar.jsx (navigation)
        │                              │
        │                              │ User clicks link
        │                              ▼
        │                      React Router
        │                      /:deptSlug/:subSlug
        │                              │
        │                              ▼
        │                      DynamicWorkstation
        │                              │
        │                              ▼
        └──────────────────►  import.meta.glob()
                              pages/workstations/**/*.jsx
                              (auto-discovers 125+ files)
```

- **`departmentRegistry.js`** — Central config defining all departments and their sub-modules
- **`DynamicWorkstation`** — Dynamic component loader using 3-strategy file matching
- **`import.meta.glob`** — Vite's lazy-import system for automatic file discovery

See `docs/frontend/routes/dynamic_workstation_routing.md` for details.

### Component System

UI components follow the **shadcn/ui** pattern — source-owned components using Radix UI primitives:

```
Frontend/src/components/ui/
├── alert.jsx          ← Native HTML + cn()
├── alert-dialog.jsx   ← @radix-ui/react-alert-dialog
├── avatar.jsx         ← @radix-ui/react-avatar
├── button.jsx         ← Native HTML + cn()
├── card.jsx           ← Native HTML + cn()
├── dialog.jsx         ← @radix-ui/react-dialog
├── select.jsx         ← @radix-ui/react-select
├── slider.jsx         ← @radix-ui/react-slider
├── switch.jsx         ← @radix-ui/react-switch
└── ... (15+ components)
```

See `docs/frontend/components/shadcn_ui_component_system.md` for the full inventory.

---

## Backend Architecture

### CLI Orchestration

All development and operational commands route through `cli.py`:

```
cli.py
  │
  ├── config/cli_configuration.json   (command registry)
  │
  └── scripts/runners/
        ├── dev_runner.py             (full stack startup)
        ├── dev_no_db_runner.py       (no-database mode)
        ├── frontend_verify_runner.py (browser verification)
        └── ... (118+ runner scripts)
```

### Service Layer

Backend services use the singleton pattern with lazy-loaded connections:

```python
class MyService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

All 133 services are in `services/` and are documented in `docs/services/`.

### API Gateway

FastAPI serves as the unified API gateway at `web/fastapi_gateway.py`, exposing REST endpoints on port 5050. The Vite dev server proxies `/api/*` requests to this gateway.

---

## Data Flow

### Standard Request

1. User interacts with a department workstation page
2. Page calls a typed service function in `Frontend/src/services/`
3. Service sends HTTP request via `apiClient` to `/api/...`
4. Vite proxy forwards to FastAPI on port 5050
5. FastAPI routes to the appropriate backend service
6. Service queries databases (PostgreSQL, Neo4j, Redis)
7. JSON response flows back through the chain
8. React component updates via Zustand store

### Real-Time Updates

1. Backend service generates event
2. Event published to Kafka topic or Socket.io
3. Frontend receives update via WebSocket connection
4. Zustand store updates, triggering component re-render

---

## Database Schema

### PostgreSQL (Primary)

| Category | Tables |
|----------|--------|
| Core | `users`, `portfolios`, `positions`, `orders`, `transactions` |
| Features | `user_workspaces`, `legal_documents`, `user_onboarding`, `user_preferences` |
| Compliance | `rule_144a_holdings`, `lockup_expirations` |

### Neo4j (Graph)

| Nodes | Relationships |
|-------|--------------|
| Stocks, Users, Portfolios, Strategies | OWNS, CONTAINS, CORRELATES_WITH, FOLLOWS |

---

## Security

| Layer | Implementation |
|-------|---------------|
| Authentication | JWT tokens with refresh token rotation |
| Authorization | Role-Based Access Control (RBAC) |
| API Keys | Managed via Sentry department |
| Network | All servers bind to `127.0.0.1` (never `0.0.0.0`) |
| Secrets | `.env` file, never logged or printed |
| Input Validation | Pydantic models on all endpoints |

---

## Key Documentation Cross-References

| Topic | Document |
|-------|----------|
| UI Components | `docs/frontend/components/shadcn_ui_component_system.md` |
| Dynamic Routing | `docs/frontend/routes/dynamic_workstation_routing.md` |
| Department Registry | `docs/frontend_special/department_registry_deep_dive.md` |
| Vite Build Config | `docs/frontend/vite_build_configuration.md` |
| CJS/ESM Interop | `docs/frontend/frontend_docs/cjs_esm_interop_reference.md` |
| CLI Commands | `docs/cli/CLI_USAGE_GUIDE.md` |
| Backend Services | `docs/services/` (133 service docs) |
| Admin Route Migration | `docs/frontend/routes/admin_route_migration_reference.md` |
