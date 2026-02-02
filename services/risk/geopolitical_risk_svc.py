import logging
import random
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class GeopoliticalRiskService:
    """
    Phase 187.1: Geopolitical Risk & 'Total War' Simulator.
    Analyzes the impact of extreme geopolitical events and market fear.
    """
    
    def simulate_total_war(self, asset_allocation: Dict[str, float]) -> Dict[str, Any]:
        """
        Phase 187.1: Total War Event Simulator.
        Tests 'Left Tail' risk outcomes for diverse global portfolios.
        """
        # Scenario impact mapping (randomized for sim)
        scenarios = {
            "GLOBAL_CONFLICT": {"Equities": -0.40, "Bonds": -0.10, "Gold": 0.25, "Commodities": 0.30},
            "REGIONAL_SKIRMISH": {"Equities": -0.15, "Bonds": -0.05, "Gold": 0.10, "Commodities": 0.15},
            "CYBER_WARFARE": {"Equities": -0.25, "Bonds": -0.02, "Gold": 0.15, "Commodities": 0.05}
        }
        
        selected_scenario = random.choice(list(scenarios.keys()))
        impacts = scenarios[selected_scenario]
        
        total_impact = 0.0
        details = {}
        
        for asset, weight in asset_allocation.items():
            impact = impacts.get(asset, -0.20) # Default heavy hit
            weighted_impact = weight * impact
            total_impact += weighted_impact
            details[asset] = round(weighted_impact, 4)
            
        logger.info(f"GEORISK_LOG: Total War Sim: {selected_scenario}. Overall Impact: {total_impact:.2%}")
        
        return {
            "scenario": selected_scenario,
            "total_portfolio_impact": round(total_impact, 4),
            "asset_breakdown": details,
            "risk_tier": "CRITICAL" if total_impact < -0.20 else "HIGH"
        }

    def calculate_geopolitical_fear_score(self, vix: float, put_call_ratio: float, news_sentiment: float) -> Dict[str, Any]:
        """
        Phase 187.3: Geopolitical Fear Score.
        Determines if fear is currently over-bid in the options market.
        """
        # Fear score normalized 0-1
        # High VIX + High Put/Call + Low News Sentiment = High Fear
        fear_score = (vix / 50.0) * 0.4 + (put_call_ratio / 2.0) * 0.4 + (1.0 - news_sentiment) * 0.2
        fear_score = min(max(fear_score, 0.0), 1.0)
        
        is_overbid = fear_score > 0.8
        
        logger.info(f"GEORISK_LOG: Geopolitical Fear Score: {fear_score:.2f}. Overbid: {is_overbid}")
        
        return {
            "fear_score": round(fear_score, 2),
            "is_fear_overbid": is_overbid,
            "market_efficiency": "INEFFICIENT" if is_overbid else "EFFICIENT",
            "recommendation": "BET_AGAINST_FEAR" if is_overbid else "MAINTAIN_HEDGES"
        }
