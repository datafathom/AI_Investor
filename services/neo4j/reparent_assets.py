
import logging
from neo4j import Driver
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AssetReparenter:
    """
    Performs the graph transition of assets from an Individual to a Testamentary Trust.
    """
    
    def __init__(self, driver: Driver):
        self.driver = driver
        
    def execute_post_mortem_transition(self, deceased_person_id: str, trust_name: str) -> Dict[str, Any]:
        """
        Moves all assets owned by the individual to the new trust node.
        """
        query = """
        MATCH (u:PERSON {id: $person_id})
        MATCH (u)-[r:OWNS]->(a:ASSET)
        SET u.is_deceased = true
        
        MERGE (t:TRUST:TESTAMENTARY {name: $trust_name, owner_id: $person_id})
        CREATE (t)-[:OWNS]->(a)
        DELETE r
        RETURN count(a) as asset_count
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, person_id=deceased_person_id, trust_name=trust_name)
                count = result.single()["asset_count"]
                
                logger.info(f"Estate Transition: Moved {count} assets from {deceased_person_id} to {trust_name}")
                
                return {
                    "deceased_id": deceased_person_id,
                    "trust_created": trust_name,
                    "assets_transferred": count,
                    "status": "SUCCESS"
                }
        except Exception as e:
            logger.error(f"Asset re-parenting failed: {e}")
            return {"status": "ERROR", "error": str(e)}
