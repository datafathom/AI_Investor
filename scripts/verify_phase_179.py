import sys
import os
import logging
import uuid
from decimal import Decimal

# Add project root to path
# Ensure local 'scripts/neo4j' doesn't shadow the actual 'neo4j' library
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))

sys.path.append(os.getcwd())

from services.external.salesforce_adapter import SalesforceAdapter
from services.neo4j.sfo_network_pathfinder import SFONetworkPathfinder
from services.analysis.deal_source_quality import DealSourceQuality
from services.deal.club_deal_manager import ClubDealManager
from services.analysis.event_roi import EventROITracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_179")

def verify_179():
    print("\n" + "="*60)
    print("       PHASE 179: DEAL FLOW NETWORK & CRM VERIFICATION")
    print("="*60 + "\n")

    # 1. Salesforce CRM Sync
    print("[*] Testing SalesforceAdapter...")
    adapter = SalesforceAdapter()
    contacts = adapter.sync_contacts(uuid.uuid4())
    print(f"    Sync Result: {len(contacts)} contacts synced.")
    
    # 2. Neo4j Pathfinding
    print("\n[*] Testing SFONetworkPathfinder...")
    pf = SFONetworkPathfinder()
    res = pf.find_shortest_connection(uuid.uuid4(), "Elon Musk")
    experts = pf.find_expert_connection("TECH")
    print(f"    Path Result: {res['status']} (Intermediary: {res['intermediary']})")
    print(f"    Experts Found: {len(experts)}")

    # 3. Deal Source Quality
    print("\n[*] Testing DealSourceQuality...")
    quality = DealSourceQuality()
    history = [
        {"moic": 3.5, "invested": True},
        {"moic": 0.5, "invested": False},
        {"moic": 12.0, "invested": True}
    ]
    score = quality.analyze_source("Goldman", history)
    print(f"    Source Score: {score['quality_score']} (Recommendation: {score['recommendation']})")

    # 4. Club Deal Manager
    print("\n[*] Testing ClubDealManager...")
    mgr = ClubDealManager()
    club = mgr.create_club_deal("SpaceX Pre-IPO", 50000000.0, 10000000.0, [uuid.uuid4()])
    print(f"    Club Deal Status: {club['status']} (ID: {club['deal_id']})")

    # 5. Event ROI Tracker
    print("\n[*] Testing EventROITracker...")
    tracker = EventROITracker()
    roi = tracker.calculate_event_roi("Davos", Decimal('50000'), 20, 1, Decimal('500000'))
    print(f"    Event ROI: {roi['hard_roi_multiplier']}x ({roi['status']})")

    print("\n" + "="*60)
    print("               PHASE 179 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_179()
