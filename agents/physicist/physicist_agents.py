from typing import Dict
from agents.base_agent import BaseAgent
from agents.physicist.theta_collector_agent import ThetaCollectorAgent
from agents.physicist.volatility_surface_mapper_agent import VolatilitySurfaceMapperAgent
from agents.physicist.gamma_warning_system_agent import GammaWarningSystemAgent
from agents.physicist.delta_hedger_agent import DeltaHedgerAgent
from agents.physicist.probability_modeler_agent import ProbabilityModelerAgent
from agents.physicist.black_swan_insurance_agent_agent import BlackSwanInsuranceAgentAgent

def get_physicist_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Physicist department agents.
    """
    return {
        "physicist.theta_collector": ThetaCollectorAgent(),
        "physicist.volatility_surface_mapper": VolatilitySurfaceMapperAgent(),
        "physicist.gamma_warning_system": GammaWarningSystemAgent(),
        "physicist.delta_hedger": DeltaHedgerAgent(),
        "physicist.probability_modeler": ProbabilityModelerAgent(),
        "physicist.black_swan_insurance_agent": BlackSwanInsuranceAgentAgent(),
    }
