import pytest
import json
import uuid
from datetime import datetime, timezone
from utils.database_manager import get_database_manager

@pytest.mark.asyncio
async def test_trace_db_persistence():
    db = get_database_manager()
    agent_id = f"test_trace_agent_{uuid.uuid4()}"
    content = "Thinking about the meaning of life..."
    label = "DEEP_THOUGHT"
    meta = {"confidence": 0.99, "sources": ["galaxy"]}
    
    # 1. Insert Trace
    try:
        with db.pg_cursor() as cur:
            cur.execute("""
                INSERT INTO agent_traces (agent_id, label, content, type, metadata)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (agent_id, label, content, "thought", json.dumps(meta)))
            row = cur.fetchone()
            trace_id = row[0]
            assert trace_id is not None
            print(f"Inserted trace {trace_id}")
    except Exception as e:
        pytest.fail(f"DB Insert failed: {e}")

    # 2. Query Trace Key correctness
    try:
        with db.pg_cursor() as cur:
            cur.execute("""
                SELECT agent_id, label, content, type, metadata 
                FROM agent_traces 
                WHERE id = %s
            """, (trace_id,))
            row = cur.fetchone()
            
            assert row[0] == agent_id
            assert row[1] == label
            assert row[2] == content
            assert row[3] == "thought"
            assert row[4]["confidence"] == 0.99
            
    except Exception as e:
        pytest.fail(f"DB Select failed: {e}")
        
    # 3. Cleanup
    with db.pg_cursor() as cur:
        cur.execute("DELETE FROM agent_traces WHERE agent_id = %s", (agent_id,))
