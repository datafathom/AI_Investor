import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class REITGraphService:
    """Manages REIT nodes and property-type relationships in Neo4j."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def create_reit_node(self, ticker: str, name: str, prop_type: str, div_yield: float):
        """
        Label: REIT
        Adds specific property type label dynamically.
        """
        label = prop_type.upper()
        logger.info(f"NEO4J_LOG: MERGE (r:REIT:{label} {{ticker: '{ticker}', name: '{name}', yield: {div_yield}}})")

    def link_portfolio_to_reit(self, portfolio_id: str, ticker: str, weight: float):
        logger.info(f"NEO4J_LOG: MATCH (p:PORTFOLIO {{id: '{portfolio_id}'}}), (r:REIT {{ticker: '{ticker}'}}) "
                    f"MERGE (p)-[:HOLDS_REIT {{weight: {weight}}}]->(r)")
