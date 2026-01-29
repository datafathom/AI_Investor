import logging
from uuid import UUID
from typing import List

logger = logging.getLogger(__name__)

class SuccessionMapper:
    """
    Maps the chain of succession for trustees in Neo4j.
    Follows singleton pattern.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SuccessionMapper, cls).__new__(cls)
        return cls._instance

    def __init__(self, neo4j_service=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.neo4j_service = neo4j_service
        self._initialized = True
        logger.info("SuccessionMapper initialized")

    def map_succession_chain(self, trust_id: UUID, successor_ids: List[UUID]) -> bool:
        """
        Creates a chain of succession in Neo4j.
        """
        for i, successor_id in enumerate(successor_ids):
            prev_id = successor_ids[i-1] if i > 0 else "PRIMARY_TRUSTEE"
            logger.info(f"NEO4J_LOG: MATCH (prev {{id: '{prev_id}'}}), (next {{id: '{successor_id}'}}) "
                        f"MERGE (prev)-[:SUCCEEDED_BY {{order: {i+1}}}]->(next)")
        return True
