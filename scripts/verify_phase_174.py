import sys
import os
import logging
from datetime import datetime

# Add project root to path
# Ensure local 'scripts/neo4j' doesn't shadow the actual 'neo4j' library
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))

sys.path.append(os.getcwd())

from services.neo4j.alts_graph import AltsGraphService
from services.external.masterworks_adapter import MasterworksAdapter
from services.external.chrono24_adapter import Chrono24Adapter
from services.alts.cost_tracker import AltsCostTracker
from services.tax.k1_tracker import K1Tracker
from services.portfolio.emotional_utility import EmotionalUtilityOptimizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_174")

def verify_174():
    print("\n" + "="*60)
    print("       PHASE 174: ALTERNATIVE ASSETS VERIFICATION")
    print("="*60 + "\n")

    # 1. Alts Graph
    print("[*] Testing AltsGraphService...")
    graph = AltsGraphService()
    graph.create_alt_asset_class("Blue Chip Art", 0.1, "LOW")
    graph.link_asset_to_portfolio("PORT-1", "Blue Chip Art", 0.05)
    
    # 2. External Adapters
    print("\n[*] Testing External Adapters...")
    mw = MasterworksAdapter()
    art_val = mw.fetch_artwork_value("Warhol", "w-101")
    print(f"    Masterworks Value: ${art_val['market_value_usd']:,.2f}")
    
    c24 = Chrono24Adapter()
    watch_val = c24.fetch_watch_value("Rolex", "Daytona")
    print(f"    Chrono24 Value: ${watch_val['market_value_usd']:,.2f}")

    # 3. Cost Tracker
    print("\n[*] Testing AltsCostTracker...")
    ct = AltsCostTracker()
    costs = ct.calculate_annual_maintenance("WATCH-7", 100000, "WATCH")
    print(f"    Annual Carry: ${costs['total_carry_cost']:,.2f} ({costs['carry_pct']}%)")

    # 4. K-1 Tracker
    print("\n[*] Testing K1Tracker...")
    k1 = K1Tracker()
    status = k1.check_k1_status("HedgeFund-A", 2024)
    print(f"    K-1 Status: {status['status']}")

    # 5. Emotional Utility
    print("\n[*] Testing EmotionalUtilityOptimizer...")
    util = EmotionalUtilityOptimizer()
    index = util.calculate_weighted_utility(0.08, 0.90) # 8% return, 0.9 emotional value
    print(f"    Total Utility Index: {index['total_utility_index']}")

    print("\n" + "="*60)
    print("               PHASE 174 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_174()
