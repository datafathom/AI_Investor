"""
Unit tests for Searcher Agent.
"""
import pytest
from agents.searcher_agent import SearcherAgent

class TestSearcherAgent:
    @pytest.fixture
    def agent(self):
        return SearcherAgent()

    def test_scan_market(self, agent):
        # Trigger scan
        event = {"type": "SCAN_TRIGGER"}
        result = agent.process_event(event)
        
        assert result["action"] == "SCAN_COMPLETE"
        assert "opportunities" in result
        assert isinstance(result["opportunities"], list)
        
        # Check if patterns are scored
        if len(result["opportunities"]) > 0:
            opp = result["opportunities"][0]
            assert "score" in opp
            assert "symbol" in opp
            assert opp["score"] >= 0

    def test_scan_storage(self, agent):
        event = {"type": "SCAN_TRIGGER"}
        agent.process_event(event)
        results = agent.get_last_scan_results()
        assert results == agent.scan_results
