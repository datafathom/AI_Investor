import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AssetClassGraphService:
    """Manages non-correlated asset class nodes and correlation links in Neo4j."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def create_asset_class_node(self, label: str, name: str, ticker: str, corr_to_spy: float):
        """
        label: COMMODITY, FIXED_INCOME, REAL_ESTATE
        """
        logger.info(f"NEO4J_LOG: MERGE (a:ASSET_CLASS:{label} {{name: '{name}', ticker: '{ticker}', spy_corr: {corr_to_spy}}})")

    def link_non_correlated_assets(self, ticker_a: str, ticker_b: str, coefficient: float):
        logger.info(f"NEO4J_LOG: MATCH (a {{ticker: '{ticker_a}'}}), (b {{ticker: '{ticker_b}'}}) "
                    f"MERGE (a)-[:NEGATIVELY_CORRELATED_WITH {{coefficient: {coefficient}}}]->(b)")
