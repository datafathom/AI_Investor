from typing import Dict
from agents.base_agent import BaseAgent
from agents.architect.life_cycle_modeler_agent import LifeCycleModelerAgent
from agents.architect.tax_location_optimizer_agent import TaxLocationOptimizerAgent
from agents.architect.inheritance_logic_agent import InheritanceLogicAgent
from agents.architect.inflation_architect_agent import InflationArchitectAgent
from agents.architect.real_estate_amortizer_agent import RealEstateAmortizerAgent
from agents.architect.goal_priority_arbiter_agent import GoalPriorityArbiterAgent

def get_architect_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Architect department agents.
    """
    return {
        "architect.life_cycle_modeler": LifeCycleModelerAgent(),
        "architect.tax_location_optimizer": TaxLocationOptimizerAgent(),
        "architect.inheritance_logic": InheritanceLogicAgent(),
        "architect.inflation_architect": InflationArchitectAgent(),
        "architect.real_estate_amortizer": RealEstateAmortizerAgent(),
        "architect.goal_priority_arbiter": GoalPriorityArbiterAgent(),
    }
