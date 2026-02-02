import logging
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class ForcedSellerService:
    """
    Phase 190.1: Michael Green 'Forced Seller' Liquidity Tracker.
    Tracks passive fund flows and fragility.
    """
    
    def monitor_passive_flow(self, ticker: str, passive_ownership_pct: float) -> Dict[str, Any]:
        """
        Scores the fragility based on passive ownership concentration.
        High passive ownership = Higher price-elasticity (Green's Thesis).
        """
        # 0-1 scale of fragility
        fragility_score = passive_ownership_pct / 100.0
        
        risk_level = "LOW"
        if fragility_score > 0.4: risk_level = "ELEVATED"
        if fragility_score > 0.7: risk_level = "CRITICAL"
        
        logger.info(f"LIQUIDITY_LOG: {ticker} passive fragility: {fragility_score:.2f} ({risk_level})")
        
        return {
            "ticker": ticker,
            "passive_concentration": passive_ownership_pct,
            "fragility_score": round(fragility_score, 2),
            "risk_level": risk_level,
            "notes": "Driven by structural inelasticity in passive fund mandates."
        }

    def detect_liquidity_trap(self, current_spread: float, avg_spread: float) -> Dict[str, Any]:
        """
        Phase 190.2: Liquidity Trap Detector.
        """
        spread_expansion = current_spread / avg_spread if avg_spread > 0 else 1.0
        is_trapped = spread_expansion > 2.5
        
        logger.info(f"LIQUIDITY_LOG: Spread expansion: {spread_expansion:.2f}x. Trap: {is_trapped}")
        
        return {
            "spread_expansion": round(spread_expansion, 2),
            "is_liquidity_trap": is_trapped,
            "severity": "HIGH" if is_trapped else "NORMAL",
            "action": "HALT_ACTIVE_TRADING" if is_trapped else "CONTINUE"
        }
