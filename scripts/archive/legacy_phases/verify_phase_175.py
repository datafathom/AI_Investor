import sys
import os
import logging
from uuid import uuid4
from decimal import Decimal

# Add project root to path
# Ensure local 'scripts/neo4j' doesn't shadow the actual 'neo4j' library
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))

sys.path.append(os.getcwd())

from services.mfo.concierge_srv import ConciergeService
from services.mfo.spend_aggregator import MFOSpendAggregator
from services.neo4j.expert_network import ExpertNetworkGraph
from services.education.mfo_content import MFOEducationPortal
from services.compliance.fee_tier_check import FeeTierValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_175")

def verify_175():
    print("\n" + "="*60)
    print("       PHASE 175: MFO CONCIERGE LAYER RE-VERIFICATION")
    print("="*60 + "\n")

    # 1. Concierge Service
    print("[*] Testing ConciergeService...")
    concierge = ConciergeService()
    res = concierge.create_lifestyle_request(uuid4(), "TRAVEL", "Book private jet to Aspen URGENT")
    print(f"    Ticket: {res['ticket_id']}, Priority: {res['priority']}")
    
    # 2. Spend Aggregator
    print("\n[*] Testing MFOSpendAggregator...")
    sa = MFOSpendAggregator()
    leverage = sa.calculate_group_leverage("NetJets", [250000, 300000, 500000])
    print(f"    Discount: {leverage['group_discount_pct']}% (Expected: 15.0%)")

    # 3. Expert Network
    print("\n[*] Testing ExpertNetworkGraph...")
    eng = ExpertNetworkGraph()
    eng.register_expert("Dr. Smith", "Cybersecurity", 4.9)

    # 4. Education Portal
    print("\n[*] Testing MFOEducationPortal...")
    edu = MFOEducationPortal()
    courses = edu.get_available_courses()
    print(f"    Courses Available: {len(courses)}")

    # 5. Fee Tier Validator
    print("\n[*] Testing FeeTierValidator...")
    validator = FeeTierValidator()
    audit = validator.audit_fee_tier("SPY-PF", 9, 9, 3) # Current 9, Retail 9, Inst 3
    print(f"    Fee Status: {audit['status']} (Leakage: {audit['leakage_bps']} bps)")

    print("\n" + "="*60)
    print("               PHASE 175 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_175()
