"""
==============================================================================
FILE: services/analysis/fear_greed_service.py
ROLE: Fear & Greed Composite Index Service
PURPOSE: 
    Proprietary master metric for market emotion. Fuses Google Trends,
    Social sentiment, VIX proxy, and Put/Call ratio into a 0-100 scale.
    
    - < 20: Extreme Fear (High-probability buying opportunity)
    - 20-40: Fear
    - 40-60: Neutral
    - 60-80: Greed
    - > 80: Extreme Greed (Risk mitigation window)

USAGE:
    service = FearGreedIndexService()
    result = service.get_fear_greed_index(symbols=["AAPL", "TSLA", "SPY"])

ROADMAP: Phase 12 - The "Fear & Greed" Composite Index
==============================================================================
"""

import logging
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime

from services.data.google_trends import GoogleTrendsService
from services.data.options_service import OptionsFlowService
from services.data.reddit_service import RedditService
from services.data.fred_service import FredMacroService

logger = logging.getLogger(__name__)


class FearGreedIndexService:
    """
    Calculates a composite Fear & Greed Index (0-100) by fusing multiple
    sentiment and market data sources.
    
    Components (Equal Weight by Default):
    1. Retail Sentiment (Google Trends) - 25%
    2. Social Sentiment (Reddit/FinBERT) - 25%
    3. Smart Money (Put/Call Ratio) - 25%
    4. Macro Risk (VIX proxy via FRED) - 25%
    """
    
    # Strategic thresholds
    EXTREME_FEAR_THRESHOLD = 20
    FEAR_THRESHOLD = 40
    GREED_THRESHOLD = 60
    EXTREME_GREED_THRESHOLD = 80
    
    def __init__(self, mock: bool = False):
        self.mock = mock
        self.trends_service = GoogleTrendsService(mock=mock)
        self.options_service = OptionsFlowService(mock=mock)
        self.reddit_service = RedditService()  # No mock param - uses credentials or falls back to mock
        self.macro_service = FredMacroService(mock=mock)
        
    def get_fear_greed_index(
        self, 
        symbols: Optional[List[str]] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculate the composite Fear & Greed Index.
        
        Args:
            symbols: List of tickers to analyze (defaults to market proxies)
            weights: Custom component weights (must sum to 1.0)
            
        Returns:
            {
                "score": 45.5,
                "label": "FEAR",
                "timestamp": "2026-01-16T21:10:00Z",
                "components": {
                    "retail_sentiment": {...},
                    "social_sentiment": {...},
                    "smart_money": {...},
                    "macro_risk": {...}
                },
                "signal": "BUY" | "HOLD" | "SELL",
                "recommendation": "..."
            }
        """
        symbols = symbols or ["SPY", "QQQ", "AAPL", "TSLA", "NVDA"]
        weights = weights or {
            "retail_sentiment": 0.25,
            "social_sentiment": 0.25,
            "smart_money": 0.25,
            "macro_risk": 0.25
        }
        
        # Validate weights
        if not np.isclose(sum(weights.values()), 1.0):
            logger.warning("Weights don't sum to 1.0, normalizing...")
            total = sum(weights.values())
            weights = {k: v/total for k, v in weights.items()}
        
        # Fetch component scores (all normalized 0-100)
        components = {}
        
        # 1. Retail Sentiment (Google Trends)
        retail_score, retail_details = self._calculate_retail_sentiment(symbols)
        components["retail_sentiment"] = {
            "score": retail_score,
            "weight": weights["retail_sentiment"],
            "details": retail_details
        }
        
        # 2. Social Sentiment (Reddit)
        social_score, social_details = self._calculate_social_sentiment(symbols)
        components["social_sentiment"] = {
            "score": social_score,
            "weight": weights["social_sentiment"],
            "details": social_details
        }
        
        # 3. Smart Money (Put/Call Ratio)
        smart_score, smart_details = self._calculate_smart_money_sentiment(symbols)
        components["smart_money"] = {
            "score": smart_score,
            "weight": weights["smart_money"],
            "details": smart_details
        }
        
        # 4. Macro Risk (VIX proxy)
        macro_score, macro_details = self._calculate_macro_risk()
        components["macro_risk"] = {
            "score": macro_score,
            "weight": weights["macro_risk"],
            "details": macro_details
        }
        
        # Calculate Weighted Composite Score
        composite_score = sum(
            components[key]["score"] * components[key]["weight"]
            for key in components
        )
        composite_score = round(float(composite_score), 2)
        
        # Determine Label
        label = self._score_to_label(composite_score)
        
        # Generate Signal & Recommendation
        signal, recommendation = self._generate_signal(composite_score, label)
        
        result = {
            "score": composite_score,
            "label": label,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "components": components,
            "signal": signal,
            "recommendation": recommendation,
            "thresholds": {
                "extreme_fear": self.EXTREME_FEAR_THRESHOLD,
                "fear": self.FEAR_THRESHOLD,
                "greed": self.GREED_THRESHOLD,
                "extreme_greed": self.EXTREME_GREED_THRESHOLD
            }
        }
        
        logger.info(f"Fear & Greed Index: {composite_score} ({label}) - Signal: {signal}")
        return result
    
    def _calculate_retail_sentiment(self, symbols: List[str]) -> tuple[float, Dict]:
        """
        Converts Google Trends z-scores to 0-100 sentiment.
        Higher trending = more greed, lower = more fear.
        """
        try:
            trend_data = self.trends_service.get_trend_score(symbols)
            
            if not trend_data:
                return 50.0, {"error": "No trend data available"}
            
            # Average z-score across symbols
            z_scores = []
            for symbol, data in trend_data.items():
                if isinstance(data, dict) and "z_score" in data:
                    z_scores.append(data["z_score"])
            
            if not z_scores:
                return 50.0, {"error": "No valid z-scores"}
                
            avg_z = np.mean(z_scores)
            
            # Map z-score (-3 to +3) to 0-100
            # z=-3 -> 0 (extreme fear), z=0 -> 50, z=+3 -> 100 (extreme greed)
            score = float(np.clip((avg_z + 3) / 6 * 100, 0, 100))
            
            return round(score, 2), {
                "avg_z_score": round(avg_z, 3),
                "symbols_analyzed": len(z_scores),
                "raw_data": trend_data
            }
        except Exception as e:
            logger.error(f"Error calculating retail sentiment: {e}")
            return 50.0, {"error": str(e)}
    
    def _calculate_social_sentiment(self, symbols: List[str]) -> tuple[float, Dict]:
        """
        Reddit/Social sentiment from FinBERT (-1 to +1) mapped to 0-100.
        """
        try:
            # Get sentiment using track_mentions
            sentiment_data = self.reddit_service.track_mentions(symbols[:3])  # Limit API calls
            
            if not sentiment_data:
                return 50.0, {"error": "No social sentiment data"}
            
            # track_mentions returns {ticker: {"mentions": int, "sentiment": float}}
            # Aggregate sentiment across tickers
            sentiments = []
            total_mentions = 0
            for ticker, data in sentiment_data.items():
                if isinstance(data, dict):
                    sentiments.append(data.get("sentiment", 0))
                    total_mentions += data.get("mentions", 0)
            
            if not sentiments:
                return 50.0, {"error": "No sentiment scores available"}
            
            # FinBERT returns -1 to +1, map to 0-100
            avg_sentiment = np.mean(sentiments)
            score = float(np.clip((avg_sentiment + 1) / 2 * 100, 0, 100))
            
            return round(score, 2), {
                "avg_sentiment": round(avg_sentiment, 3),
                "total_mentions": total_mentions,
                "tickers_analyzed": len(sentiments)
            }
        except Exception as e:
            logger.error(f"Error calculating social sentiment: {e}")
            return 50.0, {"error": str(e)}
    
    def _calculate_smart_money_sentiment(self, symbols: List[str]) -> tuple[float, Dict]:
        """
        Put/Call ratio interpretation:
        - Low P/C (< 0.7) = Bullish (Greed) = High score
        - High P/C (> 1.0) = Bearish (Fear) = Low score
        """
        try:
            # Average P/C across symbols
            pc_ratios = []
            for symbol in symbols[:3]:  # Limit API calls
                options_data = self.options_service.get_options_sentiment(symbol)
                if isinstance(options_data, (float, int)):
                    pc_ratios.append(float(options_data))
                elif isinstance(options_data, dict):
                    pc_ratios.append(float(options_data.get("put_call_ratio", 1.0)))
            
            if not pc_ratios:
                return 50.0, {"error": "No options data available"}
            
            avg_pc = np.mean(pc_ratios)
            
            # Map P/C ratio (0.5 to 1.5) to score (100 to 0)
            # Lower P/C = more greed, Higher P/C = more fear
            score = float(np.clip((1.5 - avg_pc) / 1.0 * 100, 0, 100))
            
            return round(score, 2), {
                "avg_put_call_ratio": round(avg_pc, 3),
                "symbols_analyzed": len(pc_ratios),
                "interpretation": "BULLISH" if avg_pc < 0.7 else "BEARISH" if avg_pc > 1.0 else "NEUTRAL"
            }
        except Exception as e:
            logger.error(f"Error calculating smart money sentiment: {e}")
            return 50.0, {"error": str(e)}
    
    def _calculate_macro_risk(self) -> tuple[float, Dict]:
        """
        Macro health from FRED data:
        - Expansion = High score (Greed)
        - Recession Warning = Low score (Fear)
        """
        try:
            macro_data = self.macro_service.get_macro_regime()
            
            status = macro_data.get("status", "EXPANSION")
            
            # Map regime to score
            score_map = {
                "EXPANSION": 75.0,
                "STABLE": 60.0,
                "CAUTION": 40.0,
                "RECESSION_WARNING": 20.0,
                "RECESSION": 5.0
            }
            score = score_map.get(status, 50.0)
            
            return score, {
                "regime": status,
                "yield_curve": macro_data.get("yield_curve", {}),
                "unemployment": macro_data.get("unemployment", {})
            }
        except Exception as e:
            logger.error(f"Error calculating macro risk: {e}")
            return 50.0, {"error": str(e)}
    
    def _score_to_label(self, score: float) -> str:
        """Convert numeric score to human-readable label."""
        if score < self.EXTREME_FEAR_THRESHOLD:
            return "EXTREME_FEAR"
        elif score < self.FEAR_THRESHOLD:
            return "FEAR"
        elif score < self.GREED_THRESHOLD:
            return "NEUTRAL"
        elif score < self.EXTREME_GREED_THRESHOLD:
            return "GREED"
        else:
            return "EXTREME_GREED"
    
    def _generate_signal(self, score: float, label: str) -> tuple[str, str]:
        """Generate trading signal and recommendation based on score."""
        if label == "EXTREME_FEAR":
            return "BUY", "High-probability buying opportunity. Consider shifting from Defensive to Aggressive portfolio allocation."
        elif label == "FEAR":
            return "ACCUMULATE", "Market fear elevated. Good entry point for long-term positions."
        elif label == "NEUTRAL":
            return "HOLD", "Market sentiment balanced. Maintain current allocation strategy."
        elif label == "GREED":
            return "REDUCE", "Market optimism high. Consider taking some profits."
        else:  # EXTREME_GREED
            return "SELL", "Risk mitigation window. Shift from Aggressive to Defensive portfolio allocation."


# Singleton pattern for manager access
_instance: Optional[FearGreedIndexService] = None

def get_fear_greed_service(mock: bool = False) -> FearGreedIndexService:
    """Get or create singleton instance of FearGreedIndexService."""
    global _instance
    if _instance is None:
        _instance = FearGreedIndexService(mock=mock)
    return _instance
