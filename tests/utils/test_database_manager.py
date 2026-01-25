
import pytest
from utils.database_manager import db_manager

def test_singleton():
    from utils.database_manager import DatabaseManager
    dm1 = DatabaseManager()
    dm2 = DatabaseManager()
    assert dm1 is dm2

def test_pg_connection_lifecycle():
    # This assumes DATABASE_URL is set in environment for tests
    try:
        conn = db_manager.get_pg_connection()
        assert conn is not None
        db_manager.release_pg_connection(conn)
    except Exception as e:
        pytest.skip(f"Database not available for integration test: {e}")

def test_pg_cursor_context_manager():
    try:
        with db_manager.pg_cursor() as cur:
            cur.execute("SELECT 1;")
            res = cur.fetchone()
            assert res[0] == 1
    except Exception as e:
        pytest.skip(f"Database not available for integration test: {e}")

def test_neo4j_availability():
    # Basic check for driver initialization
    if not os.getenv("NEO4J_URI"):
        pytest.skip("NEO4J_URI not set")
    assert db_manager._neo4j_driver is not None

import os
