import sys
import os
import logging
from decimal import Decimal

# Add project root to path
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))
sys.path.append(os.getcwd())

from services.quantitative.reflexivity_engine import ReflexivityEngine
from services.risk.saturation_monitor import SaturationMonitor
from services.neo4j.flow_graph import FlowGraph
from services.simulation.reflexivity_sim import ReflexivitySim
from services.alerts.demographic_risk import DemographicRiskMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_182")

def verify_182():
    print("\n" + "="*60)
    print("       PHASE 182: REFLEXIVITY & PASSIVE BUBBLE VERIFICATION")
    print("="*60 + "\n")

    # 1. Reflexivity Engine
    print("[*] Testing ReflexivityEngine...")
    engine = ReflexivityEngine()
    res = engine.check_passive_saturation("AAPL", 45000000, 100000000)
    print(f"    Saturation: {res['passive_ownership_pct']}% (Saturated: {res['is_saturated_reflexive']})")

    # 2. Saturation Monitor (Postgres)
    print("\n[*] Testing SaturationMonitor...")
    sm = SaturationMonitor()
    log = sm.log_saturation_event("AAPL", 0.45)
    print(f"    Logged Status: {log['status']}")

    # 3. Flow Graph (Neo4j)
    print("\n[*] Testing FlowGraph (Neo4j)...")
    fg = FlowGraph()
    flow = fg.model_mechanical_bid("401K_INFLOW", "SP500", 500.0)
    print(f"    Modeled {flow['flow_m']}M flow into {flow['target']}")

    # 4. Reflexivity Sim
    print("\n[*] Testing ReflexivitySim...")
    sim = ReflexivitySim()
    hist = sim.simulate_feedback_loop(450.0, 0.45, steps=3)
    print(f"    Sim Step 3 Price: ${hist[2]['price']}")
    
    unwind = sim.simulate_unwind(hist[2]['price'], 0.15)
    print(f"    Unwind Result: {unwind['status']} (Price: ${unwind['final_unwind_price']})")

    # 5. Demographic Risk
    print("\n[*] Testing DemographicRiskMonitor...")
    drm = DemographicRiskMonitor()
    net = drm.calculate_net_flow_status(12.5, 8.2)
    print(f"    Net 401k Flow: ${net['net_flow_b']}B ({net['status']})")

    print("\n" + "="*60)
    print("               PHASE 182 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_182()
