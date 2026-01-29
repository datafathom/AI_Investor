"""
Bull Persona Agent.
Always looks for reasons to enter a trade based on momentum and trend.
"""
from typing import Dict, Any

class BullAgent:
    @staticmethod
    def evaluate_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Highly biased towards entry if trend is UP."""
        price = proposal.get('price', 1.0)
        # Simplified logic: If it's a LONG proposal, Bull likely wants in.
        is_long = proposal.get('direction') == 'LONG'
        
        return {
            'vote': True if is_long else False,
            'reason': "Structure looks impulsive with high potential for follow-through.",
            'persona': 'bull'
        }
