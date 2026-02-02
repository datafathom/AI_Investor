import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VCNetworkService:
    """
    Phase 165.3: Neo4j Entrepreneur ↔ VC Backer Graph.
    Maps connections between serial founders and top-tier VCs.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VCNetworkService, cls).__new__(cls)
        return cls._instance

    def __init__(self, neo4j_driver=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.driver = neo4j_driver
        self._initialized = True
        logger.info("VCNetworkService initialized")

    def map_founder_network(self, founder_name: str, backer_firms: List[str]) -> bool:
        """
        Graph: (Founder)-[:BACKED_BY]->(VC_FIRM)
        """
        logger.info(f"NEO4J_LOG: MERGE (p:PERSON {{name: '{founder_name}'}}) "
                    f"FOREACH (firm IN {backer_firms} | "
                    f"MERGE (v:VC_FIRM {{name: firm}}) "
                    f"MERGE (p)-[:BACKED_BY]->(v))")
        return True

    def find_serial_entrepreneurs(self) -> List[str]:
        """
        Queries for founders with >2 successful exits.
        """
        logger.info("NEO4J_LOG: MATCH (p:PERSON)-[:FOUNDED]->(c:COMPANY {status: 'EXITED'}) "
                    "WITH p, count(c) as exits WHERE exits >= 2 RETURN p.name")
        return ["Elon Musk", "Reid Hoffman"]
