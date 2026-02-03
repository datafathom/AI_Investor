import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from services.performance.staff_attribution import StaffAttributionEngine
from services.operations.outsource_calc import OperationsOutsourceCalculator
from services.operations.workload_tracker import OperationalWorkloadService
from services.pe.efficiency_engine import EfficiencyEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_163")

def verify_163():
    print("\n" + "="*60)
    print("       PHASE 163: CIO & PROFESSIONAL COMP VERIFICATION")
    print("="*60 + "\n")

    # 1. Staff Attribution
    print("[*] Testing StaffAttributionEngine...")
    engine = StaffAttributionEngine()
    perf = engine.calculate_professional_alpha(
        "PM-JONES", 
        Decimal('0.15'), 
        Decimal('0.10'), 
        Decimal('100000000')
    )
    print(f"    Alpha BPS: {perf['alpha_bps']} (Expected: 500.0)")
    print(f"    Alpha $:   ${perf['alpha_dollar_value']:,.2f} (Expected: $5,000,000.00)")
    
    # 2. Compensation Benchmarking
    print("\n[*] Testing Benchmarks...")
    cio_comp = engine.get_comp_benchmark("CIO")
    print(f"    CIO Base Min: ${cio_comp['market_base_range'][0]:,}")

    # 3. Build vs Buy
    print("\n[*] Testing OutsourceCalculator...")
    outsource = OperationsOutsourceCalculator()
    eval_res = outsource.evaluate_hiring_choice("ACCOUNTANT", 100)
    print(f"    Accountant Recommendation: {eval_res['recommendation']}")

    # 4. Workload Tracker
    print("\n[*] Testing OperationalWorkloadService...")
    workload = OperationalWorkloadService()
    workload.assign_seat("USER-1", "BLOOMBERG")
    burn = workload.get_monthly_tech_burn()
    print(f"    Monthly Tech Burn: ${burn:,.2f} (Expected: $2,400.00)")

    print("\n" + "="*60)
    print("               PHASE 163 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_163()
