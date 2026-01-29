"""
Scenario Preset Library.
Stores and manages custom what-if scenarios.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ScenarioLibrary:
    """Manages custom simulation scenarios."""
    
    def __init__(self):
        self.scenarios = {
            "ZOMBIE_APOCALYPSE": {"vix": 80, "oil": 10, "gold": 5000},
            "TECH_BUBBLE_BURST": {"nasdaq": -40, "bond_yields": 6.5}
        }
        
    def add_scenario(self, name: str, params: Dict[str, float]):
        self.scenarios[name.upper()] = params
        
    def get_all(self) -> Dict[str, Any]:
        return self.scenarios
