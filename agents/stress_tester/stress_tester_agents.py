from typing import Dict
from agents.base_agent import BaseAgent
from agents.stress_tester.war_game_simulator_agent import WarGameSimulatorAgent
from agents.stress_tester.black_swan_randomizer_agent import BlackSwanRandomizerAgent
from agents.stress_tester.liquidation_optimizer_agent import LiquidationOptimizerAgent
from agents.stress_tester.cascade_failure_detector_agent import CascadeFailureDetectorAgent
from agents.stress_tester.recovery_path_planner_agent import RecoveryPathPlannerAgent
from agents.stress_tester.robustness_scorer_agent import RobustnessScorerAgent

def get_stress_tester_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Stress-Tester department agents.
    """
    return {
        "stress_tester.war_game_simulator": WarGameSimulatorAgent(),
        "stress_tester.black_swan_randomizer": BlackSwanRandomizerAgent(),
        "stress_tester.liquidation_optimizer": LiquidationOptimizerAgent(),
        "stress_tester.cascade_failure_detector": CascadeFailureDetectorAgent(),
        "stress_tester.recovery_path_planner": RecoveryPathPlannerAgent(),
        "stress_tester.robustness_scorer": RobustnessScorerAgent(),
    }
