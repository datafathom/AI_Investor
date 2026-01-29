"""
Neo4j integrity Checker.
Validates the consistency of the financial knowledge graph.
"""
import logging
from typing import Dict, Any, List
from services.neo4j.edge_weight_updater import edge_weight_updater

logger = logging.getLogger(__name__)

class Neo4jIntegrityChecker:
    """
    Performs routine audits on the graph to detect orphan nodes or invalid weights.
    """

    @staticmethod
    def audit_correlations() -> Dict[str, Any]:
        """
        Check for invalid correlation coefficients (outside -1.0 to 1.0)
        and orphan correlation edges.
        """
        queries = {
            'out_of_bounds': "MATCH ()-[r:CORRELATED_WITH]->() WHERE r.coefficient > 1.0 OR r.coefficient < -1.0 RETURN count(r) as count",
            'orphan_edges': "MATCH (a1)-[r:CORRELATED_WITH]->(a2) WHERE NOT (a1:Asset) OR NOT (a2:Asset) RETURN count(r) as count",
            'total_correlations': "MATCH ()-[r:CORRELATED_WITH]->() RETURN count(r) as count"
        }
        
        results = {}
        try:
            with edge_weight_updater.driver.session() as session:
                for key, query in queries.items():
                    res = session.run(query)
                    record = res.single()
                    results[key] = record['count'] if record else 0
                    
            status = 'CRITICAL' if (results['out_of_bounds'] > 0 or results['orphan_edges'] > 0) else 'HEALTHY'
            
            return {
                'status': status,
                'metrics': results
            }
        except Exception as e:
            logger.error("Neo4j Audit failed: %s", str(e))
            return {'status': 'FAILED', 'error': str(e)}
