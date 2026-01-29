
import logging
from neo4j import Driver
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PropertyChainGraph:
    """
    Tracks real estate exchange chains in Neo4j to preserve tax basis history.
    """
    
    def __init__(self, driver: Driver):
        self.driver = driver
        
    def link_exchange(
        self, 
        old_property_id: str, 
        new_property_id: str, 
        deferred_gain: float,
        basis_carried: float
    ) -> bool:
        """
        Creates an EXCHANGED_INTO relationship.
        """
        query = """
        MERGE (p1:PROPERTY {id: $old_id})
        MERGE (p2:PROPERTY {id: $new_id})
        CREATE (p1)-[r:EXCHANGED_INTO {
            deferred_gain: $gain,
            basis_at_exchange: $basis,
            date: date()
        }]->(p2)
        SET p2.original_basis = $basis
        """
        try:
            with self.driver.session() as session:
                session.run(query, old_id=old_property_id, new_id=new_property_id, gain=deferred_gain, basis=basis_carried)
            logger.info(f"Neo4j: Linked {old_property_id} -> {new_property_id} via 1031 Exchange")
            return True
        except Exception as e:
            logger.error(f"Failed to link property chain: {e}")
            return False
