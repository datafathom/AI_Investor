import sys
import os
import logging
from decimal import Decimal

# Add project root to path
# Ensure local 'scripts/neo4j' doesn't shadow the actual 'neo4j' library
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))

sys.path.append(os.getcwd())

from services.pe.efficiency_engine import EfficiencyEngine
from services.pe.working_capital import WorkingCapitalCalc
from services.pe.synergy_est import SynergyEstimator
from services.analysis.pricing_power import PricingPowerModel
from services.simulation.sensitivity_analysis import SensitivityEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_176")

def verify_176():
    print("\n" + "="*60)
    print("       PHASE 176: LBO OPS SIMULATOR VERIFICATION")
    print("="*60 + "\n")

    # 1. Efficiency Engine
    print("[*] Testing EfficiencyEngine...")
    ee = EfficiencyEngine()
    res = ee.simulate_value_creation(
        Decimal('50000000'), # 50M EBITDA
        Decimal('100000000'), # 100M OpEx
        Decimal('0.15'), # 15% cut
        Decimal('0.05') # 5% efficiency
    )
    print(f"    New EBITDA: ${res['revised_ebitda']:,.2f} (Savings: ${res['opex_savings']:,.2f})")
    
    # 2. Working Capital
    print("\n[*] Testing WorkingCapitalCalc...")
    wc = WorkingCapitalCalc()
    unlocked = wc.calculate_cash_unlock(Decimal('500000000'), 10, "DSO")
    print(f"    10-day DSO Improvement: ${unlocked['cash_unlocked_usd']:,.2f}")

    # 3. Synergy Estimator
    print("\n[*] Testing SynergyEstimator...")
    se = SynergyEstimator()
    synergies = se.estimate_synergies(Decimal('100000000'), Decimal('20000000'), Decimal('0.3'))
    print(f"    Total Synergy Value: ${synergies['total_synergy_value']:,.2f}")

    # 4. Pricing Power
    print("\n[*] Testing PricingPowerModel...")
    pp = PricingPowerModel()
    hike = pp.simulate_price_hike(Decimal('500000000'), Decimal('0.05'), Decimal('-1.2'))
    print(f"    5% Hike (-1.2 Elasticity): Net Impact ${hike['net_revenue_impact']:,.2f}")

    # 5. Sensitivity Engine
    print("\n[*] Testing SensitivityEngine...")
    sim = SensitivityEngine()
    res = sim.run_sensitivity_scenarios(Decimal('120000000'), 10.0)
    print(f"    Mean Simulated Valuation: ${res['mean_valuation']:,.2f}")

    print("\n" + "="*60)
    print("               PHASE 176 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_176()
