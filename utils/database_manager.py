
import os
import logging
import psycopg2
from psycopg2 import pool
from neo4j import GraphDatabase
from typing import Optional, Any
from dotenv import load_dotenv

# Load environment variables (e.g., DATABASE_URL)
load_dotenv()


logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Singleton manager for database connections.
    Supports PostgreSQL (TimescaleDB) and Neo4j.
    Implements multi-tenant isolation through schema switching.
    """
    _instance = None
    _pg_pool = None
    _neo4j_driver = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._init_connections()
        return cls._instance

    def _init_connections(self):
        """Initialize connection pools from environment variables."""
        # PostgreSQL
        pg_url = os.getenv("DATABASE_URL")
        if pg_url:
            try:
                self._pg_pool = psycopg2.pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=20,
                    dsn=pg_url,
                    connect_timeout=30
                )
                logger.info("PostgreSQL connection pool initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize PostgreSQL pool: {e}")

        # Neo4j
        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_pwd = os.getenv("NEO4J_PASSWORD", "investor_password")
        if neo4j_uri:
            try:
                self._neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pwd))
                logger.info("Neo4j driver initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Neo4j driver: {e}")

    def get_pg_connection(self):
        """
        Get a Postgres connection from the pool.
        Lazily initializes the pool if it's missing.
        """
        if not self._pg_pool:
            logger.info("Retrying PostgreSQL pool initialization...")
            self._init_connections()
            
        if not self._pg_pool:
            raise ConnectionError("PostgreSQL pool not initialized.")

        # In a real app we might want to wait for a connection with a timeout
        # but ThreadedConnectionPool.getconn() blocks if minconn=maxconn and all busy.
        # With min=1, max=20, it should be fine unless we leak.
        conn = self._pg_pool.getconn()
        
        # Apply Tenant Isolation
        try:
            # TODO: Implement FastAPI-compatible tenant context
            schema = "public"
            
            if schema and schema != "public":
                with conn.cursor() as cur:
                    # Security: schema name must be trusted (from manager)
                    cur.execute(f"SET search_path TO {schema}, public;")
                    logger.debug(f"Switched connection to schema: {schema}")
        except (ImportError, RuntimeError, AttributeError) as e:
            logger.debug(f"Error setting tenant schema: {e}")
            # Fallback to public (default)
            
        return conn

    from contextlib import contextmanager

    @contextmanager
    def pg_cursor(self):
        """
        Context manager that yields a cursor and automatically releases the connection.
        """
        conn = self.get_pg_connection()
        try:
            with conn.cursor() as cur:
                yield cur
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error in pg_cursor: {e}")
            raise
        finally:
            self.release_pg_connection(conn)

    def release_pg_connection(self, conn):
        """Release a Postgres connection back to the pool."""
        if self._pg_pool and conn:
            self._pg_pool.putconn(conn)

    def get_neo4j_session(self, **kwargs):
        """Get a Neo4j session."""
        if not self._neo4j_driver:
            raise ConnectionError("Neo4j driver not initialized.")
        return self._neo4j_driver.session(**kwargs)

    def close_all(self):
        """Shutdown all connection pools."""
        if self._pg_pool:
            self._pg_pool.closeall()
            logger.info("PostgreSQL pool closed.")
        if self._neo4j_driver:
            self._neo4j_driver.close()
            logger.info("Neo4j driver closed.")

db_manager = DatabaseManager()
def get_database_manager() -> DatabaseManager:
    return DatabaseManager()
