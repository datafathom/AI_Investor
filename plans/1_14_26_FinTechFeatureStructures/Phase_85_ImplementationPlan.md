# Phase 85: Unified API Gateway & Rate Limiter

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Architecture Team

---

## 📋 Overview

**Description**: Centralize all external API calls (Brokerage, Data, Crypto) through a single Gateway. Handle Rate Limiting, Caching, and Circuit Breaking here. Prevent "API Ban" due to excessive polling.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 85

---

## 🎯 Sub-Deliverables

### 85.1 Redis Rate Limiter Implementation `[ ]`

**Acceptance Criteria**: Middleware limiting calls per provider. (e.g., AlphaVantage: 5 calls/min). Queue or reject excess.

| Component | File Path | Status |
|-----------|-----------|--------|
| Limiter | `services/middleware/rate_limiter.py` | `[ ]` |

---

### 85.2 Centralized Request Caching `[ ]`

**Acceptance Criteria**: Cache responses. If 5 agents ask for "AAPL Price" in 1 second, make 1 API call and serve 5 cached responses.

| Component | File Path | Status |
|-----------|-----------|--------|
| Cache Layer | `services/middleware/cache_layer.py` | `[ ]` |

---

### 85.3 Failover Logic (Circuit Breaker) `[ ]`

**Acceptance Criteria**: If Primary Data Provider fails (500 errors), switch to Backup Provider automatically.

| Component | File Path | Status |
|-----------|-----------|--------|
| Failover | `services/middleware/failover.py` | `[ ]` |

---

### 85.4 API Usage Analytics Dashboard `[ ]`

**Acceptance Criteria**: Visualize API usage. "You have used 80% of your OpenAI quota."

| Component | File Path | Status |
|-----------|-----------|--------|
| Usage Dash | `frontend2/src/components/Admin/ApiUsage.jsx` | `[ ]` |

### 85.5 Credential Manager (Vault) `[ ]`

**Acceptance Criteria**: Secure storage for all API keys. Inject into Gateway at runtime.

| Component | File Path | Status |
|-----------|-----------|--------|
| Vault | `services/security/key_vault.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py gateway status` | Show quotas | `[ ]` |
| `python cli.py gateway flush-cache` | Clear redis | `[ ]` |

---

*Last verified: 2026-01-25*
