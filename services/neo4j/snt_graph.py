
import logging
from typing import Dict, Any
from uuid import UUID
from neo4j import Driver

logger = logging.getLogger(__name__)

class SNTGraphService:
    """
    Manages Special Needs Trust (SNT) relationships in Neo4j.
    """
    
    def __init__(self, driver: Driver):
        self.driver = driver
        
    def flag_special_needs_beneficiary(
        self,
        person_id: str,
        is_special_needs: bool = True,
        receives_ssi: bool = True,
        receives_medicaid: bool = True
    ) -> bool:
        """
        Flags a person as special needs in the graph.
        """
        query = """
        MERGE (p:PERSON {id: $person_id})
        SET p.is_special_needs = $is_special_needs,
            p.receives_ssi = $receives_ssi,
            p.receives_medicaid = $receives_medicaid
        """
        try:
            with self.driver.session() as session:
                session.run(query, person_id=person_id, is_special_needs=is_special_needs, receives_ssi=receives_ssi, receives_medicaid=receives_medicaid)
            logger.info(f"Flagged person {person_id} as Special Needs in Neo4j")
            return True
        except Exception as e:
            logger.error(f"Failed to flag special needs person: {e}")
            return False

    def link_snt_to_beneficiary(self, trust_id: str, person_id: str) -> bool:
        """
        Links an SNT to its beneficiary.
        """
        query = """
        MATCH (t:TRUST {id: $trust_id})
        MATCH (p:PERSON {id: $person_id})
        MERGE (t)-[:BENEFITS {category: 'SPECIAL_NEEDS'}]->(p)
        SET t:SNT
        """
        try:
            with self.driver.session() as session:
                session.run(query, trust_id=trust_id, person_id=person_id)
            return True
        except Exception as e:
            logger.error(f"Failed to link SNT to beneficiary: {e}")
            return False
