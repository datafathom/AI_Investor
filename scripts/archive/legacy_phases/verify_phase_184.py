import sys
import os
import logging
from decimal import Decimal

# Add project root to path and remove scripts to avoid neo4j shadowing
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))
sys.path.append(os.getcwd())

from services.tax.exit_tax_service import ExitTaxService
from services.legal.residency_timer import ResidencyTimer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_184")

def verify_184():
    print("\n" + "="*60)
    print("       PHASE 184: EXIT TAX & RESIDENCY VERIFICATION")
    print("="*60 + "\n")

    # 1. Residency History (8-of-15 Rule)
    print("[*] Testing ResidencyTimer (8-of-15 Rule)...")
    timer = ResidencyTimer()
    history = [y for y in range(2010, 2025)] # 15 years
    res = timer.validate_expatriation_eligibility(history)
    print(f"    Years in period: {res['residency_years_count']}, Covered Resident: {res['is_long_term_resident']}")

    # 2. Covered Expatriate Status (NW & Tax)
    print("\n[*] Testing ExitTaxService Status Check...")
    svc = ExitTaxService()
    # Case: NW > $2M
    status = svc.check_covered_status(Decimal("2500000.00"), Decimal("150000.00"), True)
    print(f"    NW: $2.5M -> Covered: {status['is_covered_expatriate']} (Reasons: {status['reasons']})")
    
    # Case: Tax > $190k
    status2 = svc.check_covered_status(Decimal("1500000.00"), Decimal("200000.00"), True)
    print(f"    Tax: $200k -> Covered: {status2['is_covered_expatriate']} (Reasons: {status2['reasons']})")

    # 3. Phantom Sale Calculation
    print("\n[*] Testing Exit Tax Bill Calculation (Phantom Sale)...")
    gains = Decimal("2000000.00")
    bill = svc.calculate_exit_tax(gains, {"is_covered_expatriate": True})
    print(f"    Gains: $2M -> Taxable: ${bill['taxable_gain']:,.2f}, Bill: ${bill['estimated_tax_bill']:,.2f}")

    print("\n" + "="*60)
    print("               PHASE 184 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_184()
