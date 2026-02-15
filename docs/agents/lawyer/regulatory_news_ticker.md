# Regulatory News Ticker (Agent 11.5)

## ID: `regulatory_news_ticker`

## Role & Objective
The 'Policy Watcher'. Monitors legislative changes, SEC filings, and IRS code updates that impact the Sovereign OS's logic or tactical roadmap.

## Logic & Algorithm
- **Source Aggregation**: Scans federal registries, financial law blogs, and SEC press releases.
- **Alert Filtering**: Uses LLM-based summarization to extract the "Financial Impact" for the user specifically.
- **Logic Update Trigger**: Recommends updates to the Tax-Loss Harvester or Wash-Sale Watchdog if statutory limits change.

## Inputs & Outputs
- **Inputs**:
  - `legislative_rss_feeds` (Stream): Raw legal news updates.
- **Outputs**:
  - `regulatory_impact_summary` (str): Plain-English explanation of rule changes.

## Acceptance Criteria
- Alert the user of any relevant tax-code changes within 24 hours of their announcement.
- Categorize 100% of news items by "Impact Level" (Low, Medium, High).
