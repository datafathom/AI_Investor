# Real Estate Amortizer (Agent 2.5)

## ID: `real_estate_amortizer`

## Role & Objective
The property debt specialist. It manages the intricate mathematics of real estate leverage, tracking equity growth, mortgage amortization, and rental yield.

## Logic & Algorithm
1. **Amortization Modeling**: Tracks the exact split of principal vs interest for all property debt.
2. **Equity Curve Generation**: Maps future equity build-up based on scheduled payments and regional appreciation.
3. **IRR Calculation**: Determines the Internal Rate of Return for properties including leverage impacts.

## Inputs & Outputs
- **Inputs**:
  - Mortgage Terms (Principal, Rate, Length)
  - Current Property Appraisals
  - Rental Cash Flow Data
- **Outputs**:
  - Equity Build-up Curve
  - Cash-on-Cash Return Metrics

## Acceptance Criteria
- Principal/Interest splits must be accurate to the cent compared to official bank statements.
- Equity projections must include at least three scenarios (Bear, Base, Bull appreciation).
