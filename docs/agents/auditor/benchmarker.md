# Benchmarker (Agent 12.3)

## ID: `benchmarker`

## Role & Objective
The 'Standard Bearer'. Compares total portfolio performance against external indices like the S&P 500, BTC, or Gold to determine true alpha.

## Logic & Algorithm
- **Time-Weighted Returns**: Calculates the TWR of the total portfolio across all accounts.
- **Relative Performance**: Subtracts index returns from portfolio returns to isolate "Manager Skill" (Alpha).
- **Correlation Mapping**: Identifies if the portfolio is becoming "Too Beta" (moving 1:1 with the market) vs its intended uncorrelated strategy.

## Inputs & Outputs
- **Inputs**:
  - `total_account_equity` (Stream): The current net worth.
  - `market_index_prices` (Stream): Prices for SPY, QQQ, BTC, etc.
- **Outputs**:
  - `alpha_beta_report` (Dict): Relative performance metrics.

## Acceptance Criteria
- Calculate daily relative performance vs standard benchmarks by market close.
- Flag any 5-day period where "Alpha" becomes negative while the market is rising.
