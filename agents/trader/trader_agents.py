from typing import Dict
from agents.base_agent import BaseAgent
from agents.trader.sniper_agent import SniperAgent
from agents.trader.exit_manager_agent import ExitManagerAgent
from agents.trader.arbitrageur_agent import ArbitrageurAgent
from agents.trader.liquidity_scout_agent import LiquidityScoutAgent
from agents.trader.position_sizer_agent import PositionSizerAgent
from agents.trader.flash_crash_circuit_breaker_agent import FlashCrashCircuitBreakerAgent

def get_trader_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Trader department agents.
    """
    return {
        "trader.sniper": SniperAgent(),
        "trader.exit_manager": ExitManagerAgent(),
        "trader.arbitrageur": ArbitrageurAgent(),
        "trader.liquidity_scout": LiquidityScoutAgent(),
        "trader.position_sizer": PositionSizerAgent(),
        "trader.flash_crash_circuit_breaker": FlashCrashCircuitBreakerAgent(),
    }
