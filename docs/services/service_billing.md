# Backend Service: Billing

## Overview
The **Billing Service** manages all financial obligations within the platform, including consumer bill tracking and institutional-grade fee calculations. It features complex logic for AUM-based tiered fees and performance-driven "Carried Interest," ensuring transparent and fair billing through mechanisms like High-Water Marks and Hurdle Rates.

## Core Components

### 1. Consumer Bill Management (`bill_payment_service.py`)
Provides the infrastructure for users to track and pay external bills.
- **Features**:
    - **Bill Lifecycle**: Supports transitioning bills from `PENDING` to `SCHEDULED` and `PAID`.
    - **Recurrence**: Manages one-time or recurring (monthly, annual) payments.
    - **Scheduling**: Integrates with the `BankingService` to execute transfers on specific dates.
    - **History**: Maintains a permanent record of all payments for audit purposes.

### 2. Institutional Fee Engines
These components automate the billing logic for wealth managers and family offices.
- **Tiered Fee Calculator (`tiered_fee_calc.py`)**: 
    - Implements a **declining-balance schedule**. 
    - Automatically applies different rates to different "tiers" of AUM (e.g., 1.0% on the first $1M, 0.75% on the next $4M, etc.).
- **Carry Engine (`carry_calculator.py`)**: 
    - Calculates **Performance Fees** (typically 20%) on trading profits.
    - **Hurdle Rate**: Ensures a minimum return (e.g., 5% "risk-free" hurdle) is met before any fees accrue.
    - **High-Water Mark (HWM)**: Ensures fees are only charged on *new* gains. If a portfolio loses value, no performance fees are paid until the original peak value is recovered.

### 3. Utility Services
- **Proration Service (`proration_service.py`)**: Calculates partial-month fees for mid-cycle capital additions or withdrawals.
- **Payment Reminders (`payment_reminder_service.py`)**: Handles the generation of notifications for upcoming or overdue bills.

## Dependencies
- `decimal`: Used for all fee calculations to avoid floating-point rounding errors.
- `services.system.cache_service`: For rapid retrieval of bill and payment states.
- `schemas.billing` & `schemas.fee_billing`: Structured pydantic models for fee schedules and bill objects.

## Usage Examples

### Calculating an Annual AUM Fee
```python
from services.billing.tiered_fee_calc import TieredFeeCalculator
from schemas.fee_billing import FeeSchedule

calc = TieredFeeCalculator()
schedule = FeeSchedule(
    tier_1_max=1000000, tier_1_rate=0.01,
    tier_2_max=5000000, tier_2_rate=0.0075,
    tier_3_rate=0.005
)

fee = calc.calculate_annual_fee(aum=7500000, schedule=schedule)
print(f"Annual Billing Amount: ${fee:,.2f}")
```

### Accruing Performance Fees (Carry)
```python
from services.billing.carry_calculator import CarryEngine
from decimal import Decimal

engine = CarryEngine()
report = engine.calculate_performance_fee(
    current_nav=Decimal('1200000.00'),
    previous_peak_nav=Decimal('1100000.00'),
    opening_nav=Decimal('1000000.00'),
    hurdle_rate=Decimal('0.05')
)

if report['status'] == "ACRUED":
    print(f"Accrued Fee: ${report['fee_amount']:,.2f} on {report['basis_alpha']:,.2f} of alpha.")
```
