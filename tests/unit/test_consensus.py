"""
Unit tests for Consensus Protocol.
"""
import pytest
from agents.consensus.vote_aggregator import VoteAggregator
from agents.consensus.consensus_engine import ConsensusEngine
from config.consensus_thresholds import CONSENSUS_THRESHOLD_PCT

def test_consensus_approval():
    agg = VoteAggregator()
    engine = ConsensusEngine()
    
    proposal_id = "test-prop-1"
    
    # 3 agents voting YES (Weights: Searcher=1, Stacker=1, Protector=1.5 = 3.5 total)
    # Total YES weight = 3.5. Required = 0.7 * 3.5 = 2.45.
    agg.record_vote(proposal_id, "s1", "searcher", True, "Good")
    agg.record_vote(proposal_id, "st1", "stacker", True, "Agree")
    agg.record_vote(proposal_id, "p1", "protector", True, "Safe")
    
    # Inject our mock aggregator into engine if it's singleton (actually handled by imports)
    # For unit test, we can use the global or pass it? Engines uses global.
    from agents.consensus.vote_aggregator import vote_aggregator
    vote_aggregator.clear_proposal(proposal_id)
    
    vote_aggregator.record_vote(proposal_id, "s1", "searcher", True, "Good")
    vote_aggregator.record_vote(proposal_id, "st1", "stacker", True, "Agree")
    vote_aggregator.record_vote(proposal_id, "p1", "protector", True, "Safe")
    
    res = ConsensusEngine.evaluate_proposal(proposal_id, min_voters=3)
    assert res['status'] == 'APPROVED'
    assert res['consensus_reached'] is True

def test_consensus_rejection():
    proposal_id = "test-prop-2"
    from agents.consensus.vote_aggregator import vote_aggregator
    vote_aggregator.clear_proposal(proposal_id)
    
    # 2 YES, 1 NO
    # Yes Weight: 1 + 1 = 2
    # Total Weight: 1 + 1 + 1.5 = 3.5
    # Ratio: 2 / 3.5 = ~0.57 (Below 0.70)
    vote_aggregator.record_vote(proposal_id, "s1", "searcher", True, "Good")
    vote_aggregator.record_vote(proposal_id, "st1", "stacker", True, "Agree")
    vote_aggregator.record_vote(proposal_id, "p1", "protector", False, "Too Risky")
    
    res = ConsensusEngine.evaluate_proposal(proposal_id, min_voters=3)
    assert res['status'] == 'REJECTED'
    assert res['consensus_reached'] is False

def test_pending_consensus():
    proposal_id = "test-prop-3"
    from agents.consensus.vote_aggregator import vote_aggregator
    vote_aggregator.clear_proposal(proposal_id)
    
    vote_aggregator.record_vote(proposal_id, "s1", "searcher", True, "Good")
    
    res = ConsensusEngine.evaluate_proposal(proposal_id, min_voters=3)
    assert res['status'] == 'PENDING'
