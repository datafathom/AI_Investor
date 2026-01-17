
import unittest
from unittest.mock import MagicMock, patch
import os

# Mock psycopg2 and neo4j before importing DatabaseManager
with patch('psycopg2.pool.ThreadedConnectionPool'), patch('neo4j.GraphDatabase.driver'):
    from utils.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Reset singleton for each test
        DatabaseManager._instance = None
        
    @patch('psycopg2.pool.ThreadedConnectionPool')
    def test_singleton_behavior(self, mock_pool):
        dm1 = DatabaseManager()
        dm2 = DatabaseManager()
        self.assertIs(dm1, dm2)

    @patch('psycopg2.pool.ThreadedConnectionPool')
    @patch('services.auth.tenant_manager.tenant_manager.get_current_tenant_schema')
    def test_pg_connection_schema_switching(self, mock_get_schema, mock_pool):
        # Setup mocks
        mock_get_schema.return_value = "tenant_alpha"
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        dm = DatabaseManager()
        dm._pg_pool = MagicMock()
        dm._pg_pool.getconn.return_value = mock_conn
        
        # Action
        conn = dm.get_pg_connection()
        
        # Verify
        mock_cursor.execute.assert_called_with("SET search_path TO tenant_alpha, public;")
        self.assertEqual(conn, mock_conn)

    @patch('psycopg2.pool.ThreadedConnectionPool')
    def test_pg_connection_error_no_pool(self, mock_pool):
        dm = DatabaseManager()
        dm._pg_pool = None
        with self.assertRaises(ConnectionError):
            dm.get_pg_connection()

if __name__ == '__main__':
    unittest.main()
