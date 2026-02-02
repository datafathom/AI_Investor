import sys
import os
import logging
from uuid import uuid4

# Add project root to path
sys.path.append(os.getcwd())

from services.compliance.ppli_gate import PPLIEligibilityGate
from services.insurance.ppli_withdrawal import PPLIWithdrawalEngine
from services.legal.ppli_structure import PPLIStructureValidator
from services.neo4j.ppli_graph import PPLIGraphService
from services.wealth.ppli_forecaster import PPLIForecaster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_168")

def verify_168():
    print("\n" + "="*60)
    print("       PHASE 168: PPLI WRAPPER INTEGRATION VERIFICATION")
    print("="*60 + "\n")

    # 1. Eligibility Gate (MEC Check)
    print("[*] Testing PPLIEligibilityGate (MEC)...")
    gate = PPLIEligibilityGate()
    mec_res = gate.check_mec_status(500000, 400000) # MEC triggered
    print(f"    MEC Triggered: {mec_res['is_mec']} (Expected: True)")
    
    # 2. Withdrawal Engine
    print("\n[*] Testing PPLIWithdrawalEngine...")
    engine = PPLIWithdrawalEngine()
    loan = engine.calculate_max_loan(1000000, 20000)
    print(f"    Max Loan: ${loan['max_safe_loan']:,.2f}")

    # 3. Structure Validator
    print("\n[*] Testing PPLIStructureValidator...")
    validator = PPLIStructureValidator()
    valid = validator.validate_ownership("IRREVOCABLE_TRUST", "PPLI")
    print(f"    Optimal Structure: {valid['is_estate_tax_shielded']} (Expected: True)")

    # 4. Graph Service
    print("\n[*] Testing PPLIGraphService...")
    graph = PPLIGraphService()
    pol_id = uuid4()
    trust_id = uuid4()
    graph.link_ppli_to_trust(pol_id, trust_id)

    # 5. Forecaster
    print("\n[*] Testing PPLIForecaster...")
    fc = PPLIForecaster()
    proj = fc.forecast(1000000, 100000, 0.08)
    print(f"    Year 30 Projection: ${proj[-1]['value']:,.2f}")

    print("\n" + "="*60)
    print("               PHASE 168 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_168()
