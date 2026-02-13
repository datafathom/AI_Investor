import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ConsensusEngine:
    """Multi-agent consensus engine with weighted voting."""
    
    def __init__(self, session_id: str, required_approval_pct: float = 70.0):
        self.session_id = session_id
        self.required_pct = required_approval_pct # 0-100 scale
        self.votes: Dict[str, Dict[str, Any]] = {}
        self.is_finalized = False
        self.human_override = None

    def cast_vote(self, agent_id: str, vote: str, confidence: float = 1.0, reasoning: str = ""):
        """
        Cast a vote. 
        vote: 'APPROVE', 'REJECT', 'ABSTAIN'
        confidence: 0.0 - 1.0 multiplier
        """
        if self.is_finalized:
            logger.warning(f"Session {self.session_id} is finalized. Vote ignored.")
            return

        self.votes[agent_id] = {
            "vote": vote,
            "confidence": confidence,
            "reasoning": reasoning,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def set_human_override(self, decision: str, reasoning: str):
        """Force a decision by human intervention."""
        self.human_override = {
            "decision": decision,
            "reasoning": reasoning,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.is_finalized = True

    def calculate_results(self) -> Dict[str, Any]:
        """Calculate weighted consensus."""
        if self.human_override:
            return {
                "decision": self.human_override["decision"],
                "approval_pct": 100.0 if self.human_override["decision"] == "APPROVE" else 0.0,
                "is_override": True,
                "reasoning": self.human_override["reasoning"],
                "votes": self.votes
            }

        if not self.votes:
            return {
                "decision": "PENDING", 
                "approval_pct": 0.0, 
                "details": "No votes cast",
                "votes": {}
            }
        
        total_weight = 0.0
        approval_weight = 0.0
        
        for v in self.votes.values():
            if v["vote"] == "ABSTAIN":
                continue
            
            weight = v.get("confidence", 1.0)
            total_weight += weight
            
            if v["vote"] == "APPROVE":
                approval_weight += weight
        
        if total_weight == 0:
            return {"decision": "PENDING", "approval_pct": 0.0}

        approval_pct = (approval_weight / total_weight) * 100
        decision = "APPROVE" if approval_pct >= self.required_pct else "REJECT"

        return {
            "decision": decision,
            "approval_pct": round(approval_pct, 1),
            "required_pct": self.required_pct,
            "total_votes": len(self.votes),
            "votes": self.votes
        }

# Global registry of active consensus engines
# In a real app, this would be in Redis or DB
consensus_sessions: Dict[str, ConsensusEngine] = {}

def get_consensus_engine(session_id: str) -> ConsensusEngine:
    if session_id not in consensus_sessions:
        consensus_sessions[session_id] = ConsensusEngine(session_id)
    return consensus_sessions[session_id]
