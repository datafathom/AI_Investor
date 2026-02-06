"""
Columnist Department Agents (2.1 - 2.6)
Phase 2 Implementation: The Data Forge

The Columnist Department is the Intelligence Network - 
aggregating, filtering, and scoring financial news from 50+ sources.

ACCEPTANCE CRITERIA from Phase_2_ImplementationPlan.md:
- Agent 2.1: Ingest 100% of RSS feeds with <30s latency to Neo4j
- Agent 2.2: DistilBERT sentiment matches 90% human labels
- Agent 2.4: Trigger alert within 500ms on 4σ price variance
"""

import logging
import time
import re
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider

logger = logging.getLogger(__name__)


@dataclass
class NewsArticle:
    """A scraped news article with metadata."""
    article_id: str
    source: str
    title: str
    content: str
    url: str
    published_at: datetime
    scraped_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tickers: List[str] = field(default_factory=list)
    sentiment_score: Optional[float] = None
    sentiment_magnitude: Optional[float] = None


class ScraperGeneralAgent(BaseAgent):
    """
    Agent 2.1: The Scraper-General
    
    Orchestrates the news ingestion pipeline from 50+ financial sources.
    Uses RSS feeds, Playwright for JavaScript-heavy sites, and API integrations.
    
    Acceptance Criteria:
    - Ingest 100% of whitelisted RSS feeds
    - <30s latency between article post and Neo4j node creation
    """

    # Whitelisted RSS sources
    RSS_SOURCES = [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://www.reutersagency.com/feed/?taxonomy=best-sectors",
        "https://seekingalpha.com/feed.xml",
        "https://www.wsj.com/xml/rss/3_7085.xml",
        "https://finance.yahoo.com/rss/",
    ]

    # Ticker extraction pattern (uppercase 1-5 letters)
    TICKER_PATTERN = re.compile(r'\$([A-Z]{1,5})\b|\b([A-Z]{2,5})\b')

    def __init__(self) -> None:
        super().__init__(name="columnist.scraper.2.1", provider=ModelProvider.GEMINI)
        self.articles_ingested: int = 0
        self.ingestion_queue: List[NewsArticle] = []
        self.source_health: Dict[str, bool] = {}

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process scraping events and orchestrate the pipeline."""
        event_type = event.get("type", "")

        if event_type == "scrape.rss":
            return self._scrape_rss_feed(event)
        elif event_type == "scrape.article":
            return self._process_article(event)
        elif event_type == "health.check":
            return self._check_source_health()

        return None

    def _scrape_rss_feed(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape an RSS feed and queue articles for processing."""
        source_url = event.get("url", "")
        
        # In production, use feedparser or aiohttp
        logger.info(f"Scraping RSS: {source_url[:50]}...")
        
        # Mock article extraction
        articles_found = event.get("articles", [])
        
        for article_data in articles_found:
            article = NewsArticle(
                article_id=hashlib.md5(article_data.get("url", "").encode()).hexdigest()[:16],
                source=source_url,
                title=article_data.get("title", ""),
                content=article_data.get("content", ""),
                url=article_data.get("url", ""),
                published_at=datetime.now(timezone.utc),
                tickers=self._extract_tickers(article_data.get("title", "")),
            )
            self.ingestion_queue.append(article)
        
        self.articles_ingested += len(articles_found)
        
        return {
            "status": "scraped",
            "source": source_url,
            "articles_found": len(articles_found),
            "queue_size": len(self.ingestion_queue),
        }

    def _process_article(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process and enrich a single article."""
        start_time = time.perf_counter()
        
        article_data = event.get("article", {})
        article = NewsArticle(
            article_id=hashlib.md5(article_data.get("url", "").encode()).hexdigest()[:16],
            source=article_data.get("source", "unknown"),
            title=article_data.get("title", ""),
            content=article_data.get("content", ""),
            url=article_data.get("url", ""),
            published_at=datetime.now(timezone.utc),
            tickers=self._extract_tickers(article_data.get("title", "")),
        )
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        return {
            "status": "processed",
            "article_id": article.article_id,
            "tickers": article.tickers,
            "latency_ms": elapsed_ms,
            "under_30s_sla": elapsed_ms < 30000,
        }

    def _extract_tickers(self, text: str) -> List[str]:
        """Extract stock tickers from text."""
        matches = self.TICKER_PATTERN.findall(text.upper())
        tickers = []
        for match in matches:
            ticker = match[0] or match[1]
            if ticker and len(ticker) <= 5:
                tickers.append(ticker)
        return list(set(tickers))[:10]  # Limit to 10 tickers

    def _check_source_health(self) -> Dict[str, Any]:
        """Check health status of all RSS sources."""
        return {
            "status": "health_report",
            "sources_total": len(self.RSS_SOURCES),
            "sources_healthy": sum(1 for v in self.source_health.values() if v),
            "articles_ingested": self.articles_ingested,
        }


class SentimentAnalystAgent(BaseAgent):
    """
    Agent 2.2: The Sentiment Analyst
    
    Scores all ingested articles using DistilBERT for financial sentiment.
    
    Acceptance Criteria:
    - 90% accuracy against human-labeled "Trade Sentiment" dataset
    - Real-time scoring: <100ms per article
    """

    # Sentiment categories
    SENTIMENT_CATEGORIES = ["BULLISH", "BEARISH", "NEUTRAL"]

    def __init__(self) -> None:
        super().__init__(name="columnist.sentiment.2.2", provider=ModelProvider.GEMINI)
        self.articles_scored: int = 0
        self.accuracy_samples: List[bool] = []

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process sentiment scoring requests."""
        event_type = event.get("type", "")

        if event_type == "sentiment.score":
            return self._score_article(event)
        elif event_type == "sentiment.batch":
            return self._batch_score(event)
        elif event_type == "accuracy.feedback":
            return self._record_feedback(event)

        return None

    def _score_article(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Score a single article for financial sentiment."""
        start_time = time.perf_counter()
        
        text = event.get("text", "")
        article_id = event.get("article_id", "unknown")
        
        # Simple keyword-based scoring (in production: use DistilBERT)
        score, magnitude = self._analyze_sentiment(text)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        self.articles_scored += 1
        
        return {
            "status": "scored",
            "article_id": article_id,
            "sentiment_score": score,  # -1.0 (bearish) to 1.0 (bullish)
            "sentiment_magnitude": magnitude,  # 0.0 to 1.0 (strength)
            "category": self._categorize(score),
            "latency_ms": elapsed_ms,
            "under_100ms_sla": elapsed_ms < 100,
        }

    def _batch_score(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Score multiple articles in batch."""
        articles = event.get("articles", [])
        results = []
        
        for article in articles:
            result = self._score_article({
                "type": "sentiment.score",
                "text": article.get("text", ""),
                "article_id": article.get("id", ""),
            })
            results.append(result)
        
        return {
            "status": "batch_scored",
            "count": len(results),
            "avg_latency_ms": sum(r["latency_ms"] for r in results) / len(results) if results else 0,
        }

    def _analyze_sentiment(self, text: str) -> tuple[float, float]:
        """
        Analyze text for financial sentiment.
        
        Returns (score, magnitude):
        - score: -1.0 (bearish) to 1.0 (bullish)
        - magnitude: 0.0 to 1.0 (confidence/strength)
        """
        text_lower = text.lower()
        
        bullish_words = ["surge", "gain", "profit", "growth", "beat", "strong", "upgrade", "buy"]
        bearish_words = ["drop", "loss", "decline", "weak", "miss", "downgrade", "sell", "crash"]
        
        bullish_count = sum(1 for word in bullish_words if word in text_lower)
        bearish_count = sum(1 for word in bearish_words if word in text_lower)
        
        total = bullish_count + bearish_count
        if total == 0:
            return 0.0, 0.1  # Neutral, low confidence
        
        score = (bullish_count - bearish_count) / total
        magnitude = min(total / 10, 1.0)  # Cap at 1.0
        
        return round(score, 4), round(magnitude, 4)

    def _categorize(self, score: float) -> str:
        """Categorize sentiment score."""
        if score > 0.2:
            return "BULLISH"
        elif score < -0.2:
            return "BEARISH"
        return "NEUTRAL"

    def _record_feedback(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Record accuracy feedback for model improvement."""
        was_correct = event.get("correct", True)
        self.accuracy_samples.append(was_correct)
        
        if len(self.accuracy_samples) > 100:
            self.accuracy_samples = self.accuracy_samples[-100:]
        
        accuracy = sum(self.accuracy_samples) / len(self.accuracy_samples) * 100
        
        return {
            "status": "feedback_recorded",
            "current_accuracy": accuracy,
            "meets_90pct_sla": accuracy >= 90.0,
        }


class AnomalyScoutAgent(BaseAgent):
    """
    Agent 2.4: The Anomaly Scout
    
    Monitors for statistical anomalies in price movements.
    
    Acceptance Criteria:
    - Trigger alert within 500ms of detecting >4σ variance from 30-min mean
    """

    def __init__(self) -> None:
        super().__init__(name="columnist.anomaly.2.4", provider=ModelProvider.GEMINI)
        self.price_windows: Dict[str, List[float]] = {}
        self.alerts_triggered: int = 0
        self.sigma_threshold: float = 4.0

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process price updates and detect anomalies."""
        event_type = event.get("type", "")

        if event_type == "price.update":
            return self._check_anomaly(event)
        elif event_type == "price.batch":
            return self._batch_update(event)

        return None

    def _check_anomaly(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if a price update is anomalous."""
        start_time = time.perf_counter()
        
        ticker = event.get("ticker", "")
        price = event.get("price", 0.0)
        
        if ticker not in self.price_windows:
            self.price_windows[ticker] = []
        
        window = self.price_windows[ticker]
        window.append(price)
        
        # Keep 30-minute window (assuming 1-min intervals)
        if len(window) > 30:
            window.pop(0)
        
        # Need at least 5 data points to calculate meaningful stats
        if len(window) < 5:
            return None
        
        # Calculate z-score
        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return None
        
        z_score = abs(price - mean) / std_dev
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        if z_score > self.sigma_threshold:
            self.alerts_triggered += 1
            logger.warning(f"LETHAL ANOMALY: {ticker} at {z_score:.2f}σ (price={price}, mean={mean:.2f})")
            
            return {
                "status": "ALERT",
                "alert_type": "lethal_anomaly",
                "ticker": ticker,
                "price": price,
                "mean": mean,
                "z_score": z_score,
                "latency_ms": elapsed_ms,
                "under_500ms_sla": elapsed_ms < 500,
            }
        
        return None

    def _batch_update(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process batch price updates."""
        updates = event.get("updates", [])
        alerts = []
        
        for update in updates:
            result = self._check_anomaly({
                "type": "price.update",
                "ticker": update.get("ticker"),
                "price": update.get("price"),
            })
            if result:
                alerts.append(result)
        
        return {
            "status": "batch_processed",
            "updates_count": len(updates),
            "alerts_triggered": len(alerts),
        }


class RumorTrackerAgent(BaseAgent):
    """
    Agent 2.3: The Rumor Tracker
    
    Monitors social media and forums for emerging narratives.
    """

    def __init__(self) -> None:
        super().__init__(name="columnist.rumor.2.3", provider=ModelProvider.GEMINI)
        self.rumors_tracked: int = 0

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process rumor tracking events."""
        event_type = event.get("type", "")

        if event_type == "rumor.detect":
            return self._track_rumor(event)

        return None

    def _track_rumor(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Track and categorize a rumor."""
        source = event.get("source", "")
        content = event.get("content", "")
        tickers = event.get("tickers", [])
        
        self.rumors_tracked += 1
        
        return {
            "status": "tracked",
            "rumor_id": self.rumors_tracked,
            "source": source,
            "tickers": tickers,
            "credibility_score": 0.5,  # Placeholder
        }


class MacroOracleAgent(BaseAgent):
    """
    Agent 2.5: The Macro Oracle
    
    Analyzes macroeconomic indicators and FRED data.
    """

    def __init__(self) -> None:
        super().__init__(name="columnist.macro.2.5", provider=ModelProvider.GEMINI)

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process macro analysis requests."""
        event_type = event.get("type", "")

        if event_type == "macro.analyze":
            return self._analyze_macro(event)

        return None

    def _analyze_macro(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze macroeconomic data."""
        indicator = event.get("indicator", "")
        
        return {
            "status": "analyzed",
            "indicator": indicator,
            "trend": "neutral",
            "impact_sectors": [],
        }


class CatalystMapperAgent(BaseAgent):
    """
    Agent 2.6: The Catalyst Mapper
    
    Identifies and tracks upcoming catalysts (earnings, splits, etc.).
    """

    def __init__(self) -> None:
        super().__init__(name="columnist.catalyst.2.6", provider=ModelProvider.GEMINI)

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process catalyst mapping requests."""
        event_type = event.get("type", "")

        if event_type == "catalyst.map":
            return self._map_catalyst(event)

        return None

    def _map_catalyst(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Map and track a catalyst event."""
        ticker = event.get("ticker", "")
        catalyst_type = event.get("catalyst_type", "")
        
        return {
            "status": "mapped",
            "ticker": ticker,
            "catalyst_type": catalyst_type,
            "expected_impact": "medium",
        }


# =============================================================================
# Agent Registry
# =============================================================================

def get_columnist_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Columnist department agents.
    """
    return {
        "columnist.scraper.2.1": ScraperGeneralAgent(),
        "columnist.sentiment.2.2": SentimentAnalystAgent(),
        "columnist.rumor.2.3": RumorTrackerAgent(),
        "columnist.anomaly.2.4": AnomalyScoutAgent(),
        "columnist.macro.2.5": MacroOracleAgent(),
        "columnist.catalyst.2.6": CatalystMapperAgent(),
    }
