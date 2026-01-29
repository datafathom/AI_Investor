# Phase 130: Real Estate Liquidity vs. Tax Benefit Engine

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Real Estate Team

---

## 📋 Overview

**Description**: Develop a decision engine that compares the liquidity benefits of REITs against the tax advantages (depreciation, 1031 exchanges) of direct property ownership, helping investors choose the optimal vehicle for their real estate allocation.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 10

---

## 🎯 Sub-Deliverables

### 130.1 REIT Liquidity vs. Direct Property Model `[x]`

**Acceptance Criteria**: Build a comparative model that quantifies the "liquidity premium" of REITs versus the "illiquidity discount" of direct property, factoring in transaction costs and time-to-exit.

#### Backend Implementation

```python
class LiquidityModel:
    """
    Compare liquidity costs between REITs and Direct Real Estate.
    
    Factors:
    - REITs: Instant liquidity, spread cost (~0.05%), capital gains tax
    - Direct: Months to sell, broker fees (6%), depreciation recapture
    """
    
    def calculate_liquidity_adjusted_return(
        self,
        asset_type: str,  # 'REIT' or 'DIRECT'
        holding_period_years: int,
        expected_appreciation: Decimal
    ) -> Decimal:
        """Calculate annualized return adjusted for transaction/liquidity costs."""
        pass

    def estimate_time_to_exit(
        self,
        property_type: str,
        market_condition: str
    ) -> int:
        """Estimate days to sell based on property type and market."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Model | `services/real_estate/liquidity_model.py` | `[x]` |
| Transaction Cost Calc | `services/real_estate/transaction_costs.py` | `[x]` |
| API Endpoint | `web/api/real_estate/liquidity_compare.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Comparison Calculator | `frontend2/src/components/RealEstate/LiquidityCalculator.jsx` | `[x]` |
| Cost Breakdown Chart | `frontend2/src/components/Charts/RECostBreakdown.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Liquidity Model | `tests/unit/test_liquidity_model.py` | `[x]` |
| Integration: Compare API | `tests/integration/test_re_compare_api.py` | `[x]` |

---

### 130.2 Depreciation Benefit Tracking Service `[x]`

**Acceptance Criteria**: Implement a service to track depreciation schedules (27.5 year residential, 39 year commercial) and calculate the tax shield benefit for direct properties.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE property_depreciation_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Basis Details
    purchase_price DECIMAL(20, 2) NOT NULL,
    land_value DECIMAL(20, 2) NOT NULL,
    building_value DECIMAL(20, 2) GENERATED ALWAYS AS (purchase_price - land_value) STORED,
    placed_in_service_date DATE NOT NULL,
    
    -- Depreciation Method
    prop_type VARCHAR(20) NOT NULL, -- RESIDENTIAL (27.5), COMMERCIAL (39)
    recovery_period_years DECIMAL(4, 1) NOT NULL,
    
    -- Tracking
    accumulated_depreciation DECIMAL(20, 2) DEFAULT 0,
    current_year_deduction DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_depr_user ON property_depreciation_schedules(user_id);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/130_depreciation.sql` | `[x]` |
| Depreciation Service | `services/tax/depreciation_service.py` | `[x]` |
| Tax Shield Calculator | `services/tax/tax_shield_calc.py` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Depreciation Calc | `tests/unit/test_depreciation_calc.py` | `[x]` |
| Integration: Tax Impact | `tests/integration/test_tax_shield.py` | `[x]` |

---

### 130.3 Small Institutional Investor Access Logic `[x]`

**Acceptance Criteria**: Evaluate eligibility for "small institutional" access points like private REITs, syndications, or crowdfunding platforms based on accreditation status.

| Component | File Path | Status |
|-----------|-----------|--------|
| Access Gatekeeper | `services/real_estate/access_gatekeeper.py` | `[x]` |
| Accreditation Verifier | `services/compliance/accreditation.py` | `[x]` |

---

### 130.4 Neo4j 1031 Exchange Eligibility Timer `[x]`

**Acceptance Criteria**: Model 1031 exchange timelines in Neo4j to track the strict 45-day identification and 180-day closing windows.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:PROPERTY_SALE {
    id: "uuid",
    sale_date: date("2025-01-01"),
    sale_price: 500000,
    capital_gains: 150000
})

(:EXCHANGE_TIMELINE {
    id: "uuid",
    deadline_45_day: date("2025-02-15"),
    deadline_180_day: date("2025-06-30"),
    status: "ACTIVE"
})

(:PROPERTY_SALE)-[:INITIATES_1031]->(:EXCHANGE_TIMELINE)

(:EXCHANGE_TIMELINE)-[:IDENTIFIED_CANDIDATE {
    id_date: date("2025-02-10")
}]->(:POTENTIAL_PROPERTY)

(:EXCHANGE_TIMELINE)-[:COMPLETED_PURCHASE {
    close_date: date("2025-05-01")
}]->(:REPLACEMENT_PROPERTY)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Exchange Graph Service | `services/neo4j/exchange_1031_graph.py` | `[x]` |
| Timeline Monitor | `services/real_estate/timeline_monitor.py` | `[x]` |
| Alert Service | `services/alerts/exchange_deadline.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| 1031 Timeline Tracker | `frontend2/src/components/RealEstate/ExchangeTimeline.jsx` | `[x]` |
| Deadline Alert | `frontend2/src/components/Alerts/ExchangeDeadline.jsx` | `[x]` |

---

### 130.5 Time-to-Exit Comparison Calculator `[x]`

**Acceptance Criteria**: Calculator comparing the total time to convert asset to cash, outlining the liquidity risk of direct ownership.

| Component | File Path | Status |
|-----------|-----------|--------|
| Time-to-Exit Calc | `services/real_estate/time_to_exit.py` | `[x]` |

---

## 📊 Comparison Matrix

| Feature | REITs | Direct Real Estate |
|---------|-------|-------------------|
| Liquidity | T+1 | Months |
| Min Investment | Low ($) | High ($$$$) |
| Tax Benefits | Dividend Tax | Depreciation + 1031 |
| Management | Passive | Active |
| Diversification | High | Low |

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py re compare` | Run REIT vs Direct comparison | `[x]` |
| `python cli.py re depreciation <cost>` | Calculate depreciation schedule | `[x]` |
| `python cli.py re 1031-deadline <date>` | Calculate 1031 deadlines | `[x]` |

---

*Last verified: 2026-01-25*
