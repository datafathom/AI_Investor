"""
Consensus Threshold Configurations.
Defines required agreement levels for trade deployment.
"""
from typing import Dict

# Percentage required to approve a trade
CONSENSUS_THRESHOLD_PCT = 0.70  # 70%

# Weighting per persona (usually 1.0, but some might have veto or extra weight)
PERSONA_WEIGHTS = {
    'searcher': 1.0,
    'protector': 1.5, # Protector has slightly more influence on safety
    'stacker': 1.0,
    'bull': 0.8,
    'bear': 0.8
}

def is_consensus_met(yes_votes: float, total_weight: float) -> bool:
    """
    Evaluate if the weighted yes votes meet the threshold.
    """
    if total_weight == 0:
        return False
    return (yes_votes / total_weight) >= CONSENSUS_THRESHOLD_PCT
