"""
Tests for News Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.news import (
    SentimentScore,
    NewsArticle,
    NewsSentiment,
    MarketImpact
)


class TestSentimentScoreEnum:
    """Tests for SentimentScore enum."""
    
    def test_sentiment_score_enum(self):
        """Test sentiment score enum values."""
        assert SentimentScore.VERY_BEARISH == "very_bearish"
        assert SentimentScore.BEARISH == "bearish"
        assert SentimentScore.NEUTRAL == "neutral"
        assert SentimentScore.BULLISH == "bullish"
        assert SentimentScore.VERY_BULLISH == "very_bullish"


class TestNewsArticle:
    """Tests for NewsArticle model."""
    
    def test_valid_news_article(self):
        """Test valid news article creation."""
        article = NewsArticle(
            article_id='article_1',
            title='Test Article',
            content='Test content',
            source='Test Source',
            author='Test Author',
            published_date=datetime.now(),
            url='https://example.com/article',
            symbols=['AAPL'],
            sentiment_score=0.65,
            sentiment_label=SentimentScore.BULLISH,
            relevance_score=0.9
        )
        assert article.article_id == 'article_1'
        assert article.sentiment_score == 0.65
        assert article.sentiment_label == SentimentScore.BULLISH
    
    def test_news_article_optional_fields(self):
        """Test news article with optional fields."""
        article = NewsArticle(
            article_id='article_1',
            title='Test Article',
            content='Test content',
            source='Test Source',
            published_date=datetime.now()
        )
        assert article.author is None
        assert article.url is None
        assert article.sentiment_score is None


class TestNewsSentiment:
    """Tests for NewsSentiment model."""
    
    def test_valid_news_sentiment(self):
        """Test valid news sentiment creation."""
        sentiment = NewsSentiment(
            symbol='AAPL',
            overall_sentiment=0.7,
            sentiment_label=SentimentScore.BULLISH,
            article_count=10,
            bullish_count=7,
            bearish_count=1,
            neutral_count=2,
            confidence=0.85,
            last_updated=datetime.now()
        )
        assert sentiment.symbol == 'AAPL'
        assert sentiment.overall_sentiment == 0.7
        assert sentiment.bullish_count == 7


class TestMarketImpact:
    """Tests for MarketImpact model."""
    
    def test_valid_market_impact(self):
        """Test valid market impact creation."""
        impact = MarketImpact(
            symbol='AAPL',
            impact_score=0.8,
            expected_direction='up',
            expected_magnitude=0.05,
            confidence=0.75,
            time_horizon='short'
        )
        assert impact.symbol == 'AAPL'
        assert impact.impact_score == 0.8
        assert impact.expected_direction == 'up'
        assert impact.expected_magnitude == 0.05
