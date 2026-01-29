"""
Bear Persona Agent.
Skeptical agent looking for reasons NOT to enter (Risk/Overextension).
"""
from typing import Dict, Any

class BearAgent:
    @staticmethod
    def evaluate_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Biased against entry if RSI is high or near resistance."""
        return {
            'vote': False,
            'reason': "Market looks overextended. We are approaching major daily resistance levels.",
            'persona': 'bear'
        }
