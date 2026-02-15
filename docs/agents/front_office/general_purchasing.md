# General Purchasing Agent (Agent 14.7)

## ID: `general_purchasing_agent`

## Role & Objective
The 'Shopping Advocate'. Handles finding the best prices for specific general home or office items across approved vendors (Amazon, Costco, Staples, etc.), optimizing for both cost and delivery speed.

## Logic & Algorithm
- **Web Scraping / API Search**: Queries approved vendor catalogs for a specific product SKU or description.
- **Price Normalization**: Compares "Total Cost" including shipping, taxes, and potential bulk-buy discounts.
- **Vendor Reliability Check**: Prioritizes vendors with high fulfillment ratings and the fastest estimated delivery.

## Inputs & Outputs
- **Inputs**:
  - `purchase_request` (Dict): Item name, quantity, and optional max budget.
- **Outputs**:
  - `price_comparison_report` (List): Top 3 vendor options ranked by cost/speed.
  - `purchase_link` (URI): Direct link to the optimized checkout page.

## Acceptance Criteria
- Identify the lowest price for 95% of standard office/home items across 5+ vendors.
- Provide a price comparison report within 60 seconds of a request.
