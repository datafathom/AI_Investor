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

from services.portfolio.endowment_model import EndowmentModel
from services.planning.spending_rule import SpendingRule
from services.sfo.governance import GovernanceService
from services.education.heir_lms import HeirLMSService
from services.simulation.philanthropy_sim import PhilanthropySim

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_178")

def verify_178():
    print("\n" + "="*60)
    print("       PHASE 178: MULTI-GENERATIONAL MANDATE VERIFICATION")
    print("="*60 + "\n")

    # 1. Endowment Model
    print("[*] Testing EndowmentModel...")
    em = EndowmentModel()
    alloc = em.generate_allocation(Decimal('1000000000'))
    print(f"    Private Equity Target: ${alloc['allocation_usd']['private_equity']:,.2f}")
    
    # 2. Spending Rule
    print("\n[*] Testing SpendingRule...")
    sr = SpendingRule()
    spend = sr.calculate_safe_spend(Decimal('1000000000'), Decimal('0.07'), Decimal('0.03'))
    print(f"    Max Annual Spend: ${spend['max_spend_usd']:,.2f} (Rate: {spend['safe_spend_rate_pct']}%)")

    # 3. Governance Service
    print("\n[*] Testing GovernanceService...")
    gov = GovernanceService()
    family_id = uuid.uuid4()
    c = gov.create_constitution(family_id, "Preserve wealth for 100 years.", ["Integrity", "Impact"])
    res = gov.ratify_constitution(c['id'], [uuid.uuid4()])
    print(f"    Constitution: {res['status']} on {res['date']}")

    # 4. Heir LMS
    print("\n[*] Testing HeirLMSService...")
    lms = HeirLMSService()
    progress = lms.record_progress(uuid.uuid4(), "FIN-101", 95)
    print(f"    Course Status: {progress['status']} (Certified: {progress['certified']})")

    # 5. Philanthropy Sim
    print("\n[*] Testing PhilanthropySim...")
    ps = PhilanthropySim()
    legacy = ps.simulate_legacy(Decimal('50000000'), Decimal('0.05'))
    print(f"    100-Year Impact: ${legacy['total_granted_100yr']:,.2f} (Society Multiplier: {legacy['society_multiplier']}x)")

    print("\n" + "="*60)
    print("               PHASE 178 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_178()
