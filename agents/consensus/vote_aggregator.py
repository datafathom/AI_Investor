"""
Vote Aggregator Service.
Tracks individual agent votes for specific trade proposals.
"""
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from config.consensus_thresholds import PERSONA_WEIGHTS

logger = logging.getLogger(__name__)

class VoteAggregator:
    """
    Collects and maintains voting state for in-flight trade proposals.
    """
    def __init__(self):
        # { proposal_id: { agent_id: { vote: bool, reason: str, timestamp: dt } } }
        self.votes: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def record_vote(
        self, 
        proposal_id: str, 
        agent_id: str, 
        persona: str,
        vote: bool, 
        reason: str
    ):
        """Record an agent's vote for a proposal."""
        if proposal_id not in self.votes:
            self.votes[proposal_id] = {}
            
        self.votes[proposal_id][agent_id] = {
            'persona': persona,
            'vote': vote,
            'reason': reason,
            'timestamp': datetime.utcnow(),
            'weight': PERSONA_WEIGHTS.get(persona, 1.0)
        }
        
        logger.info(f"Vote Recorded: {agent_id} ({persona}) -> {'YES' if vote else 'NO'} for {proposal_id[:8]}")

    def get_votes_summary(self, proposal_id: str) -> Dict[str, float]:
        """Aggregate weighted votes for a proposal."""
        if proposal_id not in self.votes:
            return {'yes_weight': 0.0, 'no_weight': 0.0, 'total': 0.0}

        yes_w = 0.0
        no_w = 0.0
        
        for v in self.votes[proposal_id].values():
            if v['vote']:
                yes_w += v['weight']
            else:
                no_w += v['weight']
                
        return {
            'yes_weight': yes_w,
            'no_weight': no_w,
            'total': yes_w + no_w
        }

    def clear_proposal(self, proposal_id: str):
        """Clean up memory after consensus reached or rejected."""
        if proposal_id in self.votes:
            del self.votes[proposal_id]

# Global Instance
vote_aggregator = VoteAggregator()
