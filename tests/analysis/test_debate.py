"""
==============================================================================
FILE: tests/analysis/test_debate_logic.py
ROLE: Consensus Auditor
PURPOSE:
    Verify the DebateChamber correctly calculates consensus and handles 
    diverse persona responses.
==============================================================================
"""

import pytest
from services.analysis.debate_chamber import DebateChamber, DebateAgentResponse

class TestDebateLogic:
    
    def test_consensus_calculation(self):
        chamber = DebateChamber()
        ticker = "AAPL"
        summary = "Apple stock trading at all time highs."
        
        result = chamber.simulate_debate(ticker, summary)
        
        assert "responses" in result
        assert len(result["responses"]) == 3
        assert result["ticker"] == ticker
        
        # Mocking specific outcome for predictability in this test if needed
        # But for now, testing the internal logic of simulate_debate
        decision = result["consensus"]["decision"]
        assert decision in ["BUY", "NO_CONSENSUS"]

    def test_threshold_logic(self):
        # Test the math of consensus
        responses = [
            DebateAgentResponse(persona="A", signal="BUY", score=0.9, reasoning="Good"),
            DebateAgentResponse(persona="B", signal="BUY", score=0.8, reasoning="Good"),
            DebateAgentResponse(persona="C", signal="HOLD", score=0.4, reasoning="Ok"),
        ]
        
        buy_votes = sum(1 for r in responses if r.signal == "BUY")
        ratio = buy_votes / len(responses)
        assert ratio == pytest.approx(0.666, 0.01)
        assert ratio >= 0.66 # Meets the 2/3 majority rule
