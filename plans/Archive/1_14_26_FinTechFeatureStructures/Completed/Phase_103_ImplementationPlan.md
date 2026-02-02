# Phase 103: Emergency Fund & Liquidity Stability Monitor

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Financial Planning Team

---

## 📋 Overview

**Description**: Build a comprehensive emergency fund monitoring system that tracks liquid cash reserves against living expenses, prevents forced portfolio liquidation during financial stress, and provides early warning alerts.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 103.1 Kafka Liquid Cash vs. Expenses Stream `[x]`

**Acceptance Criteria**: Configure a Kafka stream that compares real-time liquid cash balances against projected 12-month living expenses with sub-second updates.

#### Database Schema

```sql
CREATE TABLE emergency_fund_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Cash Reserves
    total_liquid_cash DECIMAL(20, 2) NOT NULL,
    checking_balance DECIMAL(20, 2),
    savings_balance DECIMAL(20, 2),
    money_market_balance DECIMAL(20, 2),
    
    -- Expense Tracking
    monthly_expenses DECIMAL(20, 2) NOT NULL,
    annual_expenses DECIMAL(20, 2) GENERATED ALWAYS AS (monthly_expenses * 12) STORED,
    
    -- Coverage Metrics
    months_of_coverage DECIMAL(6, 2) GENERATED ALWAYS AS (
        CASE WHEN monthly_expenses > 0 
        THEN total_liquid_cash / monthly_expenses 
        ELSE 0 END
    ) STORED,
    
    -- Risk Assessment
    coverage_tier VARCHAR(20),   -- CRITICAL, LOW, ADEQUATE, STRONG
    income_stability_score DECIMAL(5, 2),
    career_risk_factor DECIMAL(5, 2),
    
    -- Metadata
    last_calculated TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('emergency_fund_status', 'last_calculated');
CREATE INDEX idx_emergency_user ON emergency_fund_status(user_id);
```

#### Kafka Topic Schema

```json
{
    "topic": "emergency-fund-status",
    "schema": {
        "user_id": "uuid",
        "liquid_cash": "decimal",
        "monthly_expenses": "decimal",
        "months_coverage": "decimal",
        "coverage_tier": "string",
        "alert_level": "string",
        "timestamp": "timestamp"
    }
}
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/103_emergency_fund.sql` | `[x]` |
| Model | `models/emergency_fund.py` | `[x]` |
| Kafka Producer | `services/kafka/emergency_fund_producer.py` | `[x]` |
| Expense Calculator | `services/planning/expense_calculator.py` | `[x]` |
| Coverage Analyzer | `services/planning/coverage_analyzer.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Emergency Fund Widget | `frontend2/src/components/EmergencyFund/FundWidget.jsx` | `[x]` |
| Coverage Gauge | `frontend2/src/components/EmergencyFund/CoverageGauge.jsx` | `[x]` |
| Expense Breakdown | `frontend2/src/components/EmergencyFund/ExpenseBreakdown.jsx` | `[x]` |
| useEmergencyFund Hook | `frontend2/src/hooks/useEmergencyFund.js` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Model | `tests/unit/test_emergency_fund_model.py` | `[x]` |
| Unit: Calculator | `tests/unit/test_expense_calculator.py` | `[x]` |
| Unit: Analyzer | `tests/unit/test_coverage_analyzer.py` | `[x]` |
| Integration: Kafka | `tests/integration/test_emergency_fund_kafka.py` | `[x]` |
| E2E: Widget UI | `tests/e2e/test_emergency_fund_widget.py` | `[x]` |

---

### 103.2 Threshold Alert System (3 months to 3 years) `[x]`

**Acceptance Criteria**: Implement a tiered alert system that triggers warnings at key coverage thresholds: Critical (<3 months), Low (3-6 months), Adequate (6-12 months), Strong (12-36 months).

#### Alert Tier Configuration

| Tier | Coverage Range | Color | Alert Type | Actions |
|------|---------------|-------|------------|---------|
| CRITICAL | < 3 months | Red | URGENT | Block non-essential trades |
| LOW | 3-6 months | Orange | WARNING | Reduce risk exposure |
| ADEQUATE | 6-12 months | Yellow | INFO | Monitoring mode |
| STRONG | 12-24 months | Green | NONE | Full trading enabled |
| FORTRESS | 24-36 months | Blue | NONE | Zen Mode eligible |

#### Backend Implementation

```python
class EmergencyFundAlertService:
    """
    Tiered alert system for emergency fund coverage.
    
    Alert Escalation:
    1. In-app notification (all tiers)
    2. Email notification (LOW and below)
    3. SMS notification (CRITICAL only)
    4. Trading restrictions (CRITICAL only)
    """
    
    TIERS = {
        'CRITICAL': {'min': 0, 'max': 3, 'color': 'red', 'block_trades': True},
        'LOW': {'min': 3, 'max': 6, 'color': 'orange', 'block_trades': False},
        'ADEQUATE': {'min': 6, 'max': 12, 'color': 'yellow', 'block_trades': False},
        'STRONG': {'min': 12, 'max': 24, 'color': 'green', 'block_trades': False},
        'FORTRESS': {'min': 24, 'max': 36, 'color': 'blue', 'block_trades': False}
    }
    
    def evaluate_coverage(self, months: float) -> dict:
        """Determine tier and required actions."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Alert Service | `services/alerts/emergency_fund_alerts.py` | `[x]` |
| Notification Router | `services/notifications/alert_router.py` | `[x]` |
| Trade Blocker | `services/trading/coverage_blocker.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Alert Banner | `frontend2/src/components/Alerts/EmergencyFundAlert.jsx` | `[x]` |
| Tier Indicator | `frontend2/src/components/EmergencyFund/TierIndicator.jsx` | `[x]` |
| Action Suggestions | `frontend2/src/components/EmergencyFund/ActionSuggestions.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Alert Service | `tests/unit/test_emergency_fund_alerts.py` | `[x]` |
| Unit: Tier Calculation | `tests/unit/test_tier_calculation.py` | `[x]` |
| Integration: Notifications | `tests/integration/test_alert_notifications.py` | `[x]` |

---

### 103.3 Portfolio Liquidation Constraint Trigger `[x]`

**Acceptance Criteria**: Implement a constraint that blocks new investment allocations when emergency fund coverage drops below 3 months, forcing capital preservation.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidation Constraint | `services/risk/liquidation_constraint.py` | `[x]` |
| Investment Blocker | `services/trading/investment_blocker.py` | `[x]` |
| Override Handler | `services/compliance/override_handler.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Block Modal | `frontend2/src/components/Modals/LiquidationConstraintModal.jsx` | `[x]` |
| Fund Priority Guide | `frontend2/src/components/Guides/FundPriorityGuide.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Constraint | `tests/unit/test_liquidation_constraint.py` | `[x]` |
| Integration: Block Flow | `tests/integration/test_investment_block.py` | `[x]` |
| E2E: Block Modal | `tests/e2e/test_block_modal_ui.py` | `[x]` |

---

### 103.4 Dynamic Career Risk Adjustment `[x]`

**Acceptance Criteria**: Adjust recommended emergency fund size based on career risk factors including industry volatility, income stability, and job market conditions.

#### Career Risk Scoring Model

| Factor | Weight | Description |
|--------|--------|-------------|
| Industry Volatility | 25% | Sector layoff rates and cyclicality |
| Income Stability | 30% | Variable vs. fixed compensation |
| Job Market | 20% | Unemployment rate in profession |
| Company Health | 15% | Employer financial stability |
| Personal Factors | 10% | Age, skills, market demand |

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Career Risk Scorer | `services/planning/career_risk_scorer.py` | `[x]` |
| Industry Data Service | `services/external/industry_data.py` | `[x]` |
| Fund Size Adjuster | `services/planning/fund_size_adjuster.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Career Risk Form | `frontend2/src/components/Forms/CareerRiskForm.jsx` | `[x]` |
| Risk Breakdown Chart | `frontend2/src/components/Charts/CareerRiskChart.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Risk Scorer | `tests/unit/test_career_risk_scorer.py` | `[x]` |
| Unit: Size Adjuster | `tests/unit/test_fund_size_adjuster.py` | `[x]` |
| Integration: Full Pipeline | `tests/integration/test_career_risk_pipeline.py` | `[x]` |

---

### 103.5 Medical Catastrophe Simulation Engine `[x]`

**Acceptance Criteria**: Build a simulation engine that models the financial impact of medical emergencies to stress-test emergency fund adequacy.

#### Backend Implementation

```python
class MedicalCatastropheSimulator:
    """
    Simulate financial impact of medical emergencies.
    
    Scenarios:
    1. Short-term disability (3-6 months)
    2. Long-term disability (12+ months)
    3. Major surgery with recovery
    4. Chronic illness diagnosis
    5. Family member medical crisis
    """
    
    def simulate_scenario(self, scenario: str, user_profile: UserProfile) -> SimulationResult:
        """Run simulation and return financial impact."""
        pass
    
    def stress_test_fund(self, fund: EmergencyFund, scenarios: list) -> StressTestResult:
        """Stress test emergency fund against multiple scenarios."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Simulator | `services/planning/medical_catastrophe_sim.py` | `[x]` |
| Scenario Library | `config/medical_scenarios.py` | `[x]` |
| Impact Calculator | `services/planning/impact_calculator.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Simulator Interface | `frontend2/src/components/Simulator/MedicalCatastropheSim.jsx` | `[x]` |
| Scenario Selector | `frontend2/src/components/Simulator/ScenarioSelector.jsx` | `[x]` |
| Impact Visualization | `frontend2/src/components/Charts/ImpactVisualization.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Simulator | `tests/unit/test_medical_catastrophe_sim.py` | `[x]` |
| Unit: Impact Calculator | `tests/unit/test_impact_calculator.py` | `[x]` |
| Integration: Full Simulation | `tests/integration/test_catastrophe_simulation.py` | `[x]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 103.1 Kafka Expense Stream | `[x]` | `[ ]` |
| 103.2 Threshold Alerts | `[x]` | `[ ]` |
| 103.3 Liquidation Constraint | `[x]` | `[ ]` |
| 103.4 Career Risk Adjustment | `[x]` | `[ ]` |
| 103.5 Medical Catastrophe Sim | `[x]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py emergency-fund status` | Check fund status | `[x]` |
| `python cli.py emergency-fund simulate <scenario>` | Run simulation | `[x]` |
| `python cli.py emergency-fund career-risk` | Assess career risk | `[x]` |

---

## 📦 Dependencies

- Phase 3: TimescaleDB (status tracking)
- Phase 1: Redpanda Cluster (Kafka topics)

---

*Last verified: 2026-01-25*
