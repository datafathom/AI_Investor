# Phase 23: Postgres Risk Guardrail Schema

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Define the structured database schema for persisting and adjusting global risk parameters with full auditability. This "Configuration as Code" approach ensures risk settings (Max Risk %, Daily Limits) are versioned and cannot be silently changed by rogue agents.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 23

---

## 🎯 Sub-Deliverables

### 23.1 Risk Parameter Versioning Schema `[x]`

**Acceptance Criteria**: Create Postgres tables for Max Risk %, Daily Drawdown Limits, and Asset Kill Thresholds. Use `valid_from` / `valid_to` columns for temporal versioning.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE risk_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Parameters
    max_position_size_pct DECIMAL(5, 4) DEFAULT 0.01,  -- 1%
    daily_drawdown_limit_pct DECIMAL(5, 4) DEFAULT 0.03, -- 3%
    max_leverage_ratio DECIMAL(5, 2) DEFAULT 1.0,      -- 1x (No margin)
    
    -- Audit
    reason_for_change TEXT,
    approved_by_agent_id UUID,
    
    -- Temporal
    valid_from TIMESTAMPTZ DEFAULT NOW(),
    valid_to TIMESTAMPTZ,                              -- NULL = Current
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for finding active config
CREATE UNIQUE INDEX idx_active_config ON risk_configurations (valid_from) WHERE valid_to IS NULL;
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/23_risk_config.sql` | `[x]` |
| Config Service | `services/risk/config_manager.py` | `[x]` |

---

### 23.2 Configuration Hydrator Service (500ms poller) `[x]`

**Acceptance Criteria**: Configure the `RiskGuardrailService` to hydrate the system state from this table every 500ms (or via Postgres NOTIFY).

| Component | File Path | Status |
|-----------|-----------|--------|
| Hydrator | `services/risk/hydrator.py` | `[x]` |

---

### 23.3 Signed Log Entry for Changes `[x]`

**Acceptance Criteria**: Ensure all modifications to risk parameters require Multi-Agent consensus and a signed log entry (SHA-256).

| Component | File Path | Status |
|-----------|-----------|--------|
| Signature Generator | `services/security/audit_signer.py` | `[x]` |

---

### 23.4 SHA-256 State Hash Verification `[x]`

**Acceptance Criteria**: Generate a SHA-256 hash of the current active risk state to prevent unauthorized direct database manipulation (Tripwire).

```python
class IntegrityChecker:
    def verify_config_integrity(self, config: RiskConfig) -> bool:
        computed_hash = hashlib.sha256(json.dumps(config.dict())).hexdigest()
        stored_hash = self.db.get_last_hash()
        return computed_hash == stored_hash
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Integrity Checker | `services/security/config_integrity.py` | `[x]` |

---

### 23.5 Default 'Safe Mode' Bootstrapper `[x]`

**Acceptance Criteria**: If DB is unreachable or corrupt, system must boot into "Safe Mode" (0% Risk, Liquidate Only).

| Component | File Path | Status |
|-----------|-----------|--------|
| Bootstrapper | `services/infrastructure/safe_boot.py` | `[x]` |
| 23.X Verification | `scripts/verify_phase_23.py` | `[x]` |

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py risk get-config` | Show active params | `[ ]` |
| `python cli.py risk update-param` | Propose change | `[ ]` |

---

*Last verified: 2026-01-25*
