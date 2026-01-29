import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SectorIndexGraphService:
    """Manages index fund holdings and sector allocations in Neo4j."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def create_fund_node(self, fund_id: str, ticker: str, name: str):
        logger.info(f"NEO4J_LOG: MERGE (f:INDEX_FUND {{id: '{fund_id}', ticker: '{ticker}', name: '{name}'}})")

    def link_fund_to_sector(self, fund_ticker: str, sector_name: str, weight: float):
        """Creates relationship: (:INDEX_FUND)-[:ALLOCATES_TO {weight}]->(:SECTOR)"""
        logger.info(f"NEO4J_LOG: MATCH (f:INDEX_FUND {{ticker: '{fund_ticker}'}}), (s:SECTOR {{name: '{sector_name}'}}) "
                    f"MERGE (f)-[:ALLOCATES_TO {{weight: {weight}}}]->(s)")

    def get_market_exposure(self, ticker: str) -> List[Dict[str, Any]]:
        """Finds all index funds that hold a high percentage of this sector/asset."""
        # Mock results
        return [{"fund": "XLK", "exposure": 0.22}, {"fund": "QQQ", "exposure": 0.15}]
