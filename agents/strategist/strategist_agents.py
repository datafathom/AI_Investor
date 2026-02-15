from typing import Dict
from agents.base_agent import BaseAgent
from agents.strategist.logic_architect_agent import LogicArchitectAgent
from agents.strategist.stress_tester_agent import StressTesterAgent
from agents.strategist.rebalance_bot_agent import RebalanceBotAgent
from agents.strategist.opportunity_screener_agent import OpportunityScreenerAgent
from agents.strategist.edge_decay_monitor_agent import EdgeDecayMonitorAgent
from agents.strategist.playbook_evolutionist_agent import PlaybookEvolutionistAgent
from agents.strategist.conviction_analyzer_agent import ConvictionAnalyzerAgent

def get_strategist_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Strategist department agents.
    """
    return {
        "strategist.logic_architect": LogicArchitectAgent(),
        "strategist.stress_tester": StressTesterAgent(),
        "strategist.rebalance_bot": RebalanceBotAgent(),
        "strategist.opportunity_screener": OpportunityScreenerAgent(),
        "strategist.edge_decay_monitor": EdgeDecayMonitorAgent(),
        "strategist.playbook_evolutionist": PlaybookEvolutionistAgent(),
        "strategist.conviction_analyzer": ConvictionAnalyzerAgent(),
    }

