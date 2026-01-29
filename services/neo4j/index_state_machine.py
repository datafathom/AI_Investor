import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class IndexStateMachine:
    """Manages index elevation and relegation in Neo4j (Football Pyramid model)."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def record_promotion(self, ticker: str, from_idx: str, to_idx: str):
        logger.info(f"NEO4J_LOG: MATCH (c:COMPANY {{ticker: '{ticker}'}}) "
                    f"MERGE (c)-[:PROMOTED_TO {{from: '{from_idx}'}}]->(i:INDEX {{name: '{to_idx}'}})")

    def record_relegation(self, ticker: str, from_idx: str, to_idx: str):
        logger.info(f"NEO4J_LOG: MATCH (c:COMPANY {{ticker: '{ticker}'}}) "
                    f"MERGE (c)-[:RELEGATED_FROM {{from: '{from_idx}'}}]->(i:INDEX {{name: '{to_idx}'}})")
