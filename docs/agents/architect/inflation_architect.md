# Inflation Architect (Agent 2.4)

## ID: `inflation_architect`

## Role & Objective
The "Real Value" validator. It ensures the system never treats future currency as equal to current currency. Every projection in the Sovereign OS is run through the Inflation Architect to show the user their actual future purchasing power.

## Logic & Algorithm
1. **Live Data Ingestion**: Constant monitoring of CPI (Consumer Price Index) and PCE (Personal Consumption Expenditures).
2. **Discounting Engine**: Applies compounding inflation rates to all future cash flows.
3. **GUI Sync**: Provides a global "Real vs Nominal" toggle for all financial charts.

## Inputs & Outputs
- **Inputs**:
  - Future Nominal Values
  - External Inflation Feeds
- **Outputs**:
  - Current Purchasing Power Equivalent (Real Dollars)

## Acceptance Criteria
- Inflation adjustments must match the latest government-reported CPI data within 24 hours of release.
- Real-dollar conversions must be applied to 100% of projections exceeding a 12-month horizon.
