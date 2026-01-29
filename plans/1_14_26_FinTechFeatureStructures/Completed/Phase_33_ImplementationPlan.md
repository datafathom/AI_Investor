# Phase 33: The 1% Risk Rule Verification Suite

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: QA & Compliance Team

---

## 📋 Overview

**Description**: Execute a suite of stress tests to ensure the 1% position sizing rule is unbreachable by any system agent. This is "Chaos Engineering" for risk. We intentionally try to break the rules to prove the safeguards work.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 33

---

## 🎯 Sub-Deliverables

### 33.1 Automated 'Breach Attempt' Script `[x]`

**Acceptance Criteria**: Script that attempts to place trades sizing 2%, 5%, 10% risk via the API. Verify 100% rejection rate.

```python
class BreachTest:
    def run(self):
        for risk in [0.02, 0.05, 0.10]:
            response = self.api.place_order(risk_pct=risk)
            assert response.status == 400
            assert "RiskLimitExceeded" in response.error
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Test Script | `tests/stress/break_risk_rules.py` | `[x]` |

---

### 33.2 'Fat-Finger' Input Fuzzer `[x]`

**Acceptance Criteria**: Test 'Fat-Finger' error prevention by injecting invalid or extreme size inputs (e.g., lots=1000, lots=-5).

| Component | File Path | Status |
|-----------|-----------|--------|
| Fuzzer | `tests/fuzzing/order_fuzzer.py` | `[x]` |

---

### 33.3 Aggregate Risk Verification `[x]`

**Acceptance Criteria**: Ensure the 1% limit applies to *total aggregate risk* across all open positions. If I have 10 positions each risking 0.1%, can I add another risking 0.5%? (Limit is usually per-trade, but Total Risk might also have a cap like 5%).

| Component | File Path | Status |
|-----------|-----------|--------|
| Aggregate Test | `tests/stress/aggregate_risk.py` | `[x]` |

---

### 33.4 Balance Scaling Verification `[x]`

**Acceptance Criteria**: Verify the system automatically scales down positions if account balance drops. If I lose 10%, my next 1% trade must be smaller in absolute $ terms.

| Component | File Path | Status |
|-----------|-----------|--------|
| Scaling Test | `tests/stress/balance_scaling.py` | `[x]` |

---

### 33.5 Compliance Certificate Generator `[x]`

**Acceptance Criteria**: Produce a PDF compliance certificate verifying the 1% Rule enforcement for the system audit.

| Component | File Path | Status |
|-----------|-----------|--------|
| Report Gen | `services/reporting/compliance_cert.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py stress run-breach` | Run valid. suite | `[x]` |
| `python cli.py stress generate-cert` | PDF report | `[x]` |

---

*Last verified: 2026-01-25*
