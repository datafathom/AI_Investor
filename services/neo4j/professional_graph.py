import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ProfessionalGraphService:
    """Manages professional nodes and advisor-client relationships in Neo4j."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def create_professional_node(self, prof_id: str, name: str, types: List[str], fiduciary: bool):
        labels = ":".join(["PROFESSIONAL"] + types)
        logger.info(f"NEO4J_LOG: MERGE (p:{labels} {{id: '{prof_id}', name: '{name}', fiduciary: {fiduciary}}})")

    def link_advisor_to_client(self, advisor_id: str, client_id: str, fee_pct: float):
        logger.info(f"NEO4J_LOG: MATCH (a:PROFESSIONAL {{id: '{advisor_id}'}}), (c:CLIENT {{id: '{client_id}'}}) "
                    f"MERGE (a)-[:ADVISES {{fee_pct: {fee_pct}}}]->(c)")

    def flag_conflict(self, advisor_id: str, other_id: str, reason: str):
        logger.info(f"NEO4J_LOG: MATCH (a:PROFESSIONAL {{id: '{advisor_id}'}}), (b:PROFESSIONAL {{id: '{other_id}'}}) "
                    f"MERGE (a)-[:CONFLICTS_WITH {{reason: '{reason}'}}]->(b)")
