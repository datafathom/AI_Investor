# Phase 105: Traditional vs. Roth IRA Optimization Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax Optimization Team

---

## 📋 Overview

**Description**: Build an intelligent optimization engine that recommends Traditional vs. Roth IRA contributions based on current vs. projected future tax brackets, income levels, and retirement timeline.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 105.1 Pre-Tax vs. After-Tax Comparison Service `[ ]`

**Acceptance Criteria**: Implement a service that calculates the true after-tax value of Traditional vs. Roth contributions over a 40-year horizon.

#### Database Schema

```sql
CREATE TABLE ira_optimization_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Current Tax Situation
    current_marginal_rate DECIMAL(5, 4) NOT NULL,  -- e.g., 0.32 = 32%
    current_effective_rate DECIMAL(5, 4),
    current_agi DECIMAL(20, 2),
    filing_status VARCHAR(20),  -- SINGLE, MARRIED_JOINT, HEAD_OF_HOUSEHOLD
    
    -- Projected Retirement Tax Situation
    projected_retirement_rate DECIMAL(5, 4),
    projected_retirement_income DECIMAL(20, 2),
    expected_social_security DECIMAL(20, 2),
    expected_pension_income DECIMAL(20, 2),
    
    -- Time Horizon
    current_age INTEGER NOT NULL,
    retirement_age INTEGER NOT NULL,
    life_expectancy INTEGER DEFAULT 90,
    years_to_retirement GENERATED ALWAYS AS (retirement_age - current_age) STORED,
    
    -- Recommendation
    recommended_strategy VARCHAR(20),  -- TRADITIONAL, ROTH, SPLIT
    split_percentage_roth DECIMAL(5, 2),
    recommendation_confidence DECIMAL(5, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Backend Implementation

```python
class TraditionalVsRothAnalyzer:
    """
    Analyze and recommend Traditional vs. Roth contribution strategy.
    
    Key Factors:
    1. Current marginal tax rate
    2. Expected retirement tax rate
    3. Years until retirement (compounding time)
    4. State tax considerations
    5. RMD requirements (Traditional only)
    """
    
    def analyze(self, profile: IRAOptimizationProfile) -> AnalysisResult:
        """Perform full Traditional vs. Roth analysis."""
        
        # Calculate future value of $1 Traditional contribution
        traditional_fv = self._calc_traditional_future_value(profile)
        
        # Calculate future value of $1 Roth contribution
        roth_fv = self._calc_roth_future_value(profile)
        
        # Determine breakeven tax rate
        breakeven_rate = self._calc_breakeven_rate(profile)
        
        return AnalysisResult(
            traditional_value=traditional_fv,
            roth_value=roth_fv,
            breakeven_rate=breakeven_rate,
            recommendation=self._determine_recommendation(profile)
        )
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/105_ira_optimization.sql` | `[ ]` |
| Analyzer | `services/tax/traditional_vs_roth.py` | `[ ]` |
| Future Value Calculator | `services/tax/fv_calculator.py` | `[ ]` |
| Tax Projector | `services/tax/tax_projector.py` | `[ ]` |
| API Endpoint | `web/api/retirement/ira_optimization.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| IRA Optimizer Form | `frontend2/src/components/IRA/OptimizerForm.jsx` | `[ ]` |
| Comparison Chart | `frontend2/src/components/Charts/TraditionalVsRothChart.jsx` | `[ ]` |
| Recommendation Card | `frontend2/src/components/IRA/RecommendationCard.jsx` | `[ ]` |
| Tax Bracket Slider | `frontend2/src/components/IRA/TaxBracketSlider.jsx` | `[ ]` |
| useIRAOptimization Hook | `frontend2/src/hooks/useIRAOptimization.js` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Analyzer | `tests/unit/test_traditional_vs_roth.py` | `[ ]` |
| Unit: FV Calculator | `tests/unit/test_fv_calculator.py` | `[ ]` |
| Unit: Tax Projector | `tests/unit/test_tax_projector.py` | `[ ]` |
| Integration: Full Pipeline | `tests/integration/test_ira_optimization.py` | `[ ]` |
| E2E: Optimizer Form | `tests/e2e/test_ira_optimizer_form.py` | `[ ]` |

---

### 105.2 Roth Income Limit Validator ($146k/$230k) `[ ]`

**Acceptance Criteria**: Implement validation logic that enforces Roth IRA income limits and suggests backdoor Roth when limits are exceeded.

#### Income Limit Configuration (2025)

| Filing Status | Full Contribution | Phase-out Begins | Phase-out Ends |
|---------------|-------------------|------------------|----------------|
| Single | < $146,000 | $146,000 | $161,000 |
| Married Joint | < $230,000 | $230,000 | $240,000 |
| Married Separate | $0 | $0 | $10,000 |

#### Backend Implementation

```python
class RothIncomeValidator:
    """
    Validate Roth IRA eligibility based on MAGI.
    
    Actions:
    1. Check if full contribution allowed
    2. Calculate reduced contribution in phase-out range
    3. Recommend backdoor Roth if over limits
    4. Track pro-rata rule for backdoor eligibility
    """
    
    def validate_eligibility(
        self, 
        magi: Decimal, 
        filing_status: str,
        year: int
    ) -> RothEligibilityResult:
        pass
    
    def calculate_reduced_contribution(
        self,
        magi: Decimal,
        filing_status: str,
        year: int
    ) -> Decimal:
        """Calculate allowed contribution in phase-out range."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Income Validator | `services/tax/roth_income_validator.py` | `[ ]` |
| Limit Config | `config/roth_income_limits.py` | `[ ]` |
| Backdoor Advisor | `services/tax/backdoor_roth_advisor.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Eligibility Checker | `frontend2/src/components/IRA/EligibilityChecker.jsx` | `[ ]` |
| Income Limit Warning | `frontend2/src/components/Alerts/IncomeLimitWarning.jsx` | `[ ]` |
| Backdoor Roth Guide | `frontend2/src/components/Guides/BackdoorRothGuide.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Income Validator | `tests/unit/test_roth_income_validator.py` | `[ ]` |
| Unit: Reduced Contribution | `tests/unit/test_reduced_contribution.py` | `[ ]` |
| Integration: Backdoor Flow | `tests/integration/test_backdoor_flow.py` | `[ ]` |

---

### 105.3 40-Year Accumulation Projection Table `[ ]`

**Acceptance Criteria**: Generate a detailed year-by-year projection table showing account growth, tax impact, and net worth under both Traditional and Roth scenarios.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Projection Engine | `services/retirement/accumulation_projector.py` | `[ ]` |
| Compound Growth Calculator | `services/retirement/compound_growth.py` | `[ ]` |
| Tax Impact Calculator | `services/tax/retirement_tax_impact.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Projection Table | `frontend2/src/components/Tables/AccumulationTable.jsx` | `[ ]` |
| Growth Timeline | `frontend2/src/components/Charts/GrowthTimeline.jsx` | `[ ]` |
| Net Worth Comparison | `frontend2/src/components/Charts/NetWorthComparison.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Projection Engine | `tests/unit/test_accumulation_projector.py` | `[ ]` |
| Unit: Compound Growth | `tests/unit/test_compound_growth.py` | `[ ]` |
| Integration: Full Projection | `tests/integration/test_40_year_projection.py` | `[ ]` |

---

### 105.4 Neo4j Self-Directed IRA Node `[ ]`

**Acceptance Criteria**: Model self-directed IRA accounts in Neo4j with relationships to alternative assets (real estate, private equity, crypto).

#### Neo4j Schema

```cypher
(:SELF_DIRECTED_IRA {
    id: "uuid",
    custodian: "Equity Trust",
    account_type: "ROTH",  // TRADITIONAL, ROTH, SEP
    total_value: 500000,
    checkbook_control: true
})

(:ALTERNATIVE_ASSET {
    id: "uuid",
    type: "REAL_ESTATE",
    description: "Rental Property - 123 Main St",
    acquisition_cost: 200000,
    current_value: 350000
})

(:SELF_DIRECTED_IRA)-[:HOLDS {
    acquisition_date: date(),
    cost_basis: 200000,
    current_value: 350000
}]->(:ALTERNATIVE_ASSET)

(:ALTERNATIVE_ASSET)-[:PROHIBITED_TRANSACTION_RISK {
    risk_level: "HIGH",
    reason: "Related party involvement"
}]->(:PARTY)
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| SDIRA Graph Service | `services/neo4j/sdira_graph.py` | `[ ]` |
| Alt Asset Tracker | `services/retirement/alt_asset_tracker.py` | `[ ]` |
| Prohibited Transaction Checker | `services/compliance/prohibited_tx_checker.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| SDIRA Dashboard | `frontend2/src/components/SDIRA/Dashboard.jsx` | `[ ]` |
| Alt Asset Manager | `frontend2/src/components/SDIRA/AltAssetManager.jsx` | `[ ]` |
| Prohibited TX Warning | `frontend2/src/components/SDIRA/ProhibitedTXWarning.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: SDIRA Graph | `tests/unit/test_sdira_graph.py` | `[ ]` |
| Unit: Prohibited TX | `tests/unit/test_prohibited_tx_checker.py` | `[ ]` |
| Integration: SDIRA Flow | `tests/integration/test_sdira_flow.py` | `[ ]` |

---

### 105.5 Tax Bracket Forecaster for Roth Recommendation `[ ]`

**Acceptance Criteria**: Build a forecaster that predicts future tax brackets based on income trajectory, tax law sunset provisions, and retirement timeline.

#### Backend Implementation

```python
class TaxBracketForecaster:
    """
    Forecast future tax brackets for Roth optimization.
    
    Considerations:
    1. Career income trajectory
    2. Tax Cuts and Jobs Act sunset (2026)
    3. Social Security taxation
    4. RMD-forced income in retirement
    5. State tax changes
    """
    
    def forecast_retirement_bracket(
        self,
        profile: IRAOptimizationProfile
    ) -> BracketForecast:
        pass
    
    def simulate_tax_scenarios(
        self,
        profile: IRAOptimizationProfile,
        scenarios: list[TaxScenario]
    ) -> list[ScenarioResult]:
        """Run Monte Carlo on tax law scenarios."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Bracket Forecaster | `services/tax/bracket_forecaster.py` | `[ ]` |
| Sunset Simulator | `services/tax/tcja_sunset_simulator.py` | `[ ]` |
| Income Trajectory | `services/planning/income_trajectory.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Bracket Forecast Chart | `frontend2/src/components/Charts/BracketForecast.jsx` | `[ ]` |
| Tax Scenario Simulator | `frontend2/src/components/Simulator/TaxScenarioSim.jsx` | `[ ]` |
| TCJA Sunset Warning | `frontend2/src/components/Alerts/TCJASunsetWarning.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Forecaster | `tests/unit/test_bracket_forecaster.py` | `[ ]` |
| Unit: Sunset Simulator | `tests/unit/test_tcja_sunset.py` | `[ ]` |
| Integration: Full Forecast | `tests/integration/test_tax_forecast.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 105.1 Pre-Tax vs. After-Tax | `[ ]` | `[ ]` |
| 105.2 Roth Income Validator | `[ ]` | `[ ]` |
| 105.3 40-Year Projection | `[ ]` | `[ ]` |
| 105.4 Neo4j SDIRA Node | `[ ]` | `[ ]` |
| 105.5 Bracket Forecaster | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py ira analyze` | Run IRA optimization | `[ ]` |
| `python cli.py ira eligibility <income>` | Check Roth eligibility | `[ ]` |
| `python cli.py ira project <years>` | Generate projection | `[ ]` |
| `python cli.py ira forecast-bracket` | Forecast tax bracket | `[ ]` |

---

*Last verified: 2026-01-25*
