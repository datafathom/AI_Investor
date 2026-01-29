
import logging
from typing import Dict, Any, List
from neo4j import Driver

logger = logging.getLogger(__name__)

class EthicsFirewallGraph:
    """
    Neo4j implementation of an Ethics Firewall.
    Detects and prevents communication or information paths between 
    Beneficiaries (Executives) and Trustees (Traders).
    """
    
    def __init__(self, driver: Driver):
        self.driver = driver
        
    def check_firewall_integrity(self, beneficiary_id: str, trustee_id: str) -> Dict[str, Any]:
        """
        Queries the graph for any paths (COMMUNICATED_WITH, RELATED_TO) between 
        the restricted parties.
        """
        query = """
        MATCH (b:BENEFICIARY {id: $beneficiary_id})
        MATCH (t:TRUSTEE {id: $trustee_id})
        MATCH p = shortestPath((b)-[*..3]-(t))
        RETURN p
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, beneficiary_id=beneficiary_id, trustee_id=trustee_id)
                path = result.single()
                
                if path:
                    logger.warning(f"FIREWALL BREACH DETECTED: Path found between {beneficiary_id} and {trustee_id}")
                    return {
                        "integrity": "BREACHED",
                        "path_length": len(path['p']),
                        "alert": "Insider information risk detected."
                    }
                
                return {
                    "integrity": "SECURE",
                    "message": "No direct or indirect communication paths found."
                }
        except Exception as e:
            logger.error(f"Firewall graph query failed: {e}")
            return {"integrity": "ERROR", "error": str(e)}

    def setup_firewall_nodes(self, person_id: str, role: str):
        """
        Assigns roles for firewall monitoring.
        """
        query = f"MATCH (p:PERSON {{id: $person_id}}) SET p:{role}"
        with self.driver.session() as session:
            session.run(query, person_id=person_id)
            logger.info(f"Node {person_id} assigned role {role}")
