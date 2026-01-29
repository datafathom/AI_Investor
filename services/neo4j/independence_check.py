
import logging
from neo4j import Driver
from typing import Dict, Any

logger = logging.getLogger(__name__)

class IndependenceCheck:
    """
    Verifies the independence of a Trustee from a Grantor in Neo4j.
    Required for valid Asset Protection Trusts in most jurisdictions.
    """
    
    def __init__(self, driver: Driver):
        self.driver = driver
        
    def verify_trustee_independence(self, grantor_id: str, trustee_id: str) -> Dict[str, Any]:
        """
        Checks for 'FAMILY' or 'EMPLOYEE' relationships in the graph.
        """
        query = """
        MATCH (g:PERSON {id: $grantor_id})
        MATCH (t:PERSON {id: $trustee_id})
        OPTIONAL MATCH (g)-[r]-(t)
        RETURN r.type as relationship_type
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, grantor_id=grantor_id, trustee_id=trustee_id)
                record = result.single()
                
                rel_type = record["relationship_type"] if record else None
                
                is_independent = rel_type not in ["FAMILY", "SPOUSE", "CHILD", "EMPLOYEE", "SUBORDINATE"]
                
                logger.info(f"Independence Check: Grantor={grantor_id}, Trustee={trustee_id}, Rel={rel_type}, Result={is_independent}")
                
                return {
                    "is_independent": is_independent,
                    "relationship_detected": rel_type,
                    "status": "VALID" if is_independent else "INVALID_FOR_APT"
                }
        except Exception as e:
            logger.error(f"Independence check failed: {e}")
            return {"is_independent": False, "error": str(e)}
