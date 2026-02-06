import pytest
from utils.database_manager import get_database_manager

@pytest.mark.asyncio
async def test_pgvector_extension():
    db = get_database_manager()
    with db.pg_cursor() as cur:
        cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector';")
        res = cur.fetchone()
        assert res is not None, "pgvector extension not installed"

@pytest.mark.asyncio
async def test_agent_memories_table_exists():
    db = get_database_manager()
    with db.pg_cursor() as cur:
        cur.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'agent_memories';")
        res = cur.fetchone()
        assert res is not None, "agent_memories table does not exist"

@pytest.mark.asyncio
async def test_vector_insertion_and_search():
    db = get_database_manager()
    # 768 dimension mock vector
    mock_vector = [0.1] * 768
    
    with db.pg_cursor() as cur:
        # Cleanup mock
        cur.execute("DELETE FROM agent_memories WHERE mission_id = 'test_integration_vector';")
        
        # Insert
        cur.execute("""
            INSERT INTO agent_memories (dept_id, mission_id, content, embedding)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (999, "test_integration_vector", "Test integrating vectors", mock_vector))
        
        # Recall by similarity
        cur.execute("""
            SELECT mission_id, 1 - (embedding <=> %s::vector) AS similarity 
            FROM agent_memories 
            WHERE mission_id = 'test_integration_vector'
            ORDER BY similarity DESC LIMIT 1;
        """, (mock_vector,))
        res = cur.fetchone()
        assert res[0] == "test_integration_vector"
        assert res[1] > 0.99
