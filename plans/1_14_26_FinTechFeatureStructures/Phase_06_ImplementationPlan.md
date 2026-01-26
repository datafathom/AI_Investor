# Phase 6: Demo Account Infrastructure Provisioning

> **Status**: `[/]` In Progress  
> **Last Updated**: 2026-01-25  
> **Owner**: Integration Team

---

## 📋 Overview

**Description**: Set up the simulation layer for 'paper money' trading to prevent capital erosion during the development phase.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 6.1 Demo Broker API Integration `[/]`

**Acceptance Criteria**: Integrate with IC Markets or Vantage demo APIs to facilitate simulated trade execution.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Demo Broker Client | `services/brokers/demo_broker.py` | `[/]` |
| Trade Executor (Demo) | `services/trade_executor_demo.py` | `[ ]` |
| API Adapter | `services/brokers/adapters/ic_markets.py` | `[ ]` |

#### API Configuration

| Setting | Value | Status |
|---------|-------|--------|
| Demo API URL | `https://demo-api.icmarkets.com` | `[/]` |
| Auth Method | API Key + Secret | `[ ]` |
| Rate Limit | 100 req/min | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Demo Broker | `tests/unit/test_demo_broker.py` | `[ ]` |
| Integration: Trade Flow | `tests/integration/test_demo_trade.py` | `[ ]` |

---

### 6.2 is_demo Flag Implementation `[ ]`

**Acceptance Criteria**: Implement a `is_demo` flag within the `portfolioStore` to strictly isolate simulated funds from future live capital.

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Portfolio Store | `frontend2/src/stores/portfolioStore.js` | `[ ]` |
| Demo Mode Context | `frontend2/src/context/DemoModeContext.jsx` | `[ ]` |
| Demo Indicator | `frontend2/src/components/DemoIndicator.jsx` | `[ ]` |

#### Store Schema

```javascript
// portfolioStore.js
const usePortfolioStore = create((set, get) => ({
    // Demo isolation flag
    is_demo: true,  // Default to demo mode
    
    // Separate balances
    demo_balance: 100000.00,
    live_balance: 0.00,
    
    // Current mode balance
    get balance() {
        return this.is_demo ? this.demo_balance : this.live_balance;
    },
    
    // Toggle mode (requires confirmation for live)
    toggleDemoMode: (confirm) => {
        if (!get().is_demo && !confirm) {
            throw new Error('Live mode requires explicit confirmation');
        }
        set({ is_demo: !get().is_demo });
    },
}));
```

---

### 6.3 Market Tuition Logging `[ ]`

**Acceptance Criteria**: Ensure that demo account losses are recorded as 'Market Tuition' within the Postgres journal without affecting net worth.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Market Tuition Logger | `services/market_tuition_logger.py` | `[ ]` |
| Loss Categorizer | `services/loss_categorizer.py` | `[ ]` |

#### Database Schema

```sql
CREATE TABLE market_tuition_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    trade_id UUID NOT NULL,
    loss_amount DECIMAL(20, 8) NOT NULL,
    lesson_category VARCHAR(50),  -- e.g., 'STOP_LOSS_TOO_TIGHT', 'WRONG_DIRECTION'
    agent_id VARCHAR(100),
    notes TEXT,
    is_demo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_tuition_timestamp ON market_tuition_log(timestamp);
```

---

### 6.4 System Reset Function `[ ]`

**Acceptance Criteria**: Create a 'System Reset' function to revert the demo account to initial balance for iterative strategy testing.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Demo Reset Service | `services/demo_reset_service.py` | `[ ]` |
| Reset API Endpoint | `web/api/demo/reset.py` | `[ ]` |

#### Reset Logic

```python
def reset_demo_account(user_id: str, initial_balance: Decimal = Decimal("100000.00")) -> bool:
    """
    Reset demo account to initial state.
    
    Actions:
    1. Close all open demo positions
    2. Cancel all pending demo orders
    3. Reset demo balance to initial amount
    4. Clear demo trade history (optional, configurable)
    5. Log reset event to activity service
    """
    pass
```

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Reset Button | `frontend2/src/components/DemoResetButton.jsx` | `[ ]` |
| Confirmation Modal | `frontend2/src/components/modals/ResetConfirmModal.jsx` | `[ ]` |

---

### 6.5 Agent Persona Metadata `[ ]`

**Acceptance Criteria**: Log all demo transactions to the `UnifiedActivityService` with metadata identifying the active agent persona.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Agent Metadata Injector | `services/agent_metadata_injector.py` | `[ ]` |
| Transaction Logger | `services/transaction_logger.py` | `[ ]` |

#### Metadata Schema

```json
{
    "trade_id": "uuid",
    "is_demo": true,
    "agent_persona": {
        "id": "searcher-001",
        "name": "SearcherAgent",
        "type": "HUNTER",
        "confidence": 0.78
    },
    "trade_thesis": {
        "direction": "LONG",
        "logic": "Break of structure confirmed",
        "r_target": 3.0
    },
    "timestamp": "2026-01-25T21:30:00Z"
}
```

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 6.1 Demo Broker API | `[/]` | `[ ]` |
| 6.2 is_demo Flag | `[ ]` | `[ ]` |
| 6.3 Market Tuition | `[ ]` | `[ ]` |
| 6.4 System Reset | `[ ]` | `[ ]` |
| 6.5 Agent Metadata | `[ ]` | `[ ]` |

**Phase Status**: `[/]` IN PROGRESS

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py demo-reset` | Reset demo account | `[ ]` |
| `python cli.py demo-status` | Check demo account status | `[ ]` |
| `python cli.py demo-trade <pair> <side> <size>` | Execute demo trade | `[ ]` |

---

*Last verified: 2026-01-25*
