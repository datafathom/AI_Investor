# Procurement Bot (Agent 9.4)

## ID: `procurement_bot`

## Role & Objective
The 'Smart Shopper'. Analyzes household recurring purchases and identifies bulk-buying or subscription optimization opportunities.

## Logic & Algorithm
- **Consumption Analysis**: Identifies patterns in spending on essentials (groceries, utilities, supplies) using the Banker's transaction data.
- **Price Comparison**: Scans Amazon, Costco, and specialized retailers to find lower unit prices for frequently purchased items.
- **Subscription Reaper**: Flags duplicate or under-utilized digital subscriptions (e.g., multiple streaming services) for the user to "Kill".

## Inputs & Outputs
- **Inputs**:
  - `household_transaction_history` (Data): Stream of commerce alerts.
- **Outputs**:
  - `bulk_buy_recommendations` (List): Items that should be bought in volume for X% savings.
  - `subscription_kill_list` (List): Proposed cancellations.

## Acceptance Criteria
- Identify at least $100/mo in recurring savings within the first 30 days of operation.
- Achieve 95% accuracy in matching transaction strings to specific household product categories.
