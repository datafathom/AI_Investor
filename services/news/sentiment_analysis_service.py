"""
==============================================================================
FILE: services/news/sentiment_analysis_service.py
ROLE: News Sentiment Analysis Service
PURPOSE: Analyzes news sentiment using NLP, scores articles, and aggregates
         sentiment by symbol.

INTEGRATION POINTS:
    - NewsAggregationService: News articles
    - NLPService: Text analysis
    - SentimentAPI: Sentiment endpoints
    - FrontendNews: Sentiment visualization

FEATURES:
    - Article sentiment scoring
    - Symbol-level aggregation
    - Market impact assessment
    - Sentiment trends

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models.news import (
    NewsArticle, NewsSentiment, SentimentScore, MarketImpact, SectorSentiment
)
from services.news.news_aggregation_service import get_news_aggregation_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class SentimentAnalysisService:
    """
    Service for news sentiment analysis.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.news_service = get_news_aggregation_service()
        self.cache_service = get_cache_service()
        
    async def analyze_article_sentiment(
        self,
        article: NewsArticle
    ) -> NewsArticle:
        """
        Analyze sentiment of a news article.
        
        Args:
            article: News article
            
        Returns:
            NewsArticle with sentiment scores
        """
        logger.info(f"Analyzing sentiment for article {article.article_id}")
        
        # In production, would use NLP model (VADER, TextBlob, or custom model)
        # For now, use simplified keyword-based analysis
        text = f"{article.title} {article.content}".lower()
        
        # Simple keyword-based sentiment
        positive_words = ['up', 'gain', 'rise', 'bullish', 'growth', 'profit', 'beat', 'strong']
        negative_words = ['down', 'fall', 'drop', 'bearish', 'loss', 'miss', 'weak', 'decline']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        # Calculate sentiment score (-1 to 1)
        if positive_count + negative_count > 0:
            sentiment_score = (positive_count - negative_count) / (positive_count + negative_count + 1)
        else:
            sentiment_score = 0.0
        
        # Classify sentiment
        if sentiment_score > 0.3:
            sentiment_label = SentimentScore.VERY_BULLISH
        elif sentiment_score > 0.1:
            sentiment_label = SentimentScore.BULLISH
        elif sentiment_score < -0.3:
            sentiment_label = SentimentScore.VERY_BEARISH
        elif sentiment_score < -0.1:
            sentiment_label = SentimentScore.BEARISH
        else:
            sentiment_label = SentimentScore.NEUTRAL
        
        article.sentiment_score = sentiment_score
        article.sentiment_label = sentiment_label
        
        return article
    
    async def get_symbol_sentiment(
        self,
        symbol: str,
        hours_back: int = 24
    ) -> NewsSentiment:
        """
        Get aggregated sentiment for a symbol.
        
        Args:
            symbol: Stock symbol
            hours_back: Hours to look back
            
        Returns:
            NewsSentiment object
        """
        logger.info(f"Getting sentiment for {symbol}")
        
        # Get news articles
        articles = await self.news_service.get_news_for_symbol(symbol, limit=100)
        
        # Filter by time
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        recent_articles = [a for a in articles if a.published_date >= cutoff_time]
        
        # Analyze sentiment for each article
        sentiment_scores = []
        bullish_count = 0
        bearish_count = 0
        neutral_count = 0
        
        for article in recent_articles:
            analyzed = await self.analyze_article_sentiment(article)
            if analyzed.sentiment_score is not None:
                sentiment_scores.append(analyzed.sentiment_score)
                
                if analyzed.sentiment_label == SentimentScore.BULLISH or analyzed.sentiment_label == SentimentScore.VERY_BULLISH:
                    bullish_count += 1
                elif analyzed.sentiment_label == SentimentScore.BEARISH or analyzed.sentiment_label == SentimentScore.VERY_BEARISH:
                    bearish_count += 1
                else:
                    neutral_count += 1
        
        # Calculate overall sentiment
        if sentiment_scores:
            overall_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            confidence = min(1.0, len(sentiment_scores) / 10.0)  # More articles = higher confidence
        else:
            overall_sentiment = 0.0
            confidence = 0.0
        
        # Classify overall sentiment
        if overall_sentiment > 0.3:
            sentiment_label = SentimentScore.VERY_BULLISH
        elif overall_sentiment > 0.1:
            sentiment_label = SentimentScore.BULLISH
        elif overall_sentiment < -0.3:
            sentiment_label = SentimentScore.VERY_BEARISH
        elif overall_sentiment < -0.1:
            sentiment_label = SentimentScore.BEARISH
        else:
            sentiment_label = SentimentScore.NEUTRAL
        
        return NewsSentiment(
            symbol=symbol,
            overall_sentiment=overall_sentiment,
            sentiment_label=sentiment_label,
            article_count=len(recent_articles),
            bullish_count=bullish_count,
            bearish_count=bearish_count,
            neutral_count=neutral_count,
            confidence=confidence,
            last_updated=datetime.utcnow()
        )
    
    async def assess_market_impact(
        self,
        symbol: str
    ) -> MarketImpact:
        """
        Assess market impact from news sentiment.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            MarketImpact object
        """
        sentiment = await self.get_symbol_sentiment(symbol)
        
        # Calculate impact score based on sentiment strength and confidence
        impact_score = abs(sentiment.overall_sentiment) * sentiment.confidence
        
        # Determine expected direction
        if sentiment.overall_sentiment > 0.1:
            expected_direction = "up"
            expected_magnitude = abs(sentiment.overall_sentiment) * 5.0  # 0-5% change
        elif sentiment.overall_sentiment < -0.1:
            expected_direction = "down"
            expected_magnitude = abs(sentiment.overall_sentiment) * 5.0
        else:
            expected_direction = "neutral"
            expected_magnitude = 0.0
        
        # Determine time horizon (simplified)
        time_horizon = "short" if sentiment.confidence > 0.7 else "medium"
        
        return MarketImpact(
            symbol=symbol,
            impact_score=impact_score,
            expected_direction=expected_direction,
            expected_magnitude=expected_magnitude,
            confidence=sentiment.confidence,
            time_horizon=time_horizon
        )

    async def get_all_sectors_sentiment(self) -> List[SectorSentiment]:
        """
        Calculates sentiment for all primary market sectors.
        """
        sectors = [
            "Technology", "Healthcare", "Financials", 
            "Consumer Discretionary", "Consumer Staples", 
            "Energy", "Utilities", "Industrials", 
            "Materials", "Real Estate", "Communication Services"
        ]
        
        results = []
        for sector in sectors:
            # Aggregate news for the sector (using sector name as topic)
            articles = await self.news_service.fetch_news(symbols=[sector], limit=50)
            
            # Analyze each article
            scores = []
            bullish = 0
            bearish = 0
            neutral = 0
            
            for article in articles:
                analyzed = await self.analyze_article_sentiment(article)
                if analyzed.sentiment_score is not None:
                    scores.append(analyzed.sentiment_score)
                    if analyzed.sentiment_label in [SentimentScore.BULLISH, SentimentScore.VERY_BULLISH]:
                        bullish += 1
                    elif analyzed.sentiment_label in [SentimentScore.BEARISH, SentimentScore.VERY_BEARISH]:
                        bearish += 1
                    else:
                        neutral += 1
            
            # Calculate metrics
            avg_score = sum(scores) / len(scores) if scores else 0.0
            confidence = min(1.0, len(scores) / 10.0)
            
            # Simulated velocity for demo heatmap dynamics
            import random
            velocity = random.uniform(-0.5, 0.5) 

            label = SentimentScore.NEUTRAL
            if avg_score > 0.3: label = SentimentScore.VERY_BULLISH
            elif avg_score > 0.1: label = SentimentScore.BULLISH
            elif avg_score < -0.3: label = SentimentScore.VERY_BEARISH
            elif avg_score < -0.1: label = SentimentScore.BEARISH

            results.append(SectorSentiment(
                sector=sector,
                overall_sentiment=avg_score,
                sentiment_label=label,
                article_count=len(articles),
                bullish_count=bullish,
                bearish_count=bearish,
                neutral_count=neutral,
                confidence=confidence,
                velocity=velocity,
                last_updated=datetime.utcnow()
            ))
            
        return results


# Singleton instance
_sentiment_analysis_service: Optional[SentimentAnalysisService] = None


def get_sentiment_analysis_service() -> SentimentAnalysisService:
    """Get singleton sentiment analysis service instance."""
    global _sentiment_analysis_service
    if _sentiment_analysis_service is None:
        _sentiment_analysis_service = SentimentAnalysisService()
    return _sentiment_analysis_service
