import logging
import yfinance as yf
from typing import Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class MarketRegime(Enum):
    BULL = "BULL"
    BEAR = "BEAR"
    TRANSITION = "TRANSITION"

class RegimeDetector:
    """
    Detects market regimes using technical trend filters.
    Primary filter: Price vs 200 SMA (SPY).
    """
    
    def detect_current_regime(self, ticker: str = "SPY") -> Dict[str, Any]:
        """
        Fetches live data and determines the regime.
        """
        logger.info(f"RegimeDetector: Fetching live data for {ticker}...")
        try:
            # Using yf.Ticker is cleaner for single symbols than download (no MultiIndex)
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period="1y")
            if hist.empty:
                raise ValueError(f"No data found for {ticker}")

            current_price = float(hist['Close'].iloc[-1])
            sma_200 = float(hist['Close'].rolling(window=200).mean().iloc[-1])
            
            # Use VIX for volatility filter if possible, otherwise default
            vix = 20.0
            try:
                vix_data = yf.download("^VIX", period="1d", interval="1d", progress=False)
                if not vix_data.empty:
                    vix = float(vix_data['Close'].iloc[-1])
            except:
                pass

            analysis = self.detect_regime(current_price, sma_200, vix)
            
            return {
                "name": analysis["regime"],
                "confidence": 0.85 if analysis["regime"] != "TRANSITION" else 0.5,
                "spy_pos": "ABOVE_SMA200" if current_price > sma_200 else "BELOW_SMA200",
                "is_risk_off": analysis["regime"] == "BEAR",
                "details": analysis
            }
        except Exception as e:
            logger.error(f"Failed to detect regime: {e}")
            return {
                "name": "UNKNOWN",
                "confidence": 0.0,
                "spy_pos": "N/A",
                "is_risk_off": False,
                "error": str(e)
            }

    def detect_regime(self, 
                      current_price: float, 
                      sma_200: float, 
                      volatility_vix: float = 20.0) -> Dict[str, Any]:
        """
        Determines the current regime based on price location and volatility.
        """
        is_above_sma = current_price > sma_200
        
        if is_above_sma and volatility_vix < 25:
            regime = MarketRegime.BULL
        elif not is_above_sma or volatility_vix > 35:
            regime = MarketRegime.BEAR
        else:
            regime = MarketRegime.TRANSITION
            
        logger.info(f"RegimeDetector: Price={current_price}, SMA200={sma_200}, VIX={volatility_vix} -> {regime.value}")
        
        return {
            "regime": regime.value,
            "trend_strength": "POSITIVE" if is_above_sma else "NEGATIVE",
            "vix_status": "HIGH" if volatility_vix > 30 else "NORMAL",
            "action_recommended": "REDUCE_BETA" if regime == MarketRegime.BEAR else "MAINTAIN_EXPOSURE"
        }
