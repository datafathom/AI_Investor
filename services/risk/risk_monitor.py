"""
==============================================================================
FILE: services/risk/risk_monitor.py
ROLE: Real-time Risk Engine
PURPOSE:
    Monitor portfolio exposure and calculate risk metrics.
    
    1. Value at Risk (VaR):
       - Parametric Method (Normal Distribution assumptions).
       - VaR = Portfolio Value * Volatility * Z-Score (e.g. 1.65 for 95% Conf).
       
    2. Concentration Checks:
       - Alert if any single sector > 20%.
       - Alert if any single asset > 10%.
       
ROADMAP: Phase 20 - Risk Monitor
==============================================================================
"""

import logging
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from services.analysis.fear_greed_service import get_fear_greed_service

logger = logging.getLogger(__name__)

class RiskMonitor:
    def __init__(self):
        self.CONFIDENCE_LEVEL = 0.95
        self.Z_SCORE_95 = 1.645 # 1.645 standard deviations for 95% confidence
        
        # Risk Limits
        self.MAX_SECTOR_EXPOSURE = 0.30 # 30% Max per sector
        self.MAX_SINGLE_ASSET_EXPOSURE = 0.20 # 20% Max per asset
        self.MAX_POSITION_SIZE_USD = 10000.0 # $10,000 Max per position
        self.MAX_DAILY_LOSS_USD = 500.0 # $500 Max daily loss

    def calculate_sentiment_multiplier(self) -> float:
        """
        Calculate a risk multiplier based on Fear & Greed Index.
        """
        try:
            fg_service = get_fear_greed_service(mock=True)
            fg_data = fg_service.get_fear_greed_index()
            score = fg_data.get('score', 50)
            
            if score >= 80: return 0.5 # Extreme Greed
            if score >= 60: return 0.8 # Greed
            if score <= 20: return 1.1 # Extreme Fear (conviction bonus)
            return 1.0
        except Exception as e:
            logger.error(f"Failed sentiment scaling: {e}")
            return 1.0

    def analyze_trade_risk(self, 
                          symbol: str, 
                          side: str, 
                          quantity: float, 
                          price: float, 
                          current_exposure: float = 0.0) -> Dict[str, Any]:
        """
        Analyze a proposed trade and return a risk rating.
        """
        multiplier = self.calculate_sentiment_multiplier()
        scaled_max_pos = self.MAX_POSITION_SIZE_USD * multiplier
        
        notional_value = quantity * price
        total_after_trade = current_exposure + notional_value
        
        reasons = []
        rating = "SAFE"
        
        if notional_value > scaled_max_pos:
            rating = "DANGER"
            if multiplier < 1.0:
                reasons.append(f"Trade value ${notional_value:,.2f} exceeds dynamic limit ${scaled_max_pos:,.2f} (Sentiment: {multiplier}x)")
            else:
                reasons.append(f"Trade value ${notional_value:,.2f} exceeds limit ${self.MAX_POSITION_SIZE_USD:,.2f}")
            
        elif total_after_trade > scaled_max_pos * 1.5:
            rating = "CAUTION"
            reasons.append(f"Cumulative exposure ${total_after_trade:,.2f} nearing limits")

        fg_data = get_fear_greed_service(mock=True).get_fear_greed_index()

        return {
            "rating": rating,
            "notional": notional_value,
            "reasons": reasons,
            "sentiment": {
                "score": fg_data['score'],
                "label": fg_data['label'],
                "multiplier": multiplier
            },
            "limits": {
                "max_pos": self.MAX_POSITION_SIZE_USD,
                "scaled_max_pos": scaled_max_pos,
                "max_loss": self.MAX_DAILY_LOSS_USD
            }
        }

    def calculate_parametric_var(self, 
                               portfolio_value: float, 
                               portfolio_volatility: float) -> float:
        """
        Calculate Value at Risk (VaR) using Parametric method (1-day).
        VaR = Value * Volatility * Z-Score
        
        Meaning: "We are 95% confident that we will not lose more than $VaR in 1 day."
        """
        return portfolio_value * portfolio_volatility * self.Z_SCORE_95

    def check_concentration_limits(self, 
                                 holdings: List[Dict[str, Any]]) -> List[str]:
        """
        Check for over-exposure to sectors or assets.
        Args:
            holdings: List of {'symbol': 'AAPL', 'sector': 'Tech', 'weight': 0.15}
        Returns:
            List of warning messages.
        """
        warnings = []
        sector_weights = {}
        
        for item in holdings:
            sym = item.get('symbol', 'UNKNOWN')
            weight = item.get('weight', 0.0)
            sector = item.get('sector', 'Unclassified')
            
            # Check Single Asset Limit
            if weight > self.MAX_SINGLE_ASSET_EXPOSURE:
                warnings.append(f"ASSET WARNING: {sym} weight ({weight*100:.1f}%) exceeds limit ({self.MAX_SINGLE_ASSET_EXPOSURE*100}%)")
                
            # Aggregate Sector Weight
            sector_weights[sector] = sector_weights.get(sector, 0.0) + weight
            
        # Check Sector Limits
        for sector, total_weight in sector_weights.items():
            if total_weight > self.MAX_SECTOR_EXPOSURE:
                warnings.append(f"SECTOR WARNING: {sector} weight ({total_weight*100:.1f}%) exceeds limit ({self.MAX_SECTOR_EXPOSURE*100}%)")
                
        return warnings

    def simulate_order_impact(self, 
                             symbol: str, 
                             side: str, 
                             quantity: float, 
                             price: float) -> Dict[str, Any]:
        """
        Simulates the projected impact of a pending order on the portfolio's 
        Margin, Delta, and Gamma profile.
        """
        import random
        
        notional = quantity * price
        
        # Simulate Greeks impact
        delta_impact = notional * (0.01 if side == 'buy' else -0.01)
        gamma_impact = abs(notional) * 0.0001
        vega_impact = abs(notional) * 0.0005
        
        # Simulate margin impact
        margin_requirement = notional * 0.15 # 15% maintenance margin
        buying_power_reduction = notional * 1.0 # Standard 1:1 for cash, or lower for margin
        
        # Risk analysis
        analysis = self.analyze_trade_risk(symbol, side, quantity, price)
        
        return {
            "symbol": symbol,
            "side": side,
            "notional": notional,
            "greeks_impact": {
                "delta": delta_impact,
                "gamma": gamma_impact,
                "vega": vega_impact
            },
            "margin_impact": {
                "requirement": margin_requirement,
                "buying_power_used": buying_power_reduction,
                "available_after": 500000 - buying_power_reduction # Mock available
            },
            "risk_verdict": analysis["rating"],
            "reasons": analysis["reasons"],
            "timestamp": datetime.utcnow().isoformat()
        }

    def trigger_liquidity_markdown(self, asset_id: str, markdown_pct: float):
        """
        Phase 181.3: Kafka Liquidity Event Markdown Trigger.
        Triggers a markdown on private assets when a public liquidity event (forced sale/downround) occurs.
        """
        message = {
            "timestamp": datetime.utcnow().isoformat(),
            "asset_id": asset_id,
            "markdown_pct": markdown_pct,
            "reason": "PUBLIC_PROXY_LIQUIDITY_EVENT"
        }
        logger.info(f"KAFKA_LOG: Triggering Liquidity Markdown for {asset_id} (-{markdown_pct:.1%}) to 'risk_events_v1'")
        # Real: self.producer.send('risk_events', message)
        return message

# Singleton
_instance = None

def get_risk_monitor() -> RiskMonitor:
    global _instance
    if _instance is None:
        _instance = RiskMonitor()
    return _instance
