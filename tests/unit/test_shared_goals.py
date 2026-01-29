import pytest
from services.coordination.shared_goals import SharedGoalsService

def test_shared_goal_addition():
    service = SharedGoalsService()
    goal = service.add_coordinated_goal("client_123", "Estate Trust Creation", ["ADVISOR", "ATTORNEY"])
    assert goal["description"] == "Estate Trust Creation"
    assert "ATTORNEY" in goal["stakeholders"]
    assert service.goals["client_123"][0]["status"] == "OPEN"
