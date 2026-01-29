import logging
import uuid
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class NodeFactory:
    """
    Creates standardized graph nodes.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NodeFactory, cls).__new__(cls)
        return cls._instance

    def __init__(self, driver=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.driver = driver
        logger.info("NodeFactory initialized")

    def create_asset_node(self, symbol: str, asset_type: str, props: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Prepares properties for an ASSET node.
        In a real app, this might execute the CYPHER to create it.
        Here we return the dict for verification/mocking.
        """
        node_id = str(uuid.uuid4())
        properties = {
            "id": node_id,
            "label": "ASSET",
            "symbol": symbol,
            "type": asset_type,
            "created_at": "now()" # Placeholder for timestamp
        }
        if props:
            properties.update(props)
            
        logger.info(f"NodeFactory: Prepared ASSET node for {symbol}")
        return properties

    def create_agent_node(self, name: str, persona: str) -> Dict[str, Any]:
        """Prepares properties for an AGENT node."""
        node_id = str(uuid.uuid4())
        properties = {
            "id": node_id,
            "label": "AGENT",
            "name": name,
            "persona": persona,
            "active": True
        }
        logger.info(f"NodeFactory: Prepared AGENT node for {name}")
        return properties
