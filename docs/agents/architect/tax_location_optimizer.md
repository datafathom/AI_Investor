# Tax Location Optimizer (Agent 2.2)

## ID: `tax_location_optimizer`

## Role & Objective
The efficiency engine for the portfolio. It determines the most tax-efficient placement of assets across Taxable (Brokerage), Tax-Deferred (401k/IRA), and Tax-Exempt (Roth) accounts to maximize after-tax wealth.

## Logic & Algorithm
1. **Asset Classification**: Tags every asset as high-yield (tax-heavy) or growth-oriented (tax-light).
2. **Account Matching**: Maps high-tax assets (REITs, Corporate Bonds) to tax-advantaged accounts.
3. **Alpha Estimation**: Calculates the "Tax Alpha" or additional return generated solely through optimized placement.

## Inputs & Outputs
- **Inputs**:
  - Account Map (Tax Status per ID)
  - Asset List (Yield & Growth projections)
  - User Tax Bracket
- **Outputs**:
  - Proposed Asset Swaps
  - Estimated Annual Tax Savings (USD)

## Acceptance Criteria
- Tax Alpha optimization must be recalculated within 2 seconds of any major portfolio rebalance.
- Proposed swaps must account for any potential realized gains from the move itself (Wash-sale avoidance).
