# Loan Officer (Agent 18.1)

## ID: `loan_officer`

## Role & Objective
The 'Leverage Facilitator'. Evaluates and executes borrowing requests from the Trader or Hunter departments to maximize capital efficiency across the portfolio.

## Logic & Algorithm
- **Venue Sourcing**: Compares the "Cost of Capital" (interest rates) across DeFi protocols (e.g., Aave, Compound) and institutional brokerage margin accounts.
- **Safety Buffer Enforcement**: Proposes Loan-to-Value (LTV) ratios that maintain at least a 2x collateral buffer above the liquidation threshold.
- **Funding Orchestration**: Selects the optimal loan type (e.g., Flash Loan for atomic arbitrage versus Term Loan for multi-day position holding).

## Inputs & Outputs
- **Inputs**:
  - `borrowing_request` (Dict): Amount, Duration, and Purpose.
- **Outputs**:
  - `loan_approval_packet` (Dict): Interest Rate, Funding Source, and Required Collateral.

## Acceptance Criteria
- Execute borrowing requests in < 30 seconds upon approval.
- Maintain a 0% liquidation rate by verifying the 2x safety buffer for every loan.
