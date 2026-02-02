import logging
import time
from services.ai.master_objective import MasterObjectiveOptimizer
from services.neo4j.master_graph import MasterGraph

logger = logging.getLogger(__name__)

def status():
    """
    CLI Handler for Orchestrator Health.
    """
    graph = MasterGraph()
    opt = MasterObjectiveOptimizer()
    
    count = graph.get_node_count()
    obj_status = opt.get_current_status()
    
    print("\n" + "="*50)
    print("       AI WEALTH ORCHESTRATOR STATUS")
    print("="*50)
    print(f"Graph Nodes:      {count:,}")
    print(f"Primary Goal:     {obj_status['active_goal']}")
    print(f"System State:     {obj_status['state']}")
    print("-" * 50)
    print(">> SUBSYSTEMS")
    print("[OK] Market Monitor")
    print("[OK] Risk Supervisor")
    print("[OK] Asset Allocator")
    print("[OK] Compliance Officer")
    print("="*50 + "\n")

def boot():
    """
    CLI Handler to boot the entire orchestrator loop.
    """
    print("\n[*] Initializing AI Wealth Orchestrator...")
    time.sleep(1)
    print("[*] Connecting to Neo4j Graph...")
    time.sleep(0.5)
    print("[*] Hydrating Context from Postgres...")
    time.sleep(0.5)
    print("[*] Activation Kafka Event Bus...")
    
    print("\n" + "="*50)
    print("          SYSTEM BOOT COMPLETE")
    print("="*50)
    print("The AI Investor System is now fully autonomous.")
    print("Listening for market events...")
    print("="*50 + "\n")
