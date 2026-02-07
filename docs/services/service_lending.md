# Backend Service: Lending

## Overview
The **Lending Service** manages the platform's institutional-grade debt and liquidity infrastructure. It allows UHNW clients to unlock liquidity from concentrated asset positions without triggering immediate tax events. The service provides specialized volatility-adjusted **Loan-to-Value (LTV)** modeling, tax-aware decision logic to compare borrowing costs against capital gains hits ("Borrow vs. Sell"), and generates automated **Interest-Only (IO)** payment schedules for multi-million dollar credit facilities.

## Core Components

### 1. Stock-Based Lending Engine (`stock_lending_svc.py`)
Optimizes liquidity extraction from concentrated equity positions.
- **Volatility-Adjusted LTV**: Automatically calculates maximum borrowing capacity based on ticker volatility. Lower volatility assets (e.g., indices or mega-caps) receive higher LTVs (up to 50%), while high-volatility assets are restricted to ensure collateral stability.
- **Tax-Aware Decision Logic**: Conducts a "Borrow vs. Sell" analysis. It calculates the one-time capital gains tax cost of selling a position versus the annual interest cost of borrowing against it. If the tax hit is significantly higher than 3 years of interest, it recommends a "Borrow" strategy to preserve basis and defer taxes.

### 2. Credit Facility Manager (`payment_sched.py`)
Orchestrates the lifecycle of UHNW debt structures.
- **Interest-Only (IO) Scheduler**: Generates precision repayment schedules for interest-only credit lines. This is the standard structure for UHNW liquidity, allowing the principal to remain invested while only addressing the cost of capital on a monthly basis.
- **Balance Tracking**: Monitors the remaining principal and due dates for monthly interest payments.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Liquidity Station** | Borrowing Power Calculator | `stock_lending_svc.calculate_borrowing_power()` |
| **Liquidity Station** | Borrow vs. Sell Decision Tool| `stock_lending_svc.analyze_borrow_vs_sell()` |
| **Portfolio Detail** | Collateral LTV Status | `stock_lending_svc.calculate_borrowing_power()` |
| **Lending Panel** | IO Payment Schedule | `payment_schedule_tracker.generate_io_schedule()` |
| **Document Hub** | Credit Agreement Summary | `lending` logic (Interest rates/Terms) |

## Dependencies
- `decimal`: Used for all high-precision financial math (LTV, tax rates, and interest payments).
- `datetime / timedelta`: Orchestrates the monthly due dates for loan repayment schedules.
- `logging`: Records structural events like "Significant Borrowing Capacity Identified" or "Loan vs. Sell Recommendations."

## Usage Examples

### Calculating Max Borrowing Power for a Concentrated Holder
```python
from services.lending.stock_lending_svc import StockLendingService
from decimal import Decimal

lending = StockLendingService()

# Client holds $10M of a ticker with 25% volatility
capacity = lending.calculate_borrowing_power(
    symbol="NVDA",
    position_value=Decimal("10000000.00"),
    volatility_pct=25.0
)

print(f"Asset: {capacity['symbol']}")
print(f"Max LTV: {capacity['max_ltv']:.1%}")
print(f"Available Liquidity: ${capacity['available_liquidity']:,.2f}")
```

### Performing a "Borrow vs. Sell" Tax Break-Even Analysis
```python
from services.lending.stock_lending_svc import StockLendingService
from decimal import Decimal

lending = StockLendingService()

# Evaluate selling $1M vs borrowing at 6% interest
res = lending.analyze_borrow_vs_sell(
    position_value=Decimal("1000000.00"),
    cost_basis=Decimal("100000.00"),
    cap_gains_rate=Decimal("0.238"), # 23.8% rate
    loan_interest_rate=Decimal("0.06") # 6% interest
)

print(f"One-Time Tax Cost of Sale: ${res['one_time_tax_cost']:,.2f}")
print(f"Annual Interest Cost: ${res['annual_loan_interest']:,.2f}")
print(f"Break-even: {res['breakeven_years']} years")
print(f"Strategy Recommendation: {res['recommendation']}")
```

### Generating an 12-Month Interest-Only Schedule
```python
from services.lending.payment_sched import PaymentScheduleTracker
from decimal import Decimal

tracker = PaymentScheduleTracker()

# Generate a 1-year IO schedule for a $5M draw
schedule = tracker.generate_io_schedule(
    principal=Decimal("5000000.00"),
    rate_pct=6.25,
    months=12
)

for payment in schedule[:3]: # Show first 3 months
    print(f"Period {payment['period']} | Due: {payment['due_date']} | Interest: ${payment['interest_payment']:,.2f}")
```
