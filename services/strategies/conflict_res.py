"""
Quantamental Disagreement Analyzer.
Resolves conflicts when signals diverge.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DisagreementAnalyzer:
    """Arbitrates conflicting strategy signals."""
    
    def resolve_conflict(self, ticker: str, signals: Dict[str, str]) -> str:
        # Implementation: If Tech=BUY but Macro=SELL, SELL wins.
        if signals.get("macro") == "SELL":
             logger.info(f"ARBITRATION: Macro override SELL for {ticker}")
             return "SELL"
        return signals.get("tech", "HOLD")
