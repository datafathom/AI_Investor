# Documentation: `tests/unit/test_portfolio_manager.py` & `test_portfolio_selector.py`

## Overview
These tests validate the "Dual-Portfolio" approach (Defensive vs. Aggressive) and the automated logic that determines which strategy model a user should follow based on their capital.

## Components Under Test
- `services.portfolio_manager.PortfolioManager`: Manages capital allocation, position entry, and P&L aggregation.
- `services.portfolio.model_vs_custom.PortfolioSelector`: Strategy assignment logic.

## Key Test Scenarios

### 1. Dual-Portfolio Allocation
- **Goal**: Ensure capital is split correctly between Defensive (60% default) and Aggressive (40% default) buckets.
- **Assertions**:
    - Initialization of a $100k account correctly assigns $60k to defensive and $40k to aggressive cash reserves.
    - Adding positions correctly updates the cash balance of the targeted portfolio.

### 2. Specialized Position Types
- **Goal**: Verify "Sure-Thing" (high conviction/leverage) and "Hedge" positions.
- **Assertions**:
    - `add_sure_thing()` correctly applies high conviction labels and leverage multipliers.
    - `add_hedge()` correctly labels positions in the defensive portfolio for VIX/Volatility protection.

### 3. Strategy Selection
- **Goal**: Enforce institutional boundaries for model portfolios.
- **Assertions**:
    - Accounts with $200k are assigned a standard `MODEL_PORTFOLIO`.
    - Accounts with $1M+ are upgraded to a `CUSTOMIZED` strategy.

## Holistic Context
This logic prevents "Concentration Risk" and ensures that the AI Investor respects the user's risk profile. The dual-portfolio system acts as an internal "Barbell Strategy", keeping 60% of assets in safety while the aggressive side seeks alpha.
