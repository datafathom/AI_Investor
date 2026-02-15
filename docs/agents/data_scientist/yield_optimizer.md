# Yield Optimizer (Agent 3.5)

## ID: `yield_optimizer`

## Role & Objective
Mathematical engine for bond and cash-equiv performance. Calculates Yield-to-Maturity (YTM) for fixed-income assets.

## Logic & Algorithm
- Monitors global treasury curves (US10Y, etc.).
- Evaluates DeFi lending rates vs institutional yields.
- Proposes cash-sweep movements to capture better basis.

## Inputs & Outputs
- **Inputs**:
  - `cash_position` (float): Available liquidity to deploy.
  - `duration_preference` (int): Target investment horizon in months.
- **Outputs**:
  - `yield_map` (Dict): Comparison of top 5 safest yield sources.
  - `delta_vs_inflation` (float): Real yield after CPI adjustment.

## Acceptance Criteria
- Refresh global yield tables every 60 minutes.
- Real yield must be accurately calculated against the latest Inflation Architect data.
