import os
import logging
from typing import Dict, Any, List
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

class Neo4jService:
    """
    Service to manage Neo4j Bolt connections and execute high-speed graph queries.
    Following the Singleton pattern for connection pooling.
    """
    _instance = None
    _driver = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Neo4jService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

    @property
    def driver(self):
        """Lazy-load the Neo4j driver with dynamic config resolution."""
        if self._driver is None:
            uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
            user = os.getenv('NEO4J_USER', 'neo4j')
            password = os.getenv('NEO4J_PASSWORD', 'investor_password')
            
            try:
                self._driver = GraphDatabase.driver(
                    uri, 
                    auth=(user, password),
                    connection_timeout=5.0  # Fail fast
                )
                logger.info(f"Neo4jService: Driver initialized for {uri}")
            except Exception as e:
                logger.error(f"Neo4jService: Failed to initialize driver for {uri}: {str(e)}")
        return self._driver

    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return results as a list of dicts."""
        if not self.driver:
            logger.warning("Neo4jService: No driver available for query execution.")
            return []
            
        try:
            with self._driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Neo4jService: Query execution failed: {str(e)}")
            return []

    def close(self):
        """Close the driver connection."""
        if self._driver:
            self._driver.close()
            logger.info("Neo4jService: Connection closed.")

# Global Singleton instance
neo4j_service = Neo4jService()
