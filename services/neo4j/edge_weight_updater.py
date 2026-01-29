"""
Neo4j Edge Weight Updater Service.
Updates correlation edges in the graph database.
"""
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class EdgeWeightUpdater:
    """
    Service to update correlation edge weights in the Neo4j financial graph.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EdgeWeightUpdater, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the EdgeWeightUpdater with connection details."""
        if getattr(self, 'initialized', False):
            return
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.auth = (
            os.getenv('NEO4J_USER', 'neo4j'),
            os.getenv('NEO4J_PASSWORD', 'investor_password')
        )
        self._driver = None
        self.initialized = True

    @property
    def driver(self):
        """Lazy-loaded Neo4j driver."""
        if self._driver is None:
            from neo4j import GraphDatabase
            self._driver = GraphDatabase.driver(self.uri, auth=self.auth)
        return self._driver

    def update_correlation(
        self,
        symbol1: str,
        symbol2: str,
        coefficient: float,
        confidence: float,
        timeframe: str = "1D"
    ):
        """
        Update the CORRELATED_WITH edge weight in Neo4j.
        
        Args:
            symbol1: Source asset symbol.
            symbol2: Target asset symbol.
            coefficient: Pearson correlation coefficient.
            confidence: Statistical confidence level.
            timeframe: Analysis timeframe.
        """
        direction = self._get_direction(coefficient)

        query = """
        MATCH (a1:Asset {symbol: $symbol1})
        MATCH (a2:Asset {symbol: $symbol2})
        MERGE (a1)-[r:CORRELATED_WITH {timeframe: $timeframe}]->(a2)
        SET r.coefficient = $coefficient,
            r.confidence = $confidence,
            r.direction = $direction,
            r.updated_at = datetime()
        RETURN r
        """

        params = {
            "symbol1": symbol1,
            "symbol2": symbol2,
            "coefficient": float(coefficient),
            "confidence": float(confidence),
            "direction": direction,
            "timeframe": timeframe
        }

        try:
            with self.driver.session() as session:
                session.run(query, params)
        except Exception as e:
            logger.error("Failed to update Neo4j correlation: %s", str(e))

    def _get_direction(self, coefficient: float) -> str:
        """Categorize correlation direction."""
        if coefficient > 0.3:
            return "POSITIVE"
        if coefficient < -0.3:
            return "NEGATIVE"
        return "NEUTRAL"

    def close(self):
        """Close the Neo4j driver connection."""
        if self._driver:
            self._driver.close()
            self._driver = None

# Global Singleton
edge_weight_updater = EdgeWeightUpdater()
