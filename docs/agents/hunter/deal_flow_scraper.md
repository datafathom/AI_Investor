# Deal Flow Scraper (Agent 7.1)

## ID: `deal_flow_scraper`

## Role & Objective
The 'Venture Ingester'. Aggregates private market opportunities from Angellist, Crunchbase, and institutional deal rooms.

## Logic & Algorithm
- Scans whitelisted newsletters and venture portals for new 'Series A/B' rounds.
- Categorizes deals by sector (SaaS, AI, Biotech).
- Checks if the deal lead is a top-tier VC firm.

## Inputs & Outputs
- **Inputs**:
  - `scraper_sources` (List): Domains to monitor.
  - `min_valuation_cap` (float): Floor for considering a deal.
- **Outputs**:
  - `deal_funnel` (List): Filtered opportunities for the 'Cap-Table Modeler'.

## Acceptance Criteria
- Monitor 10+ venture sources daily with 0% missed deal announcements.
- Deduplicate deal flow across multiple sources with 99% accuracy.
