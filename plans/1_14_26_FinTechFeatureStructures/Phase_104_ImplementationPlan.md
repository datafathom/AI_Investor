# Phase 104: Defined Contribution vs. Pension History Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Retirement Planning Team

---

## 📋 Overview

**Description**: Build a comprehensive engine to track, compare, and optimize both defined contribution (401k) and defined benefit (pension) retirement accounts, including employer matching logic and contribution limit enforcement.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 104.1 Employer Matching Schema (5-7% Range) `[ ]`

**Acceptance Criteria**: Create a Postgres schema to store employer matching configurations including percentage ranges, vesting schedules, and matching caps.

#### Database Schema

```sql
CREATE TABLE employer_match_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    employer_name VARCHAR(255) NOT NULL,
    
    -- Matching Formula
    match_type VARCHAR(20) NOT NULL,        -- DOLLAR_FOR_DOLLAR, PARTIAL, TIERED
    match_percentage DECIMAL(5, 2) NOT NULL, -- e.g., 50% = 0.50
    max_match_percentage DECIMAL(5, 2),      -- Max % of salary matched
    annual_match_cap DECIMAL(20, 2),         -- Dollar cap on match
    
    -- Tiered Matching (if applicable)
    tier_1_employee_pct DECIMAL(5, 2),       -- e.g., First 3%
    tier_1_employer_pct DECIMAL(5, 2),       -- e.g., 100% match
    tier_2_employee_pct DECIMAL(5, 2),       -- e.g., Next 2%
    tier_2_employer_pct DECIMAL(5, 2),       -- e.g., 50% match
    
    -- Vesting Schedule
    vesting_type VARCHAR(20),                -- IMMEDIATE, CLIFF, GRADED
    vesting_cliff_months INTEGER,
    vesting_schedule JSONB,                  -- {"12": 0.20, "24": 0.40, ...}
    
    -- Status
    effective_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE contribution_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    account_id UUID NOT NULL,
    contribution_date DATE NOT NULL,
    
    -- Contribution Details
    employee_contribution DECIMAL(20, 2) NOT NULL,
    employer_match DECIMAL(20, 2) NOT NULL,
    total_contribution DECIMAL(20, 2) GENERATED ALWAYS AS 
        (employee_contribution + employer_match) STORED,
    
    -- Running Totals (YTD)
    ytd_employee_total DECIMAL(20, 2),
    ytd_employer_total DECIMAL(20, 2),
    ytd_total DECIMAL(20, 2),
    
    -- Limits
    annual_limit DECIMAL(20, 2),           -- IRS limit for year
    remaining_room DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('contribution_history', 'contribution_date');
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/104_employer_match.sql` | `[ ]` |
| Match Config Model | `models/employer_match.py` | `[ ]` |
| Contribution Model | `models/contribution.py` | `[ ]` |
| Match Calculator Service | `services/retirement/match_calculator.py` | `[ ]` |
| Vesting Engine | `services/retirement/vesting_engine.py` | `[ ]` |
| API Endpoint | `web/api/retirement/match.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Match Config Form | `frontend2/src/components/Retirement/MatchConfigForm.jsx` | `[ ]` |
| Vesting Schedule Display | `frontend2/src/components/Retirement/VestingSchedule.jsx` | `[ ]` |
| Match Visualization | `frontend2/src/components/Charts/MatchVisualization.jsx` | `[ ]` |
| useEmployerMatch Hook | `frontend2/src/hooks/useEmployerMatch.js` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Match Calculator | `tests/unit/test_match_calculator.py` | `[ ]` |
| Unit: Vesting Engine | `tests/unit/test_vesting_engine.py` | `[ ]` |
| Integration: Match API | `tests/integration/test_match_api.py` | `[ ]` |
| E2E: Config Form | `tests/e2e/test_match_config_form.py` | `[ ]` |

---

### 104.2 Maximum Matching Limit Calculator `[ ]`

**Acceptance Criteria**: Implement a calculator that determines the optimal employee contribution percentage to capture the maximum employer match without over-contributing.

#### Backend Implementation

```python
class MaxMatchCalculator:
    """
    Calculate optimal contribution to maximize employer match.
    
    Example:
    - Salary: $100,000
    - Employer matches 100% of first 3% + 50% of next 2%
    - Optimal contribution: 5% = $5,000/year
    - Total match received: $4,000/year (3% + 1% = 4%)
    """
    
    def calculate_optimal_contribution(
        self, 
        salary: Decimal, 
        match_config: EmployerMatchConfig
    ) -> OptimalContributionResult:
        """Calculate the contribution % to maximize match."""
        pass
    
    def calculate_match_shortfall(
        self, 
        current_contribution_pct: Decimal,
        salary: Decimal,
        match_config: EmployerMatchConfig
    ) -> MatchShortfallResult:
        """Calculate how much match is being left on the table."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Max Match Calculator | `services/retirement/max_match_calculator.py` | `[ ]` |
| Shortfall Analyzer | `services/retirement/shortfall_analyzer.py` | `[ ]` |
| Optimization Service | `services/retirement/contribution_optimizer.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Match Optimizer Widget | `frontend2/src/components/Retirement/MatchOptimizer.jsx` | `[ ]` |
| Shortfall Alert | `frontend2/src/components/Alerts/MatchShortfallAlert.jsx` | `[ ]` |
| Contribution Slider | `frontend2/src/components/Retirement/ContributionSlider.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Max Calculator | `tests/unit/test_max_match_calculator.py` | `[ ]` |
| Unit: Shortfall | `tests/unit/test_shortfall_analyzer.py` | `[ ]` |
| Integration: Optimization | `tests/integration/test_contribution_optimizer.py` | `[ ]` |

---

### 104.3 Defined Benefit vs. 401k Data Bridge `[ ]`

**Acceptance Criteria**: Create a data bridge that normalizes pension (DB) and 401k (DC) data into a unified retirement income projection model.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Data Bridge | `services/retirement/db_dc_bridge.py` | `[ ]` |
| Pension Normalizer | `services/retirement/pension_normalizer.py` | `[ ]` |
| DC Normalizer | `services/retirement/dc_normalizer.py` | `[ ]` |
| Unified Projector | `services/retirement/unified_projector.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Unified Dashboard | `frontend2/src/components/Retirement/UnifiedDashboard.jsx` | `[ ]` |
| Comparison Chart | `frontend2/src/components/Charts/DBvsDCChart.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Bridge | `tests/unit/test_db_dc_bridge.py` | `[ ]` |
| Unit: Normalizers | `tests/unit/test_pension_normalizer.py` | `[ ]` |
| Integration: Projections | `tests/integration/test_unified_projections.py` | `[ ]` |

---

### 104.4 IRS Contribution Limit Kafka Consumer `[ ]`

**Acceptance Criteria**: Configure a Kafka consumer to ingest annual IRS contribution limit updates and automatically apply them to user accounts.

#### IRS Limits Configuration

| Year | 401k Limit | Catch-up (50+) | IRA Limit | Catch-up (50+) |
|------|------------|----------------|-----------|----------------|
| 2025 | $23,500 | $7,500 | $7,000 | $1,000 |
| 2026 | $24,000 | $8,000 | $7,500 | $1,000 |

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| IRS Limits Consumer | `services/kafka/irs_limits_consumer.py` | `[ ]` |
| Limit Validator | `services/retirement/limit_validator.py` | `[ ]` |
| Limit Config | `config/irs_contribution_limits.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Limit Progress Bar | `frontend2/src/components/Retirement/LimitProgressBar.jsx` | `[ ]` |
| Catch-up Indicator | `frontend2/src/components/Retirement/CatchUpIndicator.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Limit Validator | `tests/unit/test_limit_validator.py` | `[ ]` |
| Integration: Kafka Consumer | `tests/integration/test_irs_limits_kafka.py` | `[ ]` |

---

### 104.5 Neo4j Restricted Investment Options Mapping `[ ]`

**Acceptance Criteria**: Map 401k plan investment options (often limited) in Neo4j to enable comparison against unrestricted IRA options.

#### Neo4j Schema

```cypher
// Retirement Account Nodes
(:RETIREMENT_ACCOUNT {
    id: "uuid",
    type: "401K",  // 401K, IRA, ROTH_IRA, PENSION
    provider: "Fidelity",
    plan_name: "Company 401k Plan"
})

// Investment Option Nodes
(:INVESTMENT_OPTION {
    id: "uuid",
    ticker: "FXAIX",
    name: "Fidelity 500 Index Fund",
    expense_ratio: 0.015,
    asset_class: "LARGE_CAP_US"
})

// Relationships
(:RETIREMENT_ACCOUNT)-[:OFFERS {
    is_default: true,
    min_allocation: 0,
    max_allocation: 100
}]->(:INVESTMENT_OPTION)

(:INVESTMENT_OPTION)-[:SIMILAR_TO {
    correlation: 0.98,
    expense_diff: -0.01
}]->(:INVESTMENT_OPTION)
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Options Mapper | `services/neo4j/investment_options_mapper.py` | `[ ]` |
| Similarity Analyzer | `services/retirement/option_similarity.py` | `[ ]` |
| Graph Queries | `services/neo4j/retirement_queries.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Options Comparison | `frontend2/src/components/Retirement/OptionsComparison.jsx` | `[ ]` |
| Graph Visualizer | `frontend2/src/components/Neo4j/InvestmentOptionsGraph.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Options Mapper | `tests/unit/test_investment_options_mapper.py` | `[ ]` |
| Unit: Similarity | `tests/unit/test_option_similarity.py` | `[ ]` |
| Integration: Neo4j | `tests/integration/test_retirement_neo4j.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 104.1 Employer Matching Schema | `[ ]` | `[ ]` |
| 104.2 Max Match Calculator | `[ ]` | `[ ]` |
| 104.3 DB vs. DC Bridge | `[ ]` | `[ ]` |
| 104.4 IRS Limits Consumer | `[ ]` | `[ ]` |
| 104.5 Neo4j Options Mapping | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py retirement match-config` | View match config | `[ ]` |
| `python cli.py retirement optimize` | Optimize contribution | `[ ]` |
| `python cli.py retirement limits` | Show IRS limits | `[ ]` |
| `python cli.py retirement compare` | Compare DB vs. DC | `[ ]` |

---

*Last verified: 2026-01-25*
