
import logging
from typing import Dict, Any
from uuid import UUID
from neo4j import Driver

logger = logging.getLogger(__name__)

class CRTGraphService:
    """
    Manages CRT relationships in Neo4j.
    Links Grantors to Trusts and Charities.
    """
    
    def __init__(self, driver: Driver):
        self.driver = driver
        
    def create_crt_structure(
        self,
        grantor_id: str,
        trust_id: str,
        charity_id: str,
        trust_name: str,
        charity_name: str
    ) -> bool:
        """
        Creates the Grantor -> CRT -> Charity structure in Neo4j.
        """
        query = """
        MERGE (g:PERSON {id: $grantor_id})
        MERGE (c:CHARITY {id: $charity_id, name: $charity_name})
        MERGE (t:TRUST:CRT {id: $trust_id, name: $trust_name})
        
        MERGE (g)-[:ESTABLISHED]->(t)
        MERGE (t)-[:PAYS_INCOME]->(g)
        MERGE (t)-[:REMAINDER_TO]->(c)
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, 
                    grantor_id=grantor_id,
                    trust_id=trust_id,
                    charity_id=charity_id,
                    trust_name=trust_name,
                    charity_name=charity_name
                )
            logger.info(f"Successfully created CRT structure in Neo4j for trust {trust_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create CRT structure in Neo4j: {e}")
            return False
