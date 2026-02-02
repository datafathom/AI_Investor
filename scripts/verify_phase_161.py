import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from services.sfo.sfo_justification import SFOJustificationEngine
from services.neo4j.sfo_network_pathfinder import SFONetworkPathfinder
from services.simulation.sfo_simulator import SFOSimulator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_161")

def verify_161():
    print("\n" + "="*60)
    print("       PHASE 161: SFO ECONOMY OF SCALE VERIFICATION")
    print("="*60 + "\n")

    # 1. Justification Engine
    print("[*] Testing SFOJustificationEngine...")
    engine = SFOJustificationEngine()
    
    # Case A: $50M AUM (Should NOT be viable)
    result_low = engine.run_breakeven_analysis(Decimal('50000000'))
    print(f"    $50M AUM Viability: {result_low['is_sfo_economically_viable']} (Expected: False)")
    
    # Case B: $250M AUM (Should BE viable)
    result_high = engine.run_breakeven_analysis(Decimal('250000000'))
    print(f"    $250M AUM Viability: {result_high['is_sfo_economically_viable']} (Expected: True)")
    
    # 2. Budget Template
    print("\n[*] Testing Budget Template...")
    budget = engine.get_standard_budget()
    print(f"    OpEx Personnel CIO: ${budget['personnel']['cio']:,}")
    print(f"    Total OpEx: ${budget['total_op_ex']:,}")

    # 3. Neo4j Pathfinder (Mock check)
    print("\n[*] Testing SFONetworkPathfinder...")
    import uuid
    pathfinder = SFONetworkPathfinder()
    path = pathfinder.find_shortest_connection(uuid.uuid4(), "John Doe")
    print(f"    Connection Status: {path['status']}")
    print(f"    Intermediary: {path['intermediary']}")

    # 4. Simulation
    print("\n[*] Testing SFOSimulator...")
    sim = SFOSimulator()
    vibe = sim.calculate_break_even(150000000, 1000000)
    print(f"    Sim Viability: {vibe['is_viable']}")
    print(f"    Cost Ratio: {vibe['cost_ratio_pct']:.2f}%")

    print("\n" + "="*60)
    print("               PHASE 161 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_161()
