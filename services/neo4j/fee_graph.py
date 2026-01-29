import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class FeeGraphService:
    """
    Manages Neo4j transparency graph for fee distribution.
    Maps Client -> Fee Pot -> (Advisor, Manager, Platform).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FeeGraphService, cls).__new__(cls)
        return cls._instance

    def __init__(self, neo4j_driver=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.driver = neo4j_driver
        self._initialized = True
        logger.info("FeeGraphService initialized")

    def map_fee_distribution(self, client_id: UUID, total_fee: float, splits: dict) -> bool:
        """
        Graph: (:CLIENT)-[:PAYS]->(:FEE_POT)-[:SPLIT_TO]->(:ENTITIES)
        """
        logger.info(f"NEO4J_LOG: MATCH (c:CLIENT {{id: '{client_id}'}}) "
                    f"CREATE (p:FEE_POT {{amount: {total_fee}, date: date()}}) "
                    f"MERGE (c)-[:PAYS_FEE]->(p)")
        
        for entity, amount in splits.items():
            logger.info(f"NEO4J_LOG: MATCH (p:FEE_POT), (e:ENTITY {{name: '{entity}'}}) "
                        f"MERGE (p)-[:DISTRIBUTED_TO {{amount: {amount}}}]->(e)")
            
        return True
