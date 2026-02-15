from typing import Dict
from agents.base_agent import BaseAgent
from agents.auditor.slippage_sleuth_agent import SlippageSleuthAgent
from agents.auditor.behavioral_analyst_agent import BehavioralAnalystAgent
from agents.auditor.benchmarker_agent import BenchmarkerAgent
from agents.auditor.fee_forensic_agent_agent import FeeForensicAgentAgent
from agents.auditor.reconciliation_bot_agent import ReconciliationBotAgent
from agents.auditor.mistake_classifier_agent import MistakeClassifierAgent

def get_auditor_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Auditor department agents.
    """
    return {
        "auditor.slippage_sleuth": SlippageSleuthAgent(),
        "auditor.behavioral_analyst": BehavioralAnalystAgent(),
        "auditor.benchmarker": BenchmarkerAgent(),
        "auditor.fee_forensic_agent": FeeForensicAgentAgent(),
        "auditor.reconciliation_bot": ReconciliationBotAgent(),
        "auditor.mistake_classifier": MistakeClassifierAgent(),
    }
