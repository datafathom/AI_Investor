# Schema: News

## File Location
`schemas/news.py`

## Purpose
Pydantic models for financial news aggregation, sentiment analysis, market impact assessment, and sector-level sentiment tracking.

---

## Enums

### SentimentScore
**Sentiment classification.**

| Value | Description |
|-------|-------------|
| `VERY_NEGATIVE` | Strong negative sentiment |
| `NEGATIVE` | Negative sentiment |
| `NEUTRAL` | Neutral sentiment |
| `POSITIVE` | Positive sentiment |
| `VERY_POSITIVE` | Strong positive sentiment |

---

## Models

### NewsArticle
**Financial news article.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `article_id` | `str` | *required* | Unique article ID | Primary key |
| `title` | `str` | *required* | Article headline | Display |
| `summary` | `str` | *required* | Article summary | Quick view |
| `content` | `Optional[str]` | `None` | Full article text | Deep analysis |
| `source` | `str` | *required* | News source | Attribution |
| `url` | `str` | *required* | Original article URL | Linking |
| `author` | `Optional[str]` | `None` | Article author | Attribution |
| `symbols` | `List[str]` | `[]` | Related stock tickers | Symbol linking |
| `categories` | `List[str]` | `[]` | Topic categories | Classification |
| `published_date` | `datetime` | *required* | Publication timestamp | Ordering |
| `fetched_date` | `datetime` | *required* | When article was fetched | Ingestion timing |

---

### NewsSentiment
**Sentiment analysis for an article.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `article_id` | `str` | *required* | Analyzed article | Linking |
| `overall_sentiment` | `SentimentScore` | *required* | Overall sentiment | Primary metric |
| `sentiment_score` | `float` | *required, -1 to 1* | Numeric score | Aggregation |
| `confidence` | `float` | *required, 0-1* | Analysis confidence | Quality filter |
| `key_phrases` | `List[str]` | `[]` | Extracted key phrases | Entity extraction |
| `analysis_date` | `datetime` | *required* | When analyzed | Freshness |

---

### MarketImpact
**Predicted market impact of news.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `article_id` | `str` | *required* | Source article | Linking |
| `symbol` | `str` | *required* | Affected stock | Impact target |
| `predicted_impact` | `str` | *required* | Impact: `positive`, `negative`, `neutral` | Direction |
| `impact_magnitude` | `float` | *required* | Impact size (0-1) | Intensity |
| `time_horizon` | `str` | *required* | When impact expected | Timing |
| `confidence` | `float` | *required* | Prediction confidence | Quality |

---

### SectorSentiment
**Aggregated sector-level sentiment.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `sector` | `str` | *required* | Sector name | Identification |
| `sentiment_score` | `float` | *required* | Aggregate score | Metric |
| `article_count` | `int` | *required* | Articles analyzed | Sample size |
| `trending_topics` | `List[str]` | `[]` | Hot topics | Discovery |
| `analysis_date` | `datetime` | *required* | Analysis timestamp | Freshness |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `NewsAggregationService` | Article ingestion |
| `SentimentAnalysisService` | NLP analysis |
| `MarketImpactService` | Impact prediction |

## Frontend Components
- News dashboard (FrontendNews)
- Sentiment heat map
- Sector sentiment gauges
