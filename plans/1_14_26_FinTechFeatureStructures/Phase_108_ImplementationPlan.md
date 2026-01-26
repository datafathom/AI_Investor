# Phase 108: Financial Planner Budgeting & 529 Architect

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Financial Planning Team

---

## 📋 Overview

**Description**: Build comprehensive budgeting tools for upper-middle class spending pattern analysis, combined with 529 education savings plan optimization including target date portfolio recommendations and state-specific fund validation.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Phase 8 (Financial Planner Budgeting & 529 Architect)

---

## 🎯 Sub-Deliverables

### 108.1 Spending Pattern Analyzer (Upper-Middle Class) `[ ]`

**Acceptance Criteria**: Implement a spending pattern analyzer that categorizes expenses, identifies savings opportunities, and benchmarks against upper-middle class peer groups.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE spending_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    month DATE NOT NULL,
    
    -- Core Categories
    housing DECIMAL(20, 2) DEFAULT 0,           -- Mortgage, rent, HOA
    transportation DECIMAL(20, 2) DEFAULT 0,     -- Car, gas, insurance
    food_groceries DECIMAL(20, 2) DEFAULT 0,
    food_dining DECIMAL(20, 2) DEFAULT 0,
    healthcare DECIMAL(20, 2) DEFAULT 0,
    insurance DECIMAL(20, 2) DEFAULT 0,
    
    -- Lifestyle
    education DECIMAL(20, 2) DEFAULT 0,          -- Tuition, lessons
    childcare DECIMAL(20, 2) DEFAULT 0,
    entertainment DECIMAL(20, 2) DEFAULT 0,
    travel DECIMAL(20, 2) DEFAULT 0,
    subscriptions DECIMAL(20, 2) DEFAULT 0,
    
    -- Financial
    debt_payments DECIMAL(20, 2) DEFAULT 0,
    savings_contributions DECIMAL(20, 2) DEFAULT 0,
    investments DECIMAL(20, 2) DEFAULT 0,
    
    -- Calculated
    total_spending DECIMAL(20, 2) GENERATED ALWAYS AS (
        housing + transportation + food_groceries + food_dining + 
        healthcare + insurance + education + childcare + 
        entertainment + travel + subscriptions + debt_payments
    ) STORED,
    savings_rate DECIMAL(8, 6),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('spending_categories', 'month');
CREATE INDEX idx_spending_user ON spending_categories(user_id);

CREATE TABLE spending_benchmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    income_bracket VARCHAR(50) NOT NULL,         -- $100k-$150k, $150k-$250k, etc.
    category VARCHAR(100) NOT NULL,
    benchmark_percentage DECIMAL(8, 6) NOT NULL, -- % of income
    benchmark_amount DECIMAL(20, 2),
    peer_group VARCHAR(50),                      -- UPPER_MIDDLE, HNW, UHNW
    data_source VARCHAR(100),
    year INTEGER NOT NULL
);
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/108_spending_analyzer.sql` | `[ ]` |
| Spending Model | `models/spending.py` | `[ ]` |
| Pattern Analyzer | `services/planning/spending_analyzer.py` | `[ ]` |
| Benchmark Service | `services/planning/benchmark_service.py` | `[ ]` |
| Savings Opportunity Finder | `services/planning/savings_finder.py` | `[ ]` |
| API Endpoint | `web/api/planning/spending.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Budget Dashboard | `frontend2/src/components/Budget/BudgetDashboard.jsx` | `[ ]` |
| Spending Pie Chart | `frontend2/src/components/Charts/SpendingPieChart.jsx` | `[ ]` |
| Benchmark Comparison | `frontend2/src/components/Budget/BenchmarkComparison.jsx` | `[ ]` |
| Savings Opportunities | `frontend2/src/components/Budget/SavingsOpportunities.jsx` | `[ ]` |
| useBudget Hook | `frontend2/src/hooks/useBudget.js` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Pattern Analyzer | `tests/unit/test_spending_analyzer.py` | `[ ]` |
| Unit: Benchmark Service | `tests/unit/test_benchmark_service.py` | `[ ]` |
| Unit: Savings Finder | `tests/unit/test_savings_finder.py` | `[ ]` |
| Integration: Spending API | `tests/integration/test_spending_api.py` | `[ ]` |
| E2E: Budget Dashboard | `tests/e2e/test_budget_dashboard.py` | `[ ]` |

---

### 108.2 529 Target Date Portfolio Recommender `[ ]`

**Acceptance Criteria**: Build a 529 plan optimizer that recommends age-based glide paths, comparing target date funds across state-sponsored plans.

#### Database Schema

```sql
CREATE TABLE plans_529 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    beneficiary_id UUID NOT NULL,
    
    -- Plan Details
    plan_name VARCHAR(255) NOT NULL,
    state VARCHAR(2) NOT NULL,
    is_resident_plan BOOLEAN DEFAULT FALSE,     -- For state tax benefits
    custodian VARCHAR(100),
    
    -- Beneficiary Info
    beneficiary_name VARCHAR(255),
    beneficiary_birth_date DATE NOT NULL,
    target_college_year INTEGER GENERATED ALWAYS AS (
        EXTRACT(YEAR FROM beneficiary_birth_date) + 18
    ) STORED,
    years_to_enrollment INTEGER,
    
    -- Funding
    current_balance DECIMAL(20, 2) DEFAULT 0,
    monthly_contribution DECIMAL(20, 2) DEFAULT 0,
    
    -- Goals
    target_college VARCHAR(100),
    estimated_cost DECIMAL(20, 2),              -- 4-year total
    projected_gap DECIMAL(20, 2),
    
    -- Portfolio
    portfolio_type VARCHAR(50),                  -- AGE_BASED, STATIC, CUSTOM
    current_equity_allocation DECIMAL(8, 6),
    target_equity_allocation DECIMAL(8, 6),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE glide_paths_529 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL REFERENCES plans_529(id),
    years_to_enrollment INTEGER NOT NULL,
    equity_allocation DECIMAL(8, 6) NOT NULL,
    fixed_income_allocation DECIMAL(8, 6) NOT NULL,
    money_market_allocation DECIMAL(8, 6) NOT NULL,
    PRIMARY KEY (plan_id, years_to_enrollment)
);
```

#### Backend Implementation

```python
class GlidePathRecommender529:
    """
    Recommend optimal 529 glide path based on time to enrollment.
    
    Default Glide Path:
    - 18+ years: 90% equity, 10% bonds
    - 10 years: 70% equity, 30% bonds
    - 5 years: 50% equity, 50% bonds
    - 2 years: 30% equity, 70% bonds
    - 0 years: 10% equity, 90% money market
    """
    
    def recommend_allocation(
        self, 
        years_to_enrollment: int,
        risk_tolerance: str = 'MODERATE'
    ) -> AllocationRecommendation:
        pass
    
    def compare_state_plans(
        self, 
        resident_state: str, 
        beneficiary_age: int
    ) -> list[PlanComparison]:
        """Compare 529 plans across states for best value."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| 529 Migration | `migrations/108_529_plans.sql` | `[ ]` |
| 529 Plan Model | `models/plan_529.py` | `[ ]` |
| Glide Path Recommender | `services/education/glide_path_529.py` | `[ ]` |
| State Plan Comparator | `services/education/state_plan_comparator.py` | `[ ]` |
| API Endpoint | `web/api/planning/529.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| 529 Dashboard | `frontend2/src/components/Education/Dashboard529.jsx` | `[ ]` |
| Glide Path Chart | `frontend2/src/components/Charts/GlidePathChart.jsx` | `[ ]` |
| State Plan Comparison | `frontend2/src/components/Education/StatePlanComparison.jsx` | `[ ]` |
| Contribution Calculator | `frontend2/src/components/Education/ContributionCalc.jsx` | `[ ]` |
| use529Plan Hook | `frontend2/src/hooks/use529Plan.js` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Glide Path | `tests/unit/test_glide_path_529.py` | `[ ]` |
| Unit: State Comparator | `tests/unit/test_state_plan_comparator.py` | `[ ]` |
| Integration: 529 API | `tests/integration/test_529_api.py` | `[ ]` |
| E2E: 529 Dashboard | `tests/e2e/test_529_dashboard.py` | `[ ]` |

---

### 108.3 Kafka Relationship Focus Metrics Producer `[ ]`

**Acceptance Criteria**: Stream real-time financial planner relationship metrics (client engagement, plan adherence, goal progress) via Kafka for dashboard consumption.

#### Kafka Topic (Docker-compose: redpanda service)

```json
{
    "topic": "planner-relationship-metrics",
    "partitions": 3,
    "retention_ms": 2592000000,
    "schema": {
        "planner_id": "uuid",
        "client_id": "uuid",
        "metric_type": "string",
        "metric_value": "decimal",
        "period": "string",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Metrics Producer | `services/kafka/planner_metrics_producer.py` | `[ ]` |
| Engagement Calculator | `services/planning/engagement_calculator.py` | `[ ]` |
| Goal Progress Tracker | `services/planning/goal_tracker.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Relationship Dashboard | `frontend2/src/components/Planner/RelationshipDashboard.jsx` | `[ ]` |
| Engagement Score Card | `frontend2/src/components/Planner/EngagementScoreCard.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Metrics Producer | `tests/unit/test_planner_metrics_producer.py` | `[ ]` |
| Integration: Kafka | `tests/integration/test_planner_metrics_kafka.py` | `[ ]` |

---

### 108.4 529 State-Approved Fund List Validator `[ ]`

**Acceptance Criteria**: Validate that selected 529 investments are on the state's approved fund list to maintain tax benefits.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fund Validator | `services/education/fund_validator_529.py` | `[ ]` |
| State Fund List Ingester | `services/education/state_fund_list.py` | `[ ]` |
| Tax Benefit Calculator | `services/tax/state_529_benefit.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Fund Selector with Validation | `frontend2/src/components/Education/FundSelector529.jsx` | `[ ]` |
| Tax Benefit Display | `frontend2/src/components/Education/TaxBenefitDisplay.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Fund Validator | `tests/unit/test_fund_validator_529.py` | `[ ]` |
| Unit: Tax Benefit | `tests/unit/test_state_529_benefit.py` | `[ ]` |

---

### 108.5 Retirement Math Gap Engine `[ ]`

**Acceptance Criteria**: Calculate the gap between current savings trajectory and retirement goals, identifying required course corrections.

#### Backend Implementation

```python
class RetirementGapEngine:
    """
    Calculate retirement savings gap and required corrections.
    
    Inputs:
    - Current savings
    - Monthly contribution
    - Years to retirement
    - Desired retirement income
    - Expected Social Security
    - Expected portfolio return
    
    Outputs:
    - Projected retirement balance
    - Required balance for desired income (4% rule)
    - Gap or surplus
    - Required additional monthly savings
    """
    
    def calculate_gap(self, profile: RetirementProfile) -> GapAnalysis:
        pass
    
    def suggest_corrections(self, gap: GapAnalysis) -> list[Correction]:
        """Suggest ways to close the retirement gap."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Gap Engine | `services/retirement/gap_engine.py` | `[ ]` |
| Correction Suggester | `services/retirement/correction_suggester.py` | `[ ]` |
| Social Security Estimator | `services/retirement/ss_estimator.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Retirement Gap Widget | `frontend2/src/components/Retirement/GapWidget.jsx` | `[ ]` |
| Correction Suggestions | `frontend2/src/components/Retirement/CorrectionSuggestions.jsx` | `[ ]` |
| Projection Chart | `frontend2/src/components/Charts/RetirementProjection.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Gap Engine | `tests/unit/test_retirement_gap_engine.py` | `[ ]` |
| Unit: Correction Suggester | `tests/unit/test_correction_suggester.py` | `[ ]` |
| Integration: Full Analysis | `tests/integration/test_retirement_gap_analysis.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 108.1 Spending Analyzer | `[ ]` | `[ ]` |
| 108.2 529 Target Date | `[ ]` | `[ ]` |
| 108.3 Kafka Metrics | `[ ]` | `[ ]` |
| 108.4 Fund Validator | `[ ]` | `[ ]` |
| 108.5 Retirement Gap Engine | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py budget analyze` | Analyze spending patterns | `[ ]` |
| `python cli.py 529 recommend <age>` | Recommend 529 allocation | `[ ]` |
| `python cli.py 529 compare-states` | Compare state plans | `[ ]` |
| `python cli.py retirement gap` | Calculate retirement gap | `[ ]` |

---

*Last verified: 2026-01-25*
