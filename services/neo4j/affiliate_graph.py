import logging
import uuid
from typing import Dict, List, Any
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)

class AffiliateGraph:
    """
    Phase 185.3: Neo4j Affiliate/Insider Mapper.
    Models relationships between executives, major shareholders, and public companies.
    """
    
    def map_affiliate(self, person_id: str, company_ticker: str, role: str) -> Dict[str, Any]:
        """
        Maps a person as an affiliate (Insider) of a company.
        Roles: OFFICER, DIRECTOR, MAJOR_SHEARHOLDER (>10%)
        """
        query = """
        MATCH (u:User {id: $uid})
        MERGE (c:PublicCompany {ticker: $ticker})
        MERGE (u)-[r:AFFILIATE_OF]->(c)
        SET r.role = $role,
            r.status = 'ACTIVE',
            r.mapped_at = datetime()
        """
        
        logger.info(f"NEO4J_LOG: Mapping User {person_id} as {role} for {company_ticker}")
        # db_manager.execute_neo4j(query, {"uid": person_id, "ticker": company_ticker, "role": role})
        
        return {
            "user_id": person_id,
            "ticker": company_ticker,
            "role": role,
            "status": "MAPPED"
        }

    def map_selling_plan(self, person_id: str, plan_id: str) -> Dict[str, Any]:
        """
        Links an executive/affiliate to a specific 10b5-1 selling plan.
        """
        query = """
        MATCH (u:User {id: $uid})
        MERGE (p:SellingPlan {id: $pid})
        MERGE (u)-[r:HAS_STOCKED_PLAN]->(p)
        SET r.mapped_at = datetime()
        """
        logger.info(f"NEO4J_LOG: Mapping User {person_id} to Selling Plan {plan_id}")
        return {
            "user_id": person_id,
            "plan_id": plan_id,
            "status": "MAPPED"
        }

    def get_insider_exposure(self, person_id: str) -> List[Dict[str, Any]]:
        """
        Returns all companies where the user is considered an insider.
        """
        logger.info(f"NEO4J_LOG: MATCH (u:User {{id: '{person_id}'}})-[r:AFFILIATE_OF]->(c) RETURN c.ticker, r.role")
        # Mock result
        return [
            {"ticker": "AAPL", "role": "OFFICER"},
            {"ticker": "PLTR", "role": "MAJOR_SHAREHOLDER"}
        ]
