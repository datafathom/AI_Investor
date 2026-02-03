"""
Verification script for Phase 13.
Simulates a multi-agent debate (Bull vs. Bear) and ensures consensus triggers correctly.
"""
import sys
import os
import uuid
from unittest.mock import MagicMock, patch

# Ensure paths
sys.path.append(os.getcwd())

from agents.consensus.vote_aggregator import vote_aggregator
from agents.consensus.consensus_engine import ConsensusEngine
from agents.personas.bull_agent import BullAgent
from agents.personas.bear_agent import BearAgent

def run_verification():
    print("=== Starting Phase 13 Verification ===")
    
    proposal_id = str(uuid.uuid4())
    proposal = {
        'symbol': 'EUR/USD',
        'direction': 'LONG',
        'price': 1.0850
    }

    print("\n[1/3] Gathering Persona Votes...")
    
    # 1. Bull Agent evaluates
    bull_vote = BullAgent.evaluate_proposal(proposal)
    vote_aggregator.record_vote(proposal_id, "bull-1", "bull", bull_vote['vote'], bull_vote['reason'])
    
    # 2. Bear Agent evaluates
    bear_vote = BearAgent.evaluate_proposal(proposal)
    vote_aggregator.record_vote(proposal_id, "bear-1", "bear", bear_vote['vote'], bear_vote['reason'])
    
    # 3. Searcher (Standard) approves
    vote_aggregator.record_vote(proposal_id, "searcher-1", "searcher", True, "System signal matched.")

    # 4. Protector (Safety) approves
    vote_aggregator.record_vote(proposal_id, "protector-1", "protector", True, "Hedge coverage sufficient.")

    print("\n[2/3] Evaluating Swarm Consensus...")
    
    # We have:
    # Bull: YES (Weight 0.8)
    # Bear: NO  (Weight 0.8)
    # Searcher: YES (Weight 1.0)
    # Protector: YES (Weight 1.5)
    
    # Yes Weight: 0.8 + 1.0 + 1.5 = 3.3
    # Total Weight: 3.3 + 0.8 = 4.1
    # Ratio: 3.3 / 4.1 = 0.804 (Matches > 70% threshold)
    
    result = ConsensusEngine.evaluate_proposal(proposal_id, min_voters=4)
    
    print(f"Status: {result['status']}")
    print(f"Confidence Ratio: {result['yes_weight'] / result['total_weight']:.2f}")
    
    if result['status'] == 'APPROVED' and result['consensus_reached']:
        print("✅ Consensus Engine successfully aggregated swarm decisions.")
    else:
        print("❌ Consensus logic failure.")
        return False

    print("\n[3/3] Analyzing Dissent Logs...")
    dissent = ConsensusEngine.get_dissent_log(proposal_id)
    
    print(f"Dissent Count: {len(dissent)}")
    for d in dissent:
        print(f"Agent: {d['agent_id']} ({d['persona']}) - Reason: {d['reason']}")

    if len(dissent) == 1 and dissent[0]['persona'] == 'bear':
        print("✅ Dissent forensics successfully captured Bear agent reservations.")
    else:
        print("❌ Dissent logging mismatch.")
        return False

    print("\n=== Phase 13 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
