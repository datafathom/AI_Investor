# Columnist Department Agents (`columnist/columnist_agents.py`)

The Columnist department is the "Intelligence Agency" of the Sovereign OS, responsible for ingestion and sentiment analysis of news, rumors, and catalysts.

## Scraper General Agent (Agent 2.1)
### Description
The `ScraperGeneralAgent` is a high-bandwidth ingestion engine that monitors RSS feeds, Twitter (X), and financial news portals.

### Integration
- **Ticker Extraction**: Automatically identifies mentions of $TICKER symbols in news text.
- **Preprocessing**: Cleans and stores news articles for the `SentimentAnalystAgent`.

---

## Sentiment Analyst Agent (Agent 2.2)
### Description
The `SentimentAnalystAgent` assigns quantitative sentiment scores to news articles.

### Integration
- **Scoring**: Maps articles to a score of -1.0 (Bearish) to +1.0 (Bullish).
- **Pipelines**: Feeds synthesized sentiment scores to the `StackerAgent` for trade weighting.

---

## Anomaly Scout Agent (Agent 2.4)
### Description
The `AnomalyScoutAgent` monitors price feeds for statistical outliers (exceeding 4σ variance).

### Integration
- **Trigger**: High-volatility detections are pushed to the `LayoutMorphologistAgent` to update the user HUD.

---

## Macro Oracle Agent (Agent 2.5)
### Description
The `MacroOracleAgent` analyzes high-level economic indicators such as CPI, GDP, and Fed interest rate decisions.

---

## Catalyst Mapper Agent (Agent 2.6)
### Description
The `CatalystMapperAgent` builds a timeline of upcoming market events (Earnings, FDA approvals, Halvings).

### Integration
- **Neo4j**: Maps catalysts to specific assets in the knowledge graph.
