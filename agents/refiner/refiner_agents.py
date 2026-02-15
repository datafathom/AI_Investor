from typing import Dict
from agents.base_agent import BaseAgent
from agents.refiner.hallucination_sentinel_agent import HallucinationSentinelAgent
from agents.refiner.token_efficiency_reaper_agent import TokenEfficiencyReaperAgent
from agents.refiner.performance_reviewer_agent import PerformanceReviewerAgent
from agents.refiner.prompt_optimizer_agent import PromptOptimizerAgent
from agents.refiner.model_router_agent import ModelRouterAgent
from agents.refiner.context_window_manager_agent import ContextWindowManagerAgent

def get_refiner_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Refiner department agents.
    """
    return {
        "refiner.hallucination_sentinel": HallucinationSentinelAgent(),
        "refiner.token_efficiency_reaper": TokenEfficiencyReaperAgent(),
        "refiner.performance_reviewer_agent": PerformanceReviewerAgent(),
        "refiner.prompt_optimizer": PromptOptimizerAgent(),
        "refiner.model_router": ModelRouterAgent(),
        "refiner.context_window_manager": ContextWindowManagerAgent(),
    }
