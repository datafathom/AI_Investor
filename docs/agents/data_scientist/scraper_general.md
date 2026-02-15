# Scraper General (Agent 3.1)

## ID: `scraper_general`

## Role & Objective
The primary data ingestion engine. Orchestrates scrapers for news, social media, and financial filings.

## Logic & Algorithm
- Schedules periodic scrapes of whitelisted financial domains.
- Sanitizes HTML/PDF content into clean text for LLM processing.
- Extracts structured metadata (Tickers, Sentiment, Keywords).

## Inputs & Outputs
- **Inputs**:
  - `target_url` (str): The domain or endpoint to scrape.
  - `extraction_schema` (Dict): Fields to extract (e.g., 'price', 'headline').
- **Outputs**:
  - `raw_payload` (str): Cleaned text content.
  - `entities` (List): Tickers and names found in the text.

## Acceptance Criteria
- Clean 99% of HTML boilerplate (ads, navbars) from ingested content.
- Support parallel scraping of up to 50 concurrent domains.
