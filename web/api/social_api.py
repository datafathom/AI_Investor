from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
from pydantic import BaseModel
import logging

from services.social.sentiment_analyzer import SentimentAnalyzer
from services.social.trend_detector import TrendDetector

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/social", tags=["Social"])

# --- Sentiment Endpoints ---

@router.get("/sentiment/top")
async def get_top_sentiment_movers(limit: int = 5):
    service = SentimentAnalyzer()
    return await service.get_top_sentiment_movers(limit)

@router.get("/sentiment/{ticker}")
async def get_ticker_sentiment(ticker: str):
    service = SentimentAnalyzer()
    return await service.get_ticker_sentiment(ticker)

@router.get("/sentiment/{ticker}/history")
async def get_sentiment_history(ticker: str, days: int = 7):
    service = SentimentAnalyzer()
    return await service.get_sentiment_history(ticker, days)

@router.get("/correlation/{ticker}")
async def get_sentiment_correlation(ticker: str):
    service = SentimentAnalyzer()
    return await service.get_correlation(ticker)

# --- Trend Endpoints ---

@router.get("/trends")
async def get_trends():
    service = TrendDetector()
    return await service.get_trends()

@router.get("/trends/{topic}")
async def get_trend_details(topic: str):
    service = TrendDetector()
    trend = await service.get_trend_details(topic)
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    return trend
