import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from services.crm.client_priority import PriorityScorer
from services.compliance.velvet_rope import VelvetRopeGate
from services.deal.deal_allocation_srv import DealAllocationService
from services.deal.waitlist_manager import WaitlistManager
from services.neo4j.tier_graph import TierGraphService
from services.notifications.fomo_alert import FOMOAlertService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_173")

def verify_173():
    print("\n" + "="*60)
    print("       PHASE 173: DEAL FLOW PRIORITY VERIFICATION")
    print("="*60 + "\n")

    # 1. Priority Scorer
    print("[*] Testing PriorityScorer...")
    crm = PriorityScorer()
    res = crm.calculate_priority(100_000_000, True) # SFO
    print(f"    Tier: {res['tier']} (Expected: TIER_1_SFO)")
    
    # 2. Velvet Rope Gate
    print("\n[*] Testing VelvetRopeGate...")
    gate = VelvetRopeGate()
    access = gate.can_access_deal("TIER_3_RETAIL", "TIER_2_UHNW")
    print(f"    Retail Access (Min UHNW): {access} (Expected: False)")

    # 3. Allocation Service
    print("\n[*] Testing DealAllocationService...")
    service = DealAllocationService()
    commitments = [
        {"user": "SFO-A", "amount": Decimal('6000000'), "tier": "SFO"},
        {"user": "UHNW-B", "amount": Decimal('6000000'), "tier": "UHNW"},
    ]
    allocs = service.allocate_oversubscribed_deal(Decimal('8000000'), commitments)
    print(f"    SFO-A Allocated: ${allocs[0]['allocated']:,.2f} (Expected: $6,000,000.00)")
    print(f"    UHNW-B Allocated: ${allocs[1]['allocated']:,.2f} (Expected: $2,000,000.00)")

    # 4. Waitlist Manager
    print("\n[*] Testing WaitlistManager...")
    wm = WaitlistManager()
    wm.log_interest("DEAL-99", "USER-1", 1000000, "TIER_2_UHNW")

    # 5. Tier Graph
    print("\n[*] Testing TierGraphService...")
    graph = TierGraphService()
    graph.tag_client_tier("USER-1", "TIER_2_UHNW", 2)

    # 6. FOMO Alert
    print("\n[*] Testing FOMOAlertService...")
    fomo = FOMOAlertService()
    fomo.push_scarcity_alert("Tech Unicorn", 500000, "TIER_1_SFO")

    print("\n" + "="*60)
    print("               PHASE 173 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_173()
