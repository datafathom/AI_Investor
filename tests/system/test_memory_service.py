import pytest
from services.memory_service import memory_service
from utils.database_manager import get_database_manager

@pytest.mark.asyncio
async def test_memory_service_full_cycle():
    # 1. Store experience with sensitive data
    sensitive_content = "Agent executed mission. Private Key: 0x1234567890123456789012345678901234567890123456789012345678901234"
    dept_id = 1
    mission_id = "test_memory_cycle"
    
    status = await memory_service.store_experience(
        dept_id=dept_id,
        content=sensitive_content,
        mission_id=mission_id
    )
    
    assert status == "SUCCESS"
    
    # 2. Verify redaction in DB
    db = get_database_manager()
    with db.pg_cursor() as cur:
        cur.execute("SELECT content FROM agent_memories WHERE mission_id = %s", (mission_id,))
        stored_content = cur.fetchone()[0]
        assert "0x1234567" not in stored_content
        assert "[REDACTED]" in stored_content

    # 3. Recall memory
    memories = await memory_service.recall_memories("agent executed mission", limit=1)
    assert len(memories) > 0
    assert memories[0]["mission_id"] == mission_id
    assert memories[0]["similarity"] > 0.7
