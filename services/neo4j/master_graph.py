import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MasterGraph:
    """
    The Central Brain.
    Merges disjointed domain graphs (Tax, Equity, Estate, Risk) into a single
    Unified Knowledge Graph.
    
    Enables queries like: 
    "Show me all assets in the 'Family Trust' that are exposed to 'Geopolitical Risk' 
    and have 'Unrealized Losses' > $1M."
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MasterGraph, cls).__new__(cls)
        return cls._instance

    def __init__(self, neo4j_driver=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        from services.neo4j.neo4j_service import neo4j_service
        self.neo4j = neo4j_service
        self.driver = neo4j_driver or self.neo4j.driver
        logger.info("MasterGraph initialized (The Brain is Online)")

    def get_node_count(self) -> int:
        """
        Returns the total number of nodes in the graph.
        """
        query = "MATCH (n) RETURN count(n) as count"
        try:
            results = self.neo4j.execute_query(query)
            return results[0]['count'] if results else 0
        except Exception as e:
            logger.error(f"Failed to get node count: {e}")
            return 0

    def unify_graphs(self):
        """
        Runs the Master Merge Query to link all isolated nodes.
        conceptually: MATCH (c:Client), (p:Portfolio) WHERE c.id = p.owner_id MERGE (c)-[:OWNS]->(p)
        """
        logger.info("MasterGraph: Executing Global Schema Unification...")
        query = """
        MATCH (c:Client), (p:Portfolio) 
        WHERE c.id = p.owner_id 
        MERGE (c)-[:OWNS]->(p)
        """
        self.neo4j.execute_query(query)
        return True

    def trigger_reflexivity_shock(self, asset_id: str, magnitude: float) -> Dict[str, Any]:
        """
        Traverse Neo4j links to identify affected Nodes (Trusts, Property, Entities).
        Calculates "Contagion Velocity" and propagation paths.
        """
        logger.info(f"MasterGraph: Triggering shock on {asset_id} with magnitude {magnitude}")
        
        # Cypher query to find propagation paths via refined relationships
        query = """
        MATCH path = (asset {id: $asset_id})-[r:OWNS|BENEFICIARY_OF|EXPOSED_TO*1..3]->(affected)
        RETURN affected, path, [rel IN r | rel.weight] as weights
        """
        
        try:
            results = self.neo4j.execute_query(query, {"asset_id": asset_id})
            
            affected_nodes = []
            propagation_paths = []
            
            if not results:
                logger.warning(f"MasterGraph: No downstream nodes affected by shock on {asset_id}")
                return {
                    "asset_id": asset_id,
                    "magnitude": magnitude,
                    "affected_nodes": [],
                    "contagion_velocity": 0.0,
                    "propagation_paths": []
                }

            for record in results:
                node = record['affected']
                node_id = node.get('id') or str(node.id)
                if node_id not in [n['id'] for n in affected_nodes]:
                    affected_nodes.append({
                        "id": node_id,
                        "group": list(node.labels)[0].lower() if node.labels else "unknown",
                        "impact": magnitude * 0.8 # Attenuation factor
                    })
                
                path_nodes = [n.get('id') or str(n.id) for n in record['path'].nodes]
                propagation_paths.append(path_nodes)
            
            # Contagion velocity is proportional to the branching factor
            contagion_velocity = min(1.0, len(affected_nodes) * 0.12)
            
            return {
                "asset_id": asset_id,
                "magnitude": magnitude,
                "affected_nodes": affected_nodes,
                "contagion_velocity": round(contagion_velocity, 2),
                "propagation_paths": propagation_paths
            }
            
        except Exception as e:
            logger.error(f"Failed to trigger reflexivity shock: {str(e)}")
            raise

    def query_global_exposure(self, risk_factor: str) -> List[Dict[str, Any]]:
        """
        Finds every dollar exposed to a specific risk across ALL entities.
        """
        logger.info(f"MasterGraph: Scanning super-graph for '{risk_factor}' exposure...")
        
        query = """
        MATCH (risk:Risk {name: $risk_factor})<-[:EXPOSED_TO]-(asset:Asset)<-[:OWNS]-(owner)
        RETURN owner.name as entity, asset.name as asset, asset.value as exposure
        """
        
        try:
            results = self.neo4j.execute_query(query, {"risk_factor": risk_factor})
            return [{"entity": r["entity"], "asset": r["asset"], "exposure": r["exposure"]} for r in results]
        except Exception as e:
            logger.error(f"Failed to query global exposure: {e}")
            return []

    def get_search_entities(self) -> List[Dict[str, Any]]:
        """
        Returns a list of searchable entities (Clients, Agents, Symbols) from the graph.
        """
        query = """
        MATCH (n) 
        WHERE n:Client OR n:AGENT OR n:Portfolio OR n:Asset
        RETURN n.id as id, 
               COALESCE(n.name, n.id) as label, 
               labels(n)[0] as group,
               CASE 
                 WHEN n:Client THEN 'client'
                 WHEN n:AGENT THEN 'agent'
                 WHEN n:Portfolio THEN 'portfolio'
                 ELSE 'ticker'
               END as type
        LIMIT 500
        """
        try:
            return self.neo4j.execute_query(query)
        except Exception as e:
            logger.error(f"MasterGraph: Failed to fetch search entities: {e}")
            return []

    def get_graph_data(self) -> Dict[str, Any]:
        """
        Extracts the full Neo4j graph structure formatted for D3.js Force Graphs.
        """
        query = "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 250"
        
        try:
            result = self.neo4j.execute_query(query)
            nodes = {}
            links = []
            
            for record in result:
                n = record['n']
                m = record['m']
                r = record['r']
                
                for node in [n, m]:
                    node_id = node.get('id') or str(node.id)
                    if node_id not in nodes:
                        label = list(node.labels)[0] if node.labels else "unknown"
                        nodes[node_id] = {
                            "id": node_id,
                            "group": label.lower(),
                            "val": node.get('importance', 10)
                        }
                
                links.append({
                    "source": n.get('id') or str(n.id),
                    "target": m.get('id') or str(m.id),
                    "type": r.type
                })
            
            return {"nodes": list(nodes.values()), "links": links}
        except Exception as e:
            logger.error(f"MasterGraph: Error fetching live graph: {e}")
            # Final fallback: Return empty graph rather than hardcoded mock
            return {"nodes": [], "links": []}
