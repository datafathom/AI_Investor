import os
import logging
from typing import Dict, Any, List

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
        self._mode = os.getenv("NEO4J_MODE", "LIVE")
        self._mock_checked = False
        if self._mode == "MOCK":
            logger.info("Neo4jService: Forced MOCK mode via environment variable.")

    def _check_availability(self, host: str, port: int) -> bool:
        """Perform a quick socket check to see if the port is open."""
        import socket
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False
        except Exception:
            return False

    @property
    def driver(self):
        """Lazy-load the Neo4j driver with dynamic config resolution and fast-fail mode."""
        if self._driver is None and self._mode == "LIVE":
            uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
            user = os.getenv('NEO4J_USER', 'neo4j')
            password = os.getenv('NEO4J_PASSWORD', 'investor_password')
            
            # Fast-fail check
            if not self._mock_checked:
                try:
                    # Robust URI parsing
                    import re
                    match = re.search(r'://([^:/]+)(?::(\d+))?', uri)
                    if match:
                        host = match.group(1)
                        port = int(match.group(2)) if match.group(2) else 7687
                        logger.info(f"Neo4jService: Probing {host}:{port} for availability...")
                        if not self._check_availability(host, port):
                            logger.warning(f"Neo4jService: Port {port} is closed on {host}. Falling back to MOCK mode.")
                            self._mode = "MOCK"
                            self._mock_checked = True
                            return None
                        logger.info(f"Neo4jService: Port {port} is OPEN on {host}. Proceeding LIVE.")
                except Exception as ex:
                    logger.error(f"Neo4jService: Availability probe error: {ex}")
                self._mock_checked = True

            try:
                from neo4j import GraphDatabase
                # Connection settings optimized for LAN
                self._driver = GraphDatabase.driver(
                    uri, 
                    auth=(user, password),
                    connection_timeout=5.0,
                    max_connection_lifetime=3600,
                    keep_alive=True
                )
                logger.info(f"Neo4jService: Driver ready for {uri}")
            except Exception as e:
                logger.error(f"Neo4jService: Driver init failed for {uri}: {str(e)}")
                self._mode = "MOCK"
        return self._driver

    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return results as a list of dicts."""
        if self._mode == "MOCK" or not self.driver:
            logger.warning("Neo4jService: Running in MOCK mode. Returning mock data.")
            return self._get_mock_query_results(query)
            
        try:
            with self._driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Neo4jService: Query execution failed: {str(e)}. Falling back to mock data.")
            return self._get_mock_query_results(query)

    def get_schema(self) -> Dict[str, Any]:
        """Fetch labels and relationship types for schema visualization."""
        if self._mode == "MOCK" or not self.driver:
            return self._get_mock_schema()
            
        try:
            nodes = self.execute_query("CALL db.labels() YIELD label RETURN label")
            rels = self.execute_query("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")
            
            # If we got nothing back from a "successful" query, still might want mock data for testing
            if not nodes and not rels:
                return self._get_mock_schema()

            return {
                "nodes": [n['label'] for n in nodes],
                "relationships": [r['relationshipType'] for r in rels]
            }
        except Exception as e:
            logger.error(f"Neo4jService: Schema fetch failed: {e}. Returning mock schema.")
            return self._get_mock_schema()

    def _get_mock_schema(self) -> Dict[str, Any]:
        """Hi-fidelity mock schema for development."""
        return {
            "nodes": ["Investor", "Agent", "Strategy", "Execution", "MarketData", "Metric"],
            "relationships": ["OWNS", "CONTROLS", "ANALYZES", "TRIGGERS", "LOGS"]
        }

    def _get_mock_query_results(self, query: str) -> List[Dict[str, Any]]:
        """Return sample nodes for common queries with Neo4j-style structure."""
        query_upper = query.upper()
        if "MATCH" in query_upper or "LIMIT" in query_upper:
            # High-fidelity mock nodes
            n1 = {"identity": 1, "labels": ["Agent"], "properties": {"name": "MasterDistiller_Agent", "type": "AGENT", "status": "ACTIVE"}}
            n2 = {"identity": 2, "labels": ["Strategy"], "properties": {"name": "Hedge_Strategy_v1", "type": "STRATEGY", "pnl": "+12.4%"}}
            n3 = {"identity": 3, "labels": ["MarketData"], "properties": {"name": "BTC_Price_Feed", "type": "MARKET_DATA", "value": "64231.50"}}
            n4 = {"identity": 4, "labels": ["Investor"], "properties": {"name": "Sovereign_OS_Root", "balance": "1.2M USD"}}
            
            # High-fidelity mock relationships
            r1 = {"identity": 101, "start": 4, "end": 1, "type": "CONTROLS", "properties": {}}
            r2 = {"identity": 102, "start": 1, "end": 2, "type": "EXECUTES", "properties": {}}
            r3 = {"identity": 103, "start": 2, "end": 3, "type": "ANALYZES", "properties": {}}

            return [
                {"n": n1, "r": r1},
                {"n": n2, "r": r2},
                {"n": n3, "r": r3},
                {"n": n4}
            ]
        return [{"message": "MOCK_MODE: Query execution bypassed. Neo4j is offline."}]

    def close(self):
        """Close the driver connection."""
        if self._driver:
            self._driver.close()
            logger.info("Neo4jService: Connection closed.")

# Global Singleton instance
neo4j_service = Neo4jService()

def get_neo4j() -> Neo4jService:
    return neo4j_service
