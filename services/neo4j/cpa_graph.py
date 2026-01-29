import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CPAGraphService:
    """Manages CPA nodes and tax preparation links in Neo4j."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def create_cpa_node(self, cpa_id: str, name: str, firm: str):
        logger.info(f"NEO4J_LOG: MERGE (c:CPA {{id: '{cpa_id}', name: '{name}', firm: '{firm}'}})")

    def link_client_to_cpa(self, client_id: str, cpa_id: str, years: int):
        logger.info(f"NEO4J_LOG: MATCH (cl:CLIENT {{id: '{client_id}'}}), (c:CPA {{id: '{cpa_id}'}}) "
                    f"MERGE (cl)-[:TAX_PREPARED_BY {{years: {years}}}]->(c)")

    def link_cpa_to_advisor(self, cpa_id: str, advisor_id: str):
        logger.info(f"NEO4J_LOG: MATCH (c:CPA {{id: '{cpa_id}'}}), (a:PROFESSIONAL {{id: '{advisor_id}'}}) "
                    f"MERGE (c)-[:COORDINATES_WITH]->(a)")
