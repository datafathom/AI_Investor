from typing import Dict
from agents.base_agent import BaseAgent
from agents.data_scientist.scraper_general_agent import ScraperGeneralAgent
from agents.data_scientist.backtest_autopilot_agent import BacktestAutopilotAgent
from agents.data_scientist.correlation_detective_agent import CorrelationDetectiveAgent
from agents.data_scientist.anomaly_scout_agent import AnomalyScoutAgent
from agents.data_scientist.yield_optimizer_agent import YieldOptimizerAgent
from agents.data_scientist.macro_correlation_engine_agent import MacroCorrelationEngineAgent

def get_data_scientist_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Data Scientist department agents.
    """
    return {
        "data_scientist.scraper_general": ScraperGeneralAgent(),
        "data_scientist.backtest_autopilot": BacktestAutopilotAgent(),
        "data_scientist.correlation_detective": CorrelationDetectiveAgent(),
        "data_scientist.anomaly_scout": AnomalyScoutAgent(),
        "data_scientist.yield_optimizer": YieldOptimizerAgent(),
        "data_scientist.macro_correlation_engine": MacroCorrelationEngineAgent(),
    }
