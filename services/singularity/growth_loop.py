import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GrowthLoopService:
    """
    Phase 211.4: Economic Feedback Loop.
    Automatically reinvests profits into more compute (Cloud GPU rental) to spawn more agents.
    """

    def __init__(self):
        self.treasury_balance = 5000.0 # USD
        self.agent_cost_per_hour = 0.50 # GPU cost

    def process_reinvestment(self, earnings: float) -> Dict[str, Any]:
        """
        Allocates earnings to new compute.
        """
        self.treasury_balance += earnings
        logger.info(f"Treasury updated: ${self.treasury_balance:.2f}")
        
        if self.treasury_balance > 1000:
            spend = 500.0
            new_agents = int(spend / (self.agent_cost_per_hour * 24)) # 24h of agents
            self.treasury_balance -= spend
            
            logger.info(f"Reinvesting ${spend} to spawn {new_agents} new agents.")
            
            return {
                "status": "REINVESTED",
                "amount_spent": spend,
                "new_agents_spawned": new_agents,
                "remaining_balance": self.treasury_balance
            }
            
        return {"status": "ACCUMULATING", "balance": self.treasury_balance}
