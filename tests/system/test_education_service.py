
import pytest
from unittest.mock import MagicMock
from services.system.education_service import EducationService

@pytest.fixture
def service():
    return EducationService()

@pytest.mark.asyncio
async def test_mark_tutorial_complete(service):
    user_id = "user1"
    tutorial_id = "/test/tutorial"
    
    # Should start empty
    initial_progress = await service.get_user_progress(user_id)
    assert initial_progress == []
    
    # Mark complete
    updated = await service.mark_tutorial_complete(user_id, tutorial_id)
    assert tutorial_id in updated
    assert len(updated) == 1
    
    # Check persistence
    fetched = await service.get_user_progress(user_id)
    assert fetched == [tutorial_id]

@pytest.mark.asyncio
async def test_duplicate_completion(service):
    user_id = "user1"
    tutorial_id = "/test/tutorial"
    
    await service.mark_tutorial_complete(user_id, tutorial_id)
    updated = await service.mark_tutorial_complete(user_id, tutorial_id)
    
    # Should remain 1
    assert len(updated) == 1
    assert updated[0] == tutorial_id

@pytest.mark.asyncio
async def test_multiple_users(service):
    await service.mark_tutorial_complete("user1", "tut1")
    await service.mark_tutorial_complete("user2", "tut2")
    
    u1_prog = await service.get_user_progress("user1")
    u2_prog = await service.get_user_progress("user2")
    
    assert u1_prog == ["tut1"]
    assert u2_prog == ["tut2"]
