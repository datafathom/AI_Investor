import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class AccreditationGraphService:
    """
    Manages Neo4j accreditation status for alternative investments.
    SEC rules often require Accredited or Qualified Purchaser status for carry fees.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AccreditationGraphService, cls).__new__(cls)
        return cls._instance

    def __init__(self, neo4j_driver=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.driver = neo4j_driver
        self._initialized = True
        logger.info("AccreditationGraphService initialized")

    def flag_accreditation_status(self, user_id: UUID, level: str) -> bool:
        """
        Graph: (:PERSON)-[:HAS_STATUS]->(:ACCREDITATION {level: 'QP'})
        """
        logger.info(f"NEO4J_LOG: MATCH (p:PERSON {{id: '{user_id}'}}) "
                    f"MERGE (s:ACCREDITATION {{level: '{level}', verified_date: date()}}) "
                    f"MERGE (p)-[:HAS_QUALIFICATION]->(s)")
        return True
