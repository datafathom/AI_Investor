import sys
import os
import logging
from decimal import Decimal

# Add project root to path
# Ensure local 'scripts/neo4j' doesn't shadow the actual 'neo4j' library
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))

sys.path.append(os.getcwd())

from services.insurance.efficiency_ranker import TaxEfficiencyRanker
from services.insurance.premium_opt import PremiumCadenceOptimizer
from services.neo4j.carrier_graph import CarrierGraphService
from services.simulation.policy_exit import PolicyExitModeler
from services.reporting.jurisdiction_arb import JurisdictionArbService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_177")

def verify_177():
    print("\n" + "="*60)
    print("       PHASE 177: BESPOKE PPLI TAX SHIELD VERIFICATION")
    print("="*60 + "\n")

    # 1. Tax Efficiency Ranker
    print("[*] Testing TaxEfficiencyRanker...")
    ranker = TaxEfficiencyRanker()
    portfolio = [
        {"ticker": "CREDIT", "yield": 0.09, "turnover": 0.1},
        {"ticker": "HEDGE", "yield": 0.02, "turnover": 1.4},
        {"ticker": "VTI", "yield": 0.015, "turnover": 0.03}
    ]
    ranked = ranker.rank_assets(portfolio, Decimal('0.37'), Decimal('0.35'))
    print(f"    Top Candidate: {ranked[0]['ticker']} (Drag: {ranked[0]['tax_drag_bps']} bps)")
    
    # 2. Premium Optimizer
    print("\n[*] Testing PremiumCadenceOptimizer...")
    opt = PremiumCadenceOptimizer()
    res = opt.compare_cadence(Decimal('10000000'), 7, Decimal('0.06'))
    print(f"    Dump-In Advantage: ${res['timing_alpha']:,.2f}")

    # 3. Carrier Graph
    print("\n[*] Testing CarrierGraphService...")
    graph = CarrierGraphService()
    graph.register_policy("Smith Family", "POL-99", "Lombard", 50000000.0)
    exposure = graph.get_carrier_exposure("Smith Family")
    print(f"    Carriers Found: {len(exposure)}")

    # 4. Policy Exit Modeler
    print("\n[*] Testing PolicyExitModeler...")
    exit_mod = PolicyExitModeler()
    sustained = exit_mod.simulate_retirement_draw(Decimal('20000000'), Decimal('1000000'), Decimal('0.04'))
    print(f"    Strategy Status: {sustained['status']} (Sustained: {sustained['years_sustained']} years)")

    # 5. Jurisdiction Arb
    print("\n[*] Testing JurisdictionArbService...")
    arb = JurisdictionArbService()
    report = arb.get_jurisdiction_comparison()
    print(f"    Offshore Cost Advantage: {report['domestic']['avg_m_and_e_bps'] - report['offshore']['avg_m_and_e_bps']} bps")

    print("\n" + "="*60)
    print("               PHASE 177 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_177()
