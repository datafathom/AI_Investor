import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AdvisorGraphService:
    """Manages advisor nodes and relationships in Neo4j."""
    
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver

    def create_advisor_node(self, advisor_id: str, name: str, types: List[str], fiduciary: bool):
        """
        Creates specialized advisor nodes in Neo4j.
        types: WEALTH_MANAGER, ASSET_MANAGER, FINANCIAL_PLANNER, PRIVATE_BANKER
        """
        labels = ":".join(["ADVISOR"] + types)
        query = f"MERGE (a:{labels} {{id: $id}}) SET a.name = $name, a.fiduciary = $fiduciary, a.updated_at = datetime()"
        parameters = {"id": advisor_id, "name": name, "fiduciary": fiduciary}
        
        logger.info(f"AdvisorGraph: Creating advisor node {advisor_id}")
        self.driver.execute_query(query, parameters)

    def link_advisor_to_firm(self, advisor_id: str, firm_id: str):
        """Links an advisor to a firm (Employment relationship)."""
        query = """
        MATCH (a:ADVISOR {id: $advisor_id}), (f:FIRM {id: $firm_id})
        MERGE (a)-[r:EMPLOYED_BY]->(f)
        SET r.updated_at = datetime()
        """
        parameters = {"advisor_id": advisor_id, "firm_id": firm_id}
        
        logger.info(f"AdvisorGraph: Linking advisor {advisor_id} to firm {firm_id}")
        self.driver.execute_query(query, parameters)

    def recommend_product(self, advisor_id: str, product_id: str, commission: float):
        """Links an advisor to a recommended product."""
        query = """
        MATCH (a:ADVISOR {id: $advisor_id}), (p:PRODUCT {id: $product_id})
        MERGE (a)-[r:RECOMMENDS]->(p)
        SET r.commission = $commission, r.updated_at = datetime()
        """
        parameters = {"advisor_id": advisor_id, "product_id": product_id, "commission": commission}
        
        logger.info(f"AdvisorGraph: Linking advisor {advisor_id} to product {product_id}")
        self.driver.execute_query(query, parameters)
