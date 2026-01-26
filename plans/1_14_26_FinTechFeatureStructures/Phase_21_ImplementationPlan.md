# Phase 21: The 3% Portfolio Freeze Circuit Breaker

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Develop the global "Circuit Breaker" to freeze all trading activity upon reaching a 3.0% daily drawdown threshold. This "Zen Mode" prevents emotional spirals and preserves the "Emergency Fund Moat". Ideally, this is implemented as a middleware layer blocking all order execution APIs.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 21

---

## 🎯 Sub-Deliverables

### 21.1 Real-Time daily_drawdown Aggregator (TimescaleDB) `[ ]`

**Acceptance Criteria**: Implement logic to aggregate daily realized and unrealized losses across all active brokerage accounts in real-time (<100ms latency).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE daily_pnl_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    snapshot_time TIMESTAMPTZ NOT NULL,
    
    start_of_day_equity DECIMAL(20, 2) NOT NULL,
    current_equity DECIMAL(20, 2) NOT NULL,
    
    -- Calculated
    realized_pnl DECIMAL(20, 2),
    unrealized_pnl DECIMAL(20, 2),
    total_drawdown_pct DECIMAL(5, 4) GENERATED ALWAYS AS (
        (start_of_day_equity - current_equity) / NULLIF(start_of_day_equity, 0)
    ) STORED,
    
    is_breached BOOLEAN GENERATED ALWAYS AS (total_drawdown_pct >= 0.03) STORED
);

SELECT create_hypertable('daily_pnl_snapshots', 'snapshot_time');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/21_circuit_breaker.sql` | `[ ]` |
| Drawdown Aggregator | `services/risk/drawdown_aggregator.py` | `[ ]` |

---

### 21.2 Portfolio Freeze 'Zen Mode' Middleware `[ ]`

**Acceptance Criteria**: Middleware that intercepts all `POST /orders` requests. If `is_breached` is true for the current day, reject with 423 Locked.

#### Backend Implementation

```python
class CircuitBreakerMiddleware:
    """
    Blocks trading if 3% drawdown is hit.
    """
    def check_breaker(self, account_id: UUID) -> bool:
        drawdown = self.risk_service.get_daily_drawdown(account_id)
        if drawdown >= 0.03:
            raise CircuitBreakerException("Zen Mode Active: -3% Limit Hit")
        return True
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Middleware | `api/middleware/circuit_breaker.py` | `[ ]` |
| Zen Mode Activator | `services/modes/zen_mode.py` | `[ ]` |

---

### 21.3 Redis 'Lock' for Trading State `[ ]`

**Acceptance Criteria**: Use Redis to persist the "Breached" state for the remainder of the trading day (expires at 00:00 UTC). This prevents database hammering.

| Component | File Path | Status |
|-----------|-----------|--------|
| Redis Lock | `services/infrastructure/redis_lock.py` | `[ ]` |

---

### 21.4 Warden Override (MFA Required) `[ ]`

**Acceptance Criteria**: Implement a 'Warden Override' requiring multi-factor biometric authentication to unfreeze the system (only in extreme emergencies).

| Component | File Path | Status |
|-----------|-----------|--------|
| MFA Service | `services/auth/mfa_service.py` | `[ ]` |
| Override Handler | `services/risk/override_handler.py` | `[ ]` |

---

### 21.5 Kafka Freeze Broadcast `[ ]`

**Acceptance Criteria**: Broadcast the freeze event to all mobile and desktop ProtectorAgent instances with high urgency.

#### Kafka Topic

```json
{
    "topic": "system-events",
    "schema": {
        "event_type": "The3PercentFreeze",
        "equity_loss": "decimal",
        "timestamp": "timestamp",
        "action": "CANCEL_ALL_OPEN_ORDERS"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Freeze Publisher | `services/kafka/freeze_publisher.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py risk check-drawdown` | Show current % | `[ ]` |
| `python cli.py risk simulate-breach` | Test circuit breaker | `[ ]` |

---

*Last verified: 2026-01-25*
