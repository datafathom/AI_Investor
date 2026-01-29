import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SpecializedREITGraph:
    """Manages specialized Property sub-nodes in Neo4j (Data Centers, Farmland)."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def add_data_center_node(self, ticker: str, mw_capacity: float, regions: List[str]):
        """
        Labels: REIT:DATA_CENTER
        """
        logger.info(f"NEO4J_LOG: MERGE (d:REIT:DATA_CENTER {{ticker: '{ticker}', capacity: {mw_capacity}, regions: {regions}}})")

    def add_farmland_node(self, ticker: str, total_acres: float, crops: List[str]):
        """
        Labels: REIT:FARMLAND
        """
        logger.info(f"NEO4J_LOG: MERGE (f:REIT:FARMLAND {{ticker: '{ticker}', acres: {total_acres}, crops: {crops}}})")
