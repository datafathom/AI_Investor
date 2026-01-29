import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RelationshipBuilder:
    """
    Manages relationships between graph nodes.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RelationshipBuilder, cls).__new__(cls)
        return cls._instance

    def __init__(self, driver=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.driver = driver
        logger.info("RelationshipBuilder initialized")

    def build_ownership_rel(self, owner_id: str, asset_id: str, quantity: float) -> Dict[str, Any]:
        """
        Creates an OWNS relationship.
        (:ENTITY)-[:OWNS {quantity: ...}]->(:ASSET)
        """
        rel = {
            "start_node": owner_id,
            "end_node": asset_id,
            "type": "OWNS",
            "properties": {
                "quantity": quantity
            }
        }
        logger.info(f"RelationshipBuilder: {owner_id} OWNS {asset_id}")
        return rel

    def build_correlation_rel(self, asset_a_id: str, asset_b_id: str, coefficient: float) -> Dict[str, Any]:
        """
         Creates a CORRELATED_WITH relationship.
         (:ASSET)-[:CORRELATED_WITH {coefficient: ...}]->(:ASSET)
        """
        rel = {
             "start_node": asset_a_id,
             "end_node": asset_b_id,
             "type": "CORRELATED_WITH",
             "properties": {
                 "coefficient": coefficient
             }
        }
        logger.info(f"RelationshipBuilder: {asset_a_id} CORRELATED_WITH {asset_b_id}")
        return rel
