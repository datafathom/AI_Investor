import sys
import os
import logging
from uuid import uuid4

# Add project root to path
sys.path.append(os.getcwd())

from services.hr.heir_governance_svc import HeirGovernanceService
from services.analysis.productivity_model import ProductivityModel
from services.reporting.perception_gap import PerceptionGapReporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_170")

def verify_170():
    print("\n" + "="*60)
    print("       PHASE 170: HEIR GOVERNANCE VERIFICATION")
    print("="*60 + "\n")

    # 1. Heir Governance Service
    print("[*] Testing HeirGovernanceService (KPI Override)...")
    service = HeirGovernanceService()
    final = service.apply_discretionary_kpi_override("HEIR-01", 40.0, 95.0)
    print(f"    Final Score: {final} (Expected: 73.0)")
    
    # 2. Nepotism Check
    print("\n[*] Testing Nepotism Check...")
    role = service.evaluate_role_productivity(uuid4(), "VP Social", 250000, 100000)
    print(f"    Status: {role['status']} (Expected: CUSHY_JOB)")

    # 3. Productivity Model
    print("\n[*] Testing ProductivityModel...")
    model = ProductivityModel()
    yield_res = model.calculate_social_yield(30.0, 90.0, 95.0)
    print(f"    Total Index: {yield_res['total_productivity_index']}")

    # 4. Perception Gap
    print("\n[*] Testing PerceptionGapReporter...")
    reporter = PerceptionGapReporter()
    gap = reporter.compare_perception(100000, 180000) # 80% gap
    print(f"    Status: {gap['governance_status']} (Expected: CRITICAL)")

    print("\n" + "="*60)
    print("               PHASE 170 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_170()
