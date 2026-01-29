import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SharedGoalsService:
    """Coordinates shared planning goals between multiple service providers."""
    
    def __init__(self):
        self.goals = {} # {client_id: [goals]}

    def add_coordinated_goal(self, client_id: str, goal_desc: str, stakeholders: List[str]):
        """
        stakeholders: ["ADVISOR", "CPA", "ATTORNEY"]
        """
        if client_id not in self.goals: self.goals[client_id] = []
        
        goal = {
            "description": goal_desc,
            "stakeholders": stakeholders,
            "status": "OPEN"
        }
        self.goals[client_id].append(goal)
        logger.info(f"COORDINATION_LOG: Goal '{goal_desc}' added for client {client_id} with stakeholders {stakeholders}")
        return goal
