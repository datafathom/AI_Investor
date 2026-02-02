import os
import sys
import logging
from typing import Dict, List, Any
import psycopg2
from neo4j import GraphDatabase
from decimal import Decimal

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FullSystemAudit:
    """
    Phase 200.2: Comprehensive System Audit.
    Verifies integrity of Postgres Triggers and Neo4j Graph Topology.
    """
    
    def __init__(self):
        self.pg_conn_str = os.getenv("POSTGRES_CONNECTION_STRING", "postgresql://admin:password@localhost:5432/ai_investor")
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_pass = os.getenv("NEO4J_PASSWORD", "password")
        
    def audit_postgres_triggers(self) -> Dict[str, Any]:
        """
        Audit all Postgres triggers for potential cascade loops and coverage.
        """
        logger.info("Auditing Postgres Triggers...")
        issues = []
        trigger_count = 0
        
        try:
            with psycopg2.connect(self.pg_conn_str) as conn:
                with conn.cursor() as cur:
                    # List all triggers
                    query = """
                    SELECT event_object_table, trigger_name, action_statement
                    FROM information_schema.triggers
                    WHERE trigger_schema = 'public';
                    """
                    cur.execute(query)
                    triggers = cur.fetchall()
                    trigger_count = len(triggers)
                    
                    # Basic Heuristic: Check for potential circular logic (simplified)
                    # Real recursion check requires deep AST parsing, this is a metadata check
                    table_trigger_map = {}
                    for table, name, statement in triggers:
                        if table not in table_trigger_map:
                            table_trigger_map[table] = []
                        table_trigger_map[table].append(name)
                        
                    for table, t_list in table_trigger_map.items():
                        if len(t_list) > 5:
                            issues.append(f"High trigger density on table '{table}': {len(t_list)} triggers defined.")
                            
        except Exception as e:
            logger.error(f"Postgres Audit Failed: {e}")
            return {"status": "ERROR", "error": str(e)}
            
        return {
            "status": "PASS" if not issues else "WARNING",
            "total_triggers": trigger_count,
            "issues": issues
        }

    def audit_neo4j_integrity(self) -> Dict[str, Any]:
        """
        Audit Neo4j Graph for orphaned nodes and connectivity breaks.
        """
        logger.info("Auditing Neo4j Graph Integrity...")
        orphans = 0
        disconnected_clients = 0
        
        try:
            driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_pass))
            with driver.session() as session:
                # Check for orphaned nodes (nodes with no relationships)
                result = session.run("MATCH (n) WHERE NOT (n)--() RETURN count(n) as count")
                orphans = result.single()["count"]
                
                # Check for Clients without Portfolios (Data Integrity Gap)
                result = session.run("""
                MATCH (c:Client)
                WHERE NOT (c)-[:HAS_PLAN]->()-[:INCLUDES]->(:Portfolio)
                RETURN count(c) as count
                """)
                disconnected_clients = result.single()["count"]
                
            driver.close()
            
        except Exception as e:
            logger.error(f"Neo4j Audit Failed: {e}")
            return {"status": "ERROR", "error": str(e)}
            
        return {
            "status": "PASS" if (orphans == 0 and disconnected_clients == 0) else "WARNING",
            "orphaned_nodes": orphans,
            "disconnected_clients": disconnected_clients
        }

    def run_full_audit(self):
        """
        Execute all audit suites.
        """
        logger.info("Starting Full System Audit (Phase 200)...")
        
        pg_result = self.audit_postgres_triggers()
        neo_result = self.audit_neo4j_integrity()
        
        report = {
            "postgres": pg_result,
            "neo4j": neo_result,
            "overall_status": "OPERATIONAL" if pg_result["status"] != "ERROR" and neo_result["status"] != "ERROR" else "DEGRADED"
        }
        
        logger.info(f"Audit Complete. Status: {report['overall_status']}")
        return report

if __name__ == "__main__":
    audit = FullSystemAudit()
    report = audit.run_full_audit()
    print(report)
