# Phase 4: Tax-Loss Harvesting & Optimization

## Phase Status: `NOT_STARTED` ⚠️
**Last Updated**: 2026-01-21
**Estimated Duration**: 7-10 days
**Priority**: HIGH (Tax optimization critical for returns)
**Started Date**: TBD
**Completion Status**: Not Started

---

# Audit & Hardening: App Improvements (Phases 1-33)

This plan focuses on stabilizing and verifying the "App Hardening & Improvements" cycle (Phases 1-33), ensuring full E2E integration, 100% test coverage, and removing mock data dependencies.

## Proposed Changes

### [Group A & B: Analytics & Planning]

#### [MODIFY] [rebalancing_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/optimization/rebalancing_service.py)
- Refactor to include helper methods `_execute_trades` and `_record_rebalancing_history` for better testability and modularity.
- Replace mock weights with real data calls to `PortfolioAggregator`.

#### [MODIFY] [performance_attribution_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/analytics/performance_attribution_service.py)
- Replace `_get_portfolio_data` mock block with real integration to `PortfolioAggregator`.
- Remove simplified benchmark return mocks.

## Verification Plan

### Automated Tests
- Run `pytest tests/analytics/ tests/optimization/ tests/risk/ tests/tax/` to ensure all 33-phase backend components are passing.
- Achieve 100% code coverage for core services using `pytest-cov`.

### Manual Verification (E2E)
- Verify `AdvancedPortfolioAnalytics.jsx` loads and displays real data from the API.
- Verify `PortfolioOptimizationDashboard.jsx` generates and executes real rebalancing recommendations.

---

## Phase Overview

Implement intelligent tax-loss harvesting to minimize tax liability while maintaining portfolio objectives. This phase builds on existing tax harvesting infrastructure to add advanced optimization, lot selection, and comprehensive tax impact analysis.

### Dependencies
- Portfolio service for holdings
- Tax service (existing `TaxHarvestService`)
- Brokerage APIs for execution
- Market data for replacement suggestions

### Risk Factors
- Wash-sale rule compliance is critical
- Tax regulations vary by jurisdiction
- Requires accurate cost basis tracking
- Market timing affects harvesting effectiveness

---

## Deliverable 4.1: Enhanced Tax-Loss Harvesting Engine

### Status: `NOT_STARTED` ⚠️

### Detailed Task Description

Enhance the existing tax-loss harvesting service with advanced features including automated opportunity identification, wash-sale detection with 30-day lookback, replacement asset suggestions, and batch harvesting capabilities. The engine must:

- **Identify Harvest Opportunities**: Scan all positions for unrealized losses exceeding thresholds
- **Wash-Sale Detection**: Check transaction history for 30-day window violations
- **Replacement Suggestions**: Recommend correlated but non-identical replacement assets
- **Batch Processing**: Process multiple harvesting opportunities simultaneously
- **Tax Impact Calculation**: Estimate tax savings and net benefit after transaction costs
- **Automated Execution**: Execute harvesting trades with user approval

### Backend Implementation Details

**File**: `services/tax/enhanced_tax_harvesting_service.py`

**Required Header Comment**:
```python
"""
==============================================================================
FILE: services/tax/enhanced_tax_harvesting_service.py
ROLE: Enhanced Tax-Loss Harvesting Engine
PURPOSE: Identifies and executes tax-loss harvesting opportunities with
         wash-sale protection, replacement suggestions, and batch processing.

INTEGRATION POINTS:
    - TaxHarvestService: Existing tax harvesting infrastructure
    - PortfolioService: Portfolio holdings and cost basis
    - ExecutionService: Trade execution for harvesting
    - MarketDataService: Replacement asset correlation data
    - NotificationService: Harvesting opportunity alerts

FEATURES:
    - Automated opportunity scanning
    - 30-day wash-sale lookback
    - Correlated replacement suggestions
    - Batch harvesting processing
    - Tax savings estimation

AUTHOR: AI Investor Team
CREATED: TBD
LAST_MODIFIED: TBD
==============================================================================
"""
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-4.1.1 | Service identifies all positions with unrealized losses exceeding user-defined threshold (default $500 or 5%) | `NOT_STARTED` | | |
| AC-4.1.2 | Wash-sale detection queries transaction history for 30 days before and after sale date | `NOT_STARTED` | | |
| AC-4.1.3 | Replacement suggestions identify correlated assets (correlation >0.7) that are not substantially identical | `NOT_STARTED` | | |
| AC-4.1.4 | Tax savings calculation accounts for marginal tax rate, holding period (STCG vs LTCG), and state taxes | `NOT_STARTED` | | |
| AC-4.1.5 | Batch harvesting processes multiple opportunities while respecting wash-sale rules across all trades | `NOT_STARTED` | | |
| AC-4.1.6 | Service estimates net benefit after transaction costs (commissions, spreads, market impact) | `NOT_STARTED` | | |
| AC-4.1.7 | Harvesting opportunities are ranked by tax savings potential and net benefit | `NOT_STARTED` | | |
| AC-4.1.8 | Automated execution requires user approval for trades exceeding threshold (default $5,000) | `NOT_STARTED` | | |
| AC-4.1.9 | Harvesting history tracks all executed harvests with tax savings realized | `NOT_STARTED` | | |
| AC-4.1.10 | Unit tests verify wash-sale detection with various transaction scenarios | `NOT_STARTED` | | |
| AC-4.1.11 | Integration tests confirm harvesting trades execute correctly with proper lot selection | `NOT_STARTED` | | |
| AC-4.1.12 | Service handles edge cases: insufficient replacement liquidity, market closures, partial fills | `NOT_STARTED` | | |

---

## Deliverable 4.2: Tax Optimization Service

### Status: `NOT_STARTED` ⚠️

### Detailed Task Description

Build a comprehensive tax optimization service that handles lot selection optimization, tax-aware rebalancing, tax projection, and year-end tax planning. The service must optimize for after-tax returns rather than pre-tax returns.

### Backend Implementation Details

**File**: `services/tax/tax_optimization_service.py`

**Required Header Comment**:
```python
"""
==============================================================================
FILE: services/tax/tax_optimization_service.py
ROLE: Tax Optimization Service
PURPOSE: Optimizes portfolio decisions for tax efficiency including lot
         selection, tax-aware rebalancing, and tax projections.

INTEGRATION POINTS:
    - PortfolioService: Holdings and lot-level cost basis
    - TaxHarvestService: Harvesting opportunities
    - RebalancingService: Tax-aware rebalancing
    - TaxProjectionService: Year-end tax planning

FEATURES:
    - FIFO/LIFO/Highest Cost/Specific Lot selection
    - Tax-aware rebalancing optimization
    - Year-end tax projections
    - Tax-efficient withdrawal sequencing

AUTHOR: AI Investor Team
CREATED: TBD
LAST_MODIFIED: TBD
==============================================================================
"""
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-4.2.1 | Lot selection optimizer chooses optimal lots to minimize tax impact (FIFO, LIFO, Highest Cost, Specific Lot) | `NOT_STARTED` | | |
| AC-4.2.2 | Tax-aware rebalancing minimizes tax impact while achieving target allocation | `NOT_STARTED` | | |
| AC-4.2.3 | Tax projection estimates year-end tax liability based on current positions and planned transactions | `NOT_STARTED` | | |
| AC-4.2.4 | Year-end planning identifies opportunities to reduce tax liability before year-end | `NOT_STARTED` | | |
| AC-4.2.5 | Tax-efficient withdrawal sequencing optimizes order of account withdrawals (taxable, tax-deferred, tax-free) | `NOT_STARTED` | | |
| AC-4.2.6 | Service accounts for different tax rates (ordinary income, LTCG, STCG, qualified dividends) | `NOT_STARTED` | | |
| AC-4.2.7 | Optimization considers state tax implications for multi-state portfolios | `NOT_STARTED` | | |
| AC-4.2.8 | Tax optimization recommendations include estimated tax savings and implementation steps | `NOT_STARTED` | | |

---

## Deliverable 4.3: Tax Dashboard

### Status: `NOT_STARTED` ⚠️

### Detailed Task Description

Create a comprehensive tax dashboard that displays realized/unrealized gains, tax impact analysis, harvesting recommendations, and tax optimization opportunities.

### Frontend Implementation Details

**Files**: 
- `frontend2/src/widgets/Tax/TaxLossHarvestingWidget.jsx`
- `frontend2/src/widgets/Tax/TaxOptimizationWidget.jsx`
- `frontend2/src/widgets/Tax/TaxDashboard.jsx`

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-4.3.1 | Dashboard displays realized and unrealized gains/losses by holding with tax implications | `NOT_STARTED` | | |
| AC-4.3.2 | Harvesting opportunities are displayed in sortable table with tax savings estimates | `NOT_STARTED` | | |
| AC-4.3.3 | Wash-sale warnings are clearly displayed with countdown timers for eligibility | `NOT_STARTED` | | |
| AC-4.3.4 | Replacement suggestions show correlated assets with correlation coefficients | `NOT_STARTED` | | |
| AC-4.3.5 | Tax projection shows estimated year-end tax liability with breakdown by income type | `NOT_STARTED` | | |
| AC-4.3.6 | One-click harvesting executes trades with confirmation for large amounts | `NOT_STARTED` | | |
| AC-4.3.7 | Tax optimization recommendations are displayed with implementation steps | `NOT_STARTED` | | |
| AC-4.3.8 | Dashboard is responsive and works on all device sizes | `NOT_STARTED` | | |

---

## Change Log

| Date | Author | Change Description |
|------|--------|-------------------|
| 2026-01-21 | System | Initial creation of Phase 4 implementation plan |
