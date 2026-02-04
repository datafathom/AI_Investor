"""
==============================================================================
FILE: services/market/fear_greed_service.py
ROLE: Market Sentiment Analysis Service
PURPOSE: Calculates and manages the "Fear & Greed" composite index, a key 
         metric for the AI's risk assessment engine.
         
ARCHITECTURE:
    - Service Layer: Encapsulates domain logic for sentiment calculation.
    - Simulation Mode: Generates plausible market patterns (Sine/Cosine waves)
      linking VIX and Momentum proxies for MVP demonstration.
    - Pattern: Singleton instantiation (fear_greed_service).
    
DEPENDENCIES:
    - sqlalchemy (for persistence)
    - math, random (for simulation)
==============================================================================
"""
import math
import random
from datetime import timezone, datetime
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

class FearGreedService:
    """
    Service for calculating and retrieving the Fear & Greed Index.
    
    Attributes:
        db (AsyncSession, optional): Database session for persistence.
    """

    def __init__(self, db: Optional[AsyncSession] = None):
        """Initialize the service with optional DB session."""
        self.db = db

    def calculate_score(self) -> Dict[str, Any]:
        """
        Calculates a composite sentiment score.
        
        Currently runs in Simulation Mode for the MVP, generating deterministic
        but realistic-looking fluctuations based on time of day.
        
        Returns:
            Dict: {
                "score": int (0-100),
                "rating": str (e.g. "Extreme Fear"),
                "timestamp": str (ISO format),
                "components": Dict (breakdown data)
            }
        """
        # Base on time of day to create pattern equivalent to market hours
        now = datetime.now(timezone.utc)
        minute_factor = (now.minute % 60) / 60.0
        
        # Simulate volatility (VIX contribution)
        vix_score = 50 + math.sin(minute_factor * math.pi * 2) * 20
        
        # Simulate momentum
        momentum_score = 50 + math.cos(minute_factor * math.pi) * 15
        
        # Composite weightings
        final_score = int((vix_score * 0.6) + (momentum_score * 0.4))
        final_score = max(0, min(100, final_score)) # Clamp 0-100
        
        # Determine rating
        if final_score <= 25: rating = "Extreme Fear"
        elif final_score <= 45: rating = "Fear"
        elif final_score <= 55: rating = "Neutral"
        elif final_score <= 75: rating = "Greed"
        else: rating = "Extreme Greed"
        
        return {
            "score": final_score,
            "rating": rating,
            "timestamp": now.isoformat(),
            "components": {
                "vix_contribution": round(vix_score, 1),
                "momentum_score": round(momentum_score, 1),
                "social_sentiment": random.randint(30, 70) # Placeholder
            }
        }
    
    async def get_latest(self) -> Dict[str, Any]:
        """
        Async retrieval of the latest score.
        
        In production, this would fetch from Redis cache or Postgres.
        """
        # For MVP Demo, we just calculate real-time. 
        current = self.calculate_score()
        return current

# Singleton Instance
fear_greed_service = FearGreedService()
