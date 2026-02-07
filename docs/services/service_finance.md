# Backend Service: Finance

## Overview
The **Finance Service** provides the platform's quantitative mathematical chassis. It handles specialized institutional-grade calculations ranging from **Mortgage Amortization** and equity gain tracking to the deep-dive analysis of **Total Cost of Ownership (TCO)** and **Fee Margins**. It is designed to expose the "hidden costs" of investment strategies, such as tax and cash drag, and compare them against passive "Beta" benchmarks.

## Core Components

### 1. Amortization Tracker (`amortization.py`)
Tracks the paydown of collateralized debt.
- **Equity Gain Logic**: Automatically updates the equity value of a real estate asset or business loan by resolving the monthly principal/interest split.
- **Paydown Analysis**: Integrates with the platform's balance sheet to provide an accurate "Net Worth" pulse as liabilities decrease.

### 2. Fee Margin Engine (`fee_margin_calc.py`)
Architects transparency for institutional fee structures.
- **Profitability Analysis**: Calculates the net operational margin on AUM fees after subtracting management costs and the inherent **Cost of Beta** (benchmarked at 3 bps / 0.03%).
- **Margin Thresholds**: Flags "Pressured" vs. "High" profitability strategies for Multi-Family Offices (MFOs) managing complex fee splits.

### 3. TCO & Opportunity Cost (`op_cost_calculator.py`)
Exposes the structural efficiency of investment strategies.
- **Total Cost of Ownership (TCO)**: Aggregates Management Fees, Bid-Ask Spreads, Tax Drag, and Cash Drag into a single, unified efficiency percentage.
- **Efficiency Gap**: Quantifies the delta between a custom strategy and a standard low-cost index (Cost of Beta), helping advisors justify active management premiums.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Real Estate Detail** | Equity Growth Meter | `amortization_tracker.get_equity_gain()` |
| **Family Office Station** | Strategy Margin Ledger | `fee_margin_calculator.calculate_margin()` |
| **Portfolio Audit** | TCO Transparency Card | `op_cost_calculator.calculate_tco()` |
| **Investment Planner** | "Gap vs Beta" Sparklines | `op_cost_calculator.compare_to_beta()` |
| **Wealth Dashboard** | Debt-to-Equity Pulse | `amortization_tracker` (Balance updates) |

## Dependencies
- `logging`: Records structural margin changes and efficiency flags for the platform's financial history.

## Usage Examples

### Calculating the TCO of an Active Growth Strategy
```python
from services.finance.op_cost_calculator import OperationalCostCalculator

calc = OperationalCostCalculator()

# Calculate TCO: 1% fee, 0.2% spread, 0.5% tax drag, 0.1% cash drag
tco = calc.calculate_tco(
    strategy_name="Aggressive Growth Aggregator",
    management_fee=0.0100,
    avg_spread=0.0020,
    tax_drag=0.0050,
    cash_drag=0.0010
)

gap = calc.compare_to_beta(strategy_tco=tco)
print(f"Total Cost of Ownership: {tco:.2%}")
print(f"Efficiency Gap vs Passive Beta: {gap*10000:.0f} bps")
```

### Analyzing Institutional Profitability
```python
from services.finance.fee_margin_calc import FeeMarginCalculator

fmc = FeeMarginCalculator()

# 0.75% Gross Fee, 0.20% Admin/Op Cost
analysis = fmc.calculate_margin(gross_fee=0.0075, operational_cost=0.0020)

print(f"Net Operational Fee: {analysis['net_fee_pct']:.2%}")
print(f"Surplus vs Beta Benchmark: {analysis['margin_vs_beta_bps']} bps")
print(f"Strategic Viability: {analysis['profitability']}")
```
