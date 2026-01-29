import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AttorneyGraphService:
    """Manages estate attorney nodes and collaboration links in Neo4j."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def create_attorney_node(self, atty_id: str, name: str, specializations: List[str]):
        logger.info(f"NEO4J_LOG: MERGE (a:ESTATE_ATTORNEY {{id: '{atty_id}', name: '{name}', specs: {specializations}}})")

    def link_client_to_attorney(self, client_id: str, atty_id: str, engagement: str):
        logger.info(f"NEO4J_LOG: MATCH (c:CLIENT {{id: '{client_id}'}}), (a:ESTATE_ATTORNEY {{id: '{atty_id}'}}) "
                    f"MERGE (c)-[:REPRESENTED_BY {{type: '{engagement}'}}]->(a)")

    def link_atty_to_advisor(self, atty_id: str, advisor_id: str):
        logger.info(f"NEO4J_LOG: MATCH (a:ESTATE_ATTORNEY {{id: '{atty_id}'}}), (adv:PROFESSIONAL {{id: '{advisor_id}'}}) "
                    f"MERGE (a)-[:COLLABORATES_WITH]->(adv)")
