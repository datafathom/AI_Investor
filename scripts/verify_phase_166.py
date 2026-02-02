import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from services.kafka.deal_consumer import DealConsumer
from services.neo4j.syndication_graph import SyndicationGraphService
from services.real_estate.syndication_service import SyndicationService
from services.compliance.compliance_506b import Compliance506bFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_166")

def verify_166():
    print("\n" + "="*60)
    print("       PHASE 166: SYNDICATION NETWORK VERIFICATION")
    print("="*60 + "\n")

    # 1. Deal Consumer (Kafka)
    print("[*] Testing DealConsumer...")
    cons = DealConsumer()
    cons.process_message({"id": "DEAL-1", "sponsor": "Sponsor-A", "target_irr": 18.5})

    # 2. Compliance Filter
    print("\n[*] Testing Compliance506bFilter...")
    comp = Compliance506bFilter()
    res = comp.validate_offering_access("USER-1", "DEAL-1", True)
    print(f"    Can access: {res['can_access']} (Expected: True)")

    # 3. Syndication Graph
    print("\n[*] Testing SyndicationGraphService...")
    graph = SyndicationGraphService()
    graph.map_syndication("GP-1", ["LP-1", "LP-2"], "DEAL-1")
    track = graph.get_sponsor_track_record("GP-1")
    print(f"    GP Track Record MOIC: {track['avg_moic']}")

    # 4. Syndication Service (Raise Tracker)
    print("\n[*] Testing SyndicationService (Commitments)...")
    service = SyndicationService()
    service.soft_circle("DEAL-1", "LP-1", Decimal('500000'))
    status = service.get_raise_status("DEAL-1", Decimal('5000000'))
    print(f"    Raise Pct: {status['pct_complete']}% (Expected: 10.0)")

    print("\n" + "="*60)
    print("               PHASE 166 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_166()
