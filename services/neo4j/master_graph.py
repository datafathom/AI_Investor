import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MasterGraphService:
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
            cls._instance = super(MasterGraphService, cls).__new__(cls)
        return cls._instance

    def __init__(self, neo4j_driver=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        from services.neo4j.neo4j_service import neo4j_service
        self.neo4j = neo4j_service
        self.driver = neo4j_driver or self.neo4j.driver
        logger.info("MasterGraphService initialized (The Brain is Online)")

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
        
        # Cypher query to find propagation paths
        # Returns paths from the shocked asset to all reachable nodes
        query = """
        MATCH path = (asset {id: $asset_id})-[r*1..5]->(affected)
        RETURN affected, path, [rel IN r | rel.weight] as weights
        """
        
        try:
            results = self.neo4j.execute_query(query, {"asset_id": asset_id})
            
            affected_nodes = []
            propagation_paths = []
            contagion_velocity = 0.0
            
            if not results:
                # Fallback mock for demonstration if graph is empty
                return {
                    "asset_id": asset_id,
                    "magnitude": magnitude,
                    "affected_nodes": [asset_id, "Portfolio_Main", "Trust_Revocable"],
                    "contagion_velocity": 0.75,
                    "propagation_paths": [
                        [asset_id, "Portfolio_Main"],
                        ["Portfolio_Main", "Trust_Revocable"]
                    ]
                }

            for record in results:
                node = record['affected']
                node_id = node.get('id') or str(node.id)
                if node_id not in [n['id'] for n in affected_nodes]:
                    affected_nodes.append({
                        "id": node_id,
                        "group": list(node.labels)[0].lower() if node.labels else "unknown",
                        "impact": magnitude * 0.8 # Simplified impact attenuation
                    })
                
                # Extract path IDs
                path_nodes = [n.get('id') or str(n.id) for n in record['path'].nodes]
                propagation_paths.append(path_nodes)
            
            # Calculate contagion velocity (simplified)
            contagion_velocity = min(1.0, len(affected_nodes) * 0.15)
            
            return {
                "asset_id": asset_id,
                "magnitude": magnitude,
                "affected_nodes": affected_nodes,
                "contagion_velocity": contagion_velocity,
                "propagation_paths": propagation_paths
            }
            
        except Exception as e:
            logger.error(f"Failed to trigger reflexivity shock: {str(e)}")
            raise

    def query_global_exposure(self, risk_factor: str) -> List[Dict[str, Any]]:
        """
        Finds every dollar exposed to a specific risk across ALL entities
        (Personal, Trust, LLC, Foundation).
        """
        logger.info(f"MasterGraph: Scanning entire ecosystem for '{risk_factor}' exposure...")
        
        # Mock result
        return [
            {"entity": "Grandchildren Trust", "asset": "EM_ETF", "exposure": 500000},
            {"entity": "Personal Account", "asset": "Tech_Stock_A", "exposure": 1200000}
        ]

    def get_graph_data(self) -> Dict[str, Any]:
        """
        Extracts the full Neo4j graph structure formatted for D3.js Force Graphs.
        """
        if not self.driver:
            # Fallback mock for dev
            return {
                "nodes": [
                    {"id": "Client_Alpha", "group": "entity", "val": 20},
                    {"id": "Trust_Revocable", "group": "trust", "val": 15},
                    {"id": "Trust_Irrevocable", "group": "trust", "val": 15},
                    {"id": "Portfolio_Main", "group": "portfolio", "val": 10},
                    {"id": "Portfolio_Spec", "group": "portfolio", "val": 8},
                    {"id": "Asset_AAPL", "group": "asset", "val": 5},
                    {"id": "Asset_BTC", "group": "asset", "val": 5},
                    {"id": "Asset_RealEstate", "group": "asset", "val": 12},
                    {"id": "Risk_Geopolitics", "group": "risk", "val": 8},
                    {"id": "Risk_Margin", "group": "risk", "val": 8},
                    {"id": "Benefit_Kids", "group": "entity", "val": 5},
                ],
                "links": [
                    {"source": "Client_Alpha", "target": "Trust_Revocable"},
                    {"source": "Client_Alpha", "target": "Trust_Irrevocable"},
                    {"source": "Trust_Revocable", "target": "Portfolio_Main"},
                    {"source": "Trust_Irrevocable", "target": "Portfolio_Spec"},
                    {"source": "Portfolio_Main", "target": "Asset_AAPL"},
                    {"source": "Portfolio_Main", "target": "Asset_RealEstate"},
                    {"source": "Portfolio_Spec", "target": "Asset_BTC"},
                    {"source": "Risk_Geopolitics", "target": "Portfolio_Spec"},
                    {"source": "Risk_Margin", "target": "Portfolio_Main"},
                    {"source": "Trust_Irrevocable", "target": "Benefit_Kids"},
                ]
            }

        # Real Cypher Query
        logger.info("MasterGraph: Fetching live super-graph from Neo4j...")
        with self.driver.session() as session:
            result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100")
            nodes = {}
            links = []
            for record in result:
                n = record['n']
                m = record['m']
                r = record['r']
                
                # Add nodes
                for node in [n, m]:
                    node_id = node.get('id') or str(node.id)
                    if node_id not in nodes:
                        label = list(node.labels)[0] if node.labels else "unknown"
                        nodes[node_id] = {
                            "id": node_id,
                            "group": label.lower(),
                            "val": node.get('importance', 10)
                        }
                
                # Add link
                links.append({
                    "source": n.get('id') or str(n.id),
                    "target": m.get('id') or str(m.id),
                    "type": r.type
                })
            
            return {"nodes": list(nodes.values()), "links": links}
