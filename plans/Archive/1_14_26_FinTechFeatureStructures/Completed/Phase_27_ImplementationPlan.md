# Phase 27: The Warden’s Routine Automation

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Architecture Team

---

## 📋 Overview

**Description**: Automate recurring health checks for liquidity, volatility, and equilibrium (The Warden's Routine). This is the heartbeat of the self-correcting system. A cron-based microservice verifies "Environmental Conditions" every 5 minutes.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 27

---

## 🎯 Sub-Deliverables

### 27.1 Cron Health Check Microservice `[x]`

**Acceptance Criteria**: Scheduler service (APScheduler or Celery Beat) triggering checks every 5 minutes. Must be robust and separate from trade execution loops.

```python
class WardenRoutine:
    @every(minutes=5)
    def perform_health_check(self):
        self.check_liquidity()
        self.check_volatility()
        self.check_margin()
        self.save_report()
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Scheduler | `services/warden/scheduler.py` | `[x]` |
| Routine Runner | `services/warden/routine_runner.py` | `[x]` |

---

### 27.2 Liquidity Depth Checker `[x]`

**Acceptance Criteria**: Check real-time liquidity depth via Kafka telemetry for all assets with open exposure. If depth drops (thin market), flag "Liquidity Risk".

| Component | File Path | Status |
|-----------|-----------|--------|
| Depth Checker | `services/market/depth_check.py` | `[x]` |

---

### 27.3 Volatility Boundary Monitor (VIX/ATR) `[x]`

**Acceptance Criteria**: Ensure mathematical boundaries for system-wide volatility are not breached. If VIX > 40, Warden declares "Defensive Capital Shielding".

| Component | File Path | Status |
|-----------|-----------|--------|
| Vol Monitor | `services/market/vol_boundary.py` | `[x]` |

---

### 27.4 'Defensive Capital Shielding' Flag `[x]`

**Acceptance Criteria**: A global system state stored in Redis. `SHIELD_MODE = TRUE`. Agents check this before trading.

| Component | File Path | Status |
|-----------|-----------|--------|
| Shield Logic | `services/modes/shield_logic.py` | `[x]` |

---

### 27.5 UnifiedActivityService Health Log `[x]`

**Acceptance Criteria**: Persist the result of every 'Warden Health Check' in the `UnifiedActivityService` table for the daily report.

| Component | File Path | Status |
|-----------|-----------|--------|
| Logger | `services/logging/health_log.py` | `[x]` |

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py warden run-check` | Manual triggering | `[x]` |
| `python cli.py warden status` | Show latest health | `[x]` |

---

*Last verified: 2026-01-25*
