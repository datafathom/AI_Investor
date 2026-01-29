"""
Family Office CIO Consensus - Phase 75.
Multi-agent consensus for major decisions.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ConsensusEngine:
    """Multi-agent consensus engine."""
    
    def __init__(self, required_approval_pct: float = 0.70):
        self.required_pct = required_approval_pct
        self.votes: Dict[str, bool] = {}
    
    def vote(self, agent_id: str, approve: bool):
        self.votes[agent_id] = approve
    
    def get_result(self) -> Dict[str, Any]:
        if not self.votes:
            return {"approved": False, "reason": "No votes"}
        
        approval_rate = sum(1 for v in self.votes.values() if v) / len(self.votes)
        return {
            "approved": approval_rate >= self.required_pct,
            "approval_rate": approval_rate * 100,
            "required": self.required_pct * 100
        }
