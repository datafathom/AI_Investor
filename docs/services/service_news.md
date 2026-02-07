# Backend Service: News (Sentiment Engine)

## Overview
The **News Service** acts as the platform's sensory organ for unstructured market data. It aggregates news from multiple providers, filters it for relevance to the user's portfolio, and applies Natural Language Processing (NLP) to generate quantitative sentiment scores. This allows the AI Investor to react not just to price action, but to the narrative driving the market.

## Core Components

### 1. News Aggregator (`news_aggregation_service.py`)
The ingestion pipeline.
- **Multi-Source Fetching**: logic to pull headlines from various APIs (currently mocked, designed for simple integration with vendors like NewsAPI or Alpha Vantage).
- **Relevance Engine**: Filters the firehose of global news down to articles that matter for the specific symbols in the user's Watchlist vs Portfolio. It boosts the "Relevance Score" based on recency and keyword matches.

### 2. Sentiment Analyzer (`sentiment_analysis_service.py`)
The NLP scoring engine.
- **Article Scoring**: Scans article titles and content for positive/negative keywords (e.g., "gain", "profit" vs "drop", "loss").
    - *Current Implementation*: Heuristic keyword counting.
    - *Architecture*: Plug-and-play compatible with advanced transformers (BERT/FinBERT).
- **Market Impact Assessment**: Combines sentiment score with "Confidence" (based on article volume) to predict potential price movement direction and magnitude.
- **Sector Heatmap**: Aggregates individual stock sentiment to gauge the mood of entire sectors (e.g., "Tech is Very Bullish," "Energy is Bearish").

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Market Dashboard** | News Feed | `news_aggregation_service.fetch_news()` | **Implemented** (`NewsFeed.jsx`) |
| **Analytics** | Sentiment Chart | `sentiment_analysis_service.get_symbol_sentiment()` | **Implemented** (`SentimentChart.jsx`) |
| **Market Overview** | Sector Heatmap | `sentiment_analysis_service.get_all_sectors_sentiment()`| **Implemented** (via `FearGreedGauge.jsx` logic) |

## Dependencies
- `textblob` or `vaderSentiment`: (Future) Libraries for upgraded sentiment analysis.
- `cache_service`: Caches API responses to prevent rate-limit exhaustion and reduce latency.

## Usage Examples

### Fetching & Analyzing News for 'AAPL'
```python
from services.news.sentiment_analysis_service import get_sentiment_analysis_service

sentiment_svc = get_sentiment_analysis_service()

# Get aggregated sentiment for the last 24 hours
sentiment = await sentiment_svc.get_symbol_sentiment(symbol="AAPL", hours_back=24)

print(f"Sentiment: {sentiment.sentiment_label} ({sentiment.overall_sentiment:.2f})")
print(f"Based on {sentiment.article_count} articles.")
print(f"Bullish/Bearish Ratio: {sentiment.bullish_count}/{sentiment.bearish_count}")
```

### Assessing Market Impact
```python
impact = await sentiment_svc.assess_market_impact(symbol="TSLA")

if impact.impact_score > 0.5:
    print(f"High Impact Alert: {impact.expected_direction.upper()} move expected.")
    print(f"Magnitude: ~{impact.expected_magnitude}%")
```
