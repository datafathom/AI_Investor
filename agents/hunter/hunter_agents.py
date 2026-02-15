from typing import Dict
from agents.base_agent import BaseAgent
from agents.hunter.deal_flow_scraper_agent import DealFlowScraperAgent
from agents.hunter.cap_table_modeler_agent import CapTableModelerAgent
from agents.hunter.exit_catalyst_monitor_agent import ExitCatalystMonitorAgent
from agents.hunter.lotto_risk_manager_agent import LottoRiskManagerAgent
from agents.hunter.whitepaper_summarizer_agent import WhitepaperSummarizerAgent
from agents.hunter.asset_hunter_agent import AssetHunterAgent

def get_hunter_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Hunter department agents.
    """
    return {
        "hunter.deal_flow_scraper": DealFlowScraperAgent(),
        "hunter.cap_table_modeler": CapTableModelerAgent(),
        "hunter.exit_catalyst_monitor": ExitCatalystMonitorAgent(),
        "hunter.lotto_risk_manager": LottoRiskManagerAgent(),
        "hunter.whitepaper_summarizer": WhitepaperSummarizerAgent(),
        "hunter.asset_hunter": AssetHunterAgent(),
    }
