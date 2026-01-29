"""
Consensus Engine.
Evaluates vote batches and determines if a trade can proceed.
"""
import logging
from typing import Dict, List, Any, Optional
from config.consensus_thresholds import is_consensus_met
from agents.consensus.vote_aggregator import vote_aggregator

logger = logging.getLogger(__name__)

class ConsensusEngine:
    """
    Core engine for multi-agent consensus protocols.
    """

    @staticmethod
    def evaluate_proposal(proposal_id: str, min_voters: int = 3) -> Dict[str, Any]:
        """
        Evaluate current votes for a proposal.
        """
        # 1. Get raw votes
        summary = vote_aggregator.get_votes_summary(proposal_id)
        
        # 2. Count distinct voters
        voter_count = len(vote_aggregator.votes.get(proposal_id, {}))
        
        if voter_count < min_voters:
            return {
                'status': 'PENDING',
                'voters': voter_count,
                'required': min_voters,
                'consensus_reached': False
            }

        # 3. Check weighting
        reached = is_consensus_met(summary['yes_weight'], summary['total'])
        
        status = 'APPROVED' if reached else 'REJECTED'
        
        return {
            'status': status,
            'voters': voter_count,
            'yes_weight': summary['yes_weight'],
            'total_weight': summary['total'],
            'consensus_reached': reached
        }

    @staticmethod
    def get_dissent_log(proposal_id: str) -> List[Dict]:
        """Collect reasoning from dissenting votes."""
        votes = vote_aggregator.votes.get(proposal_id, {})
        return [
            {
                'agent_id': aid,
                'persona': v['persona'],
                'reason': v['reason']
            } for aid, v in votes.items() if not v['vote']
        ]
