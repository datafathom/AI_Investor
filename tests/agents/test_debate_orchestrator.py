import pytest
from services.agents.debate_orchestrator import DebateOrchestrator

class TestDebateOrchestrator:
    @pytest.fixture
    def orchestrator(self):
        # Reset singleton logic
        DebateOrchestrator._instance = None
        return DebateOrchestrator()

    def test_start_debate(self, orchestrator):
        session = orchestrator.start_debate("TSLA")
        assert session["ticker"] == "TSLA"
        assert len(session["transcript"]) == 1
        assert session["transcript"][0]["persona"] == "The Bull"

    def test_inject_argument(self, orchestrator):
        orchestrator.start_debate("AAPL")
        
        # Inject user argument
        orchestrator.inject_argument("user1", "I think demand is slowing down.")
        
        transcript = orchestrator.active_session["transcript"]
        
        # Should have: 
        # 1. Bull Opening
        # 2. User Argument
        # 3. Agent Response (Likely Bear since argument is bearish/neutral, or Bull defending)
        assert len(transcript) == 3
        
        user_msg = transcript[1]
        assert user_msg["persona"] == "User"
        assert user_msg["reasoning"] == "I think demand is slowing down."
        assert user_msg["id"] is not None

        response_msg = transcript[2]
        assert response_msg["role"] == "AI Agent"
        assert response_msg["parent_id"] == user_msg["id"]
