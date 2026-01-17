"""
==============================================================================
FILE: services/risk/circuit_breaker.py
ROLE: Emergency Brake System
PURPOSE:
    Halt trading automatically when risk thresholds are breached.
    
    1. Portfolio Freeze:
       - Stop ALL trading if Daily Drawdown > 3%.
       - Prevents catastrophic days (Flash Crashes).
       
    2. Asset Kill Switch:
       - Stop TRADING A SPECIFIC ASSET if it drops > 10% in short window.
       
ROADMAP: Phase 21 - Volatility Circuit Breakers
==============================================================================
"""

import logging
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(self):
        # Limits
        self.MAX_DAILY_DRAWDOWN = -0.03 # -3%
        self.ASSET_CRASH_THRESHOLD = -0.10 # -10%
        
        # State
        self.portfolio_frozen = False
        self.global_kill_switch = False
        self.frozen_assets = set()
        self.freeze_reason = None

    def trigger_global_kill_switch(self, reason: str = "Manual Emergency Halt"):
        """
        Engage the safety pin. Stop ALL trading immediately.
        """
        self.global_kill_switch = True
        self.portfolio_frozen = True
        self.freeze_reason = reason
        logger.critical(f"GLOBAL KILL SWITCH ENGAGED: {reason}")

    def is_halted(self) -> bool:
        """
        Combined check for any halt condition.
        """
        return self.portfolio_frozen or self.global_kill_switch

    def check_portfolio_freeze(self, current_daily_pnl_pct: float) -> bool:
        """
        Check if the entire portfolio should be frozen.
        """
        if self.portfolio_frozen:
            return True # Already frozen
            
        if current_daily_pnl_pct < self.MAX_DAILY_DRAWDOWN:
            self.portfolio_frozen = True
            self.freeze_reason = f"Daily Drawdown {current_daily_pnl_pct*100:.2f}% exceeded limit {self.MAX_DAILY_DRAWDOWN*100}%"
            logger.critical(f"CIRCUIT BREAKER TRIGGERED: {self.freeze_reason}")
            return True
            
        return False

    def check_asset_kill_switch(self, symbol: str, prices: List[float]) -> bool:
        """
        Check if a specific asset should be halted.
        Trigger: Drop > 10% from the high in the provided window (prices list).
        """
        if not prices:
            return False
            
        high = max(prices)
        current = prices[-1]
        
        if high <= 0:
            return False
            
        drop = (current - high) / high
        
        if drop < self.ASSET_CRASH_THRESHOLD:
            if symbol not in self.frozen_assets:
                logger.warning(f"KILL SWITCH TRIGGERED: {symbol} dropped {drop*100:.1f}%")
                self.frozen_assets.add(symbol)
            return True
            
        return False
        
    def reset(self):
        """
        Manual override to unfreeze.
        """
        self.portfolio_frozen = False
        self.global_kill_switch = False
        self.frozen_assets.clear()
        self.freeze_reason = None

# Singleton
_instance = None

def get_circuit_breaker() -> CircuitBreaker:
    global _instance
    if _instance is None:
        _instance = CircuitBreaker()
    return _instance
