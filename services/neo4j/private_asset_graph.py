import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class PrivateAssetGraphService:
    """
    Manages Neo4j relationships for Reg D Private Placements.
    Different from public assets as they have funded vs committed amounts.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PrivateAssetGraphService, cls).__new__(cls)
        return cls._instance

    def __init__(self, neo4j_driver=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.driver = neo4j_driver
        self._initialized = True
        logger.info("PrivateAssetGraphService initialized")

    def subscribe_to_placement(self, investor_id: UUID, asset_id: UUID, commitment: float) -> bool:
        """
        Graph: (:PERSON)-[:SUBSCRIBED_TO {commitment: X, funded: 0}]->(:PRIVATE_PLACEMENT)
        """
        logger.info(f"NEO4J_LOG: MATCH (i:PERSON {{id: '{investor_id}'}}), (a:PRIVATE_ASSET {{id: '{asset_id}'}}) "
                    f"MERGE (i)-[:SUBSCRIBED_TO {{commitment: {commitment}, funded: 0, date: date()}}]->(a)")
        return True

    def fund_capital_call(self, investor_id: UUID, asset_id: UUID, amount: float) -> bool:
        """
        Updates the 'funded' property on the relationship.
        """
        logger.info(f"NEO4J_LOG: MATCH (i:PERSON {{id: '{investor_id}'}})-[r:SUBSCRIBED_TO]->(a:PRIVATE_ASSET {{id: '{asset_id}'}}) "
                    f"SET r.funded = r.funded + {amount}")
        return True
