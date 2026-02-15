from typing import Dict
from agents.base_agent import BaseAgent
from agents.historian.journal_entry_agent_agent import JournalEntryAgentAgent
from agents.historian.regime_classifier_agent import RegimeClassifierAgent
from agents.historian.ghost_decision_overlay_agent import GhostDecisionOverlayAgent
from agents.historian.pattern_recognition_bot_agent import PatternRecognitionBotAgent
from agents.historian.decision_replay_engine_agent import DecisionReplayEngineAgent
from agents.historian.timeline_curator_agent import TimelineCuratorAgent

def get_historian_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Historian department agents.
    """
    return {
        "historian.journal_entry_agent": JournalEntryAgentAgent(),
        "historian.regime_classifier": RegimeClassifierAgent(),
        "historian.ghost_decision_overlay": GhostDecisionOverlayAgent(),
        "historian.pattern_recognition_bot": PatternRecognitionBotAgent(),
        "historian.decision_replay_engine": DecisionReplayEngineAgent(),
        "historian.timeline_curator": TimelineCuratorAgent(),
    }
