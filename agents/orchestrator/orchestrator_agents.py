from typing import Dict
from agents.base_agent import BaseAgent
from agents.orchestrator.synthesizer_agent import SynthesizerAgent
from agents.orchestrator.command_interpreter_agent import CommandInterpreterAgent
from agents.orchestrator.traffic_controller_agent import TrafficControllerAgent
from agents.orchestrator.layout_morphologist_agent import LayoutMorphologistAgent
from agents.orchestrator.red_team_sentry_agent import RedTeamSentryAgent
from agents.orchestrator.context_weaver_agent import ContextWeaverAgent

def get_orchestrator_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Orchestrator department agents.
    """
    return {
        "orchestrator.synthesizer": SynthesizerAgent(),
        "orchestrator.command_interpreter": CommandInterpreterAgent(),
        "orchestrator.traffic_controller": TrafficControllerAgent(),
        "orchestrator.layout_morphologist": LayoutMorphologistAgent(),
        "orchestrator.red_team_sentry": RedTeamSentryAgent(),
        "orchestrator.context_weaver": ContextWeaverAgent(),
    }
