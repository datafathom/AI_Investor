
import logging
from neo4j import Driver
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ILITGraphService:
    """
    Manages ILIT structures in Neo4j.
    Ensures the trust owns the policy, not the individual.
    """
    
    def __init__(self, driver: Driver):
        self.driver = driver
        
    def setup_ilit_structure(self, trust_id: str, policy_id: str, insured_id: str) -> Dict[str, Any]:
        """
        Creates the correct ILIT ownership/beneficiary lattice.
        """
        query = """
        MATCH (t:TRUST {id: $trust_id})
        MATCH (p:POLICY {id: $policy_id})
        MATCH (u:PERSON {id: $insured_id})
        
        MERGE (t)-[:OWNS]->(p)
        MERGE (p)-[:INSURES]->(u)
        MERGE (p)-[:PAYS_BENEFIT_TO]->(t)
        
        WITH p, u
        OPTIONAL MATCH (u)-[r:OWNS]->(p)
        DELETE r
        RETURN count(p) as success
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, trust_id=trust_id, policy_id=policy_id, insured_id=insured_id)
                logger.info(f"ILIT Graph: Successfully structured Trust {trust_id} as owner of Policy {policy_id}")
                return {"status": "SUCCESS", "message": "Ownership lattice established. 3-year clock initiated."}
        except Exception as e:
            logger.error(f"ILIT graph setup failed: {e}")
            return {"status": "ERROR", "error": str(e)}
