
import logging
from neo4j import Driver
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FrictionGraphService:
    """
    Detects competing interests in assets using Neo4j.
    """
    
    def __init__(self, driver: Driver):
        self.driver = driver
        
    def detect_friction_points(self, estate_id: str) -> Dict[str, Any]:
        """
        Queries for heirs with conflicting 'DESIRES' on the same asset.
        """
        query = """
        MATCH (p1:HEIR)-[d1:DESIRES]->(a:ASSET)<-[d2:DESIRES]-(p2:HEIR)
        WHERE d1.action <> d2.action
        RETURN a.name as asset_name, p1.name as heir_a, p2.name as heir_b, d1.action as action_a, d2.action as action_b
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query)
                conflicts = []
                for record in result:
                    conflicts.append({
                        "asset": record["asset_name"],
                        "parties": [record["heir_a"], record["heir_b"]],
                        "conflict": f"{record['action_a']} vs {record['action_b']}"
                    })
                
                logger.info(f"Friction Graph: Detected {len(conflicts)} conflict points.")
                return {"conflicts": conflicts, "conflict_count": len(conflicts)}
        except Exception as e:
            logger.error(f"Friction graph query failed: {e}")
            return {"error": str(e)}
