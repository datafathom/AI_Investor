import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CustodianGraphService:
    """Manages custodian nodes and account verification links in Neo4j."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def create_custodian_node(self, custodian_id: str, name: str, is_sip_fdic: bool):
        logger.info(f"NEO4J_LOG: MERGE (c:CUSTODIAN {{id: '{custodian_id}', name: '{name}', sipc_member: {is_sip_fdic}}})")

    def link_account_to_custodian(self, account_id: str, custodian_id: str, verified: bool):
        logger.info(f"NEO4J_LOG: MATCH (a:ACCOUNT {{id: '{account_id}'}}), (c:CUSTODIAN {{id: '{custodian_id}'}}) "
                    f"MERGE (a)-[:HELD_AT {{is_verified: {verified}}}]->(c)")

    def flag_custody_anomaly(self, advisor_id: str, account_id: str):
        """Flags when an advisor has direct withdrawal authority where they shouldn't."""
        logger.warning(f"NEO4J_LOG: ALERT! Potential direct custody detected for advisor {advisor_id} on {account_id}")
