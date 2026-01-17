
import os
import logging
import psycopg2
from psycopg2 import pool
from neo4j import GraphDatabase
from typing import Optional, Any
from flask import g

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
                    dsn=pg_url
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
        Automatically sets the search_path based on the current tenant context.
        """
        if not self._pg_pool:
            raise ConnectionError("PostgreSQL pool not initialized.")

        conn = self._pg_pool.getconn()
        
        # Apply Tenant Isolation
        try:
            from services.auth.tenant_manager import tenant_manager
            schema = tenant_manager.get_current_tenant_schema()
            
            with conn.cursor() as cur:
                # Security: schema name must be trusted (from manager)
                cur.execute(f"SET search_path TO {schema}, public;")
                logger.debug(f"Switched connection to schema: {schema}")
        except Exception as e:
            logger.error(f"Failed to set tenant schema context: {e}")
            # Fallback to public for safety (or raise error depending on policy)
            
        return conn

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
