import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from services.credit.loan_tape_svc import LoanTapeService
from services.credit.credit_risk_engine import CreditRiskEngine
from services.pe.waterfall_engine import WaterfallEngine
from services.neo4j.covenant_graph import CovenantGraphService
from services.analysis.rate_exposure import RateExposureAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_171")

def verify_171():
    print("\n" + "="*60)
    print("       PHASE 171: PRIVATE CREDIT TRACKER VERIFICATION")
    print("="*60 + "\n")

    # 1. Loan Tape Ingestion
    print("[*] Testing LoanTapeService...")
    tape = LoanTapeService()
    res = tape.ingest_tape([{"principal": 1000000}, {"principal": 2500000}])
    print(f"    Total Committed: ${res['total_committed']:,.2f} (Expected: $3,500,000.00)")
    
    # 2. Risk Engine
    print("\n[*] Testing CreditRiskEngine...")
    risk = CreditRiskEngine()
    yield_res = risk.calculate_expected_net_yield(650, Decimal('0.05'), Decimal('0.02'), Decimal('0.60'))
    print(f"    Net Yield: {yield_res['net_yield_pct']}% (Expected: 10.7%)")

    # 3. Waterfall Engine
    print("\n[*] Testing WaterfallEngine...")
    wf = WaterfallEngine()
    dist = wf.calculate_distributions(Decimal('500000'), Decimal('5000000'), Decimal('0.08'))
    print(f"    LP Dist: ${dist['total_lp_dist']:,.2f}")

    # 4. Covenant Graph
    print("\n[*] Testing CovenantGraphService...")
    graph = CovenantGraphService()
    graph.link_covenant_to_borrower("TechCorp", "L-77", "Debt/EBITDA", 4.5)

    # 5. Rate Exposure
    print("\n[*] Testing RateExposureAnalyzer...")
    analyzer = RateExposureAnalyzer()
    port = [{"principal": 10000000, "is_floating": True}, {"principal": 5000000, "is_floating": False}]
    sens = analyzer.analyze_sensitivity(port, 100) # +1% shift
    print(f"    100bps Impact: ${sens['annual_income_impact']:,.2f} (Expected: $100,000.00)")

    print("\n" + "="*60)
    print("               PHASE 171 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_171()
