import sys
import os
import logging
from decimal import Decimal

# Add project root to path
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))
sys.path.append(os.getcwd())

from services.reporting.global_risk_aggregator import GlobalRiskAggregator
from services.analysis.macro_service import MacroService
from services.reporting.total_wealth import TotalWealthCalculator
from services.trading.fx_service import get_fx_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_180")

def verify_180():
    print("\n" + "="*60)
    print("       PHASE 180: GLOBAL RISK & SOVEREIGNTY VERIFICATION")
    print("="*60 + "\n")

    # 1. Global Risk Aggregator
    print("[*] Testing GlobalRiskAggregator...")
    agg = GlobalRiskAggregator()
    positions = [
        {"country_code": "US", "market_value": Decimal('1000000')},
        {"country_code": "UK", "market_value": Decimal('500000')},
        {"country_code": "CH", "market_value": Decimal('2000000')}
    ]
    res = agg.aggregate_geo_exposure(positions)
    print(f"    Sovereign Exposure: {res['sovereign_exposure']}")

    # 2. Macro Kafka Bridge
    print("\n[*] Testing MacroService Kafka Bridge...")
    macro = MacroService()
    event = macro.produce_macro_event("GEOPOLITICAL_SHOCK", {"region": "MIDDLE_EAST", "severity": "HIGH"})
    print(f"    Produced Event: {event['event_type']} at {event['timestamp']}")

    # 3. Total Wealth Unified View
    print("\n[*] Testing TotalWealthCalculator...")
    twc = TotalWealthCalculator()
    wealth = twc.aggregate_net_worth(
        Decimal('5000000'), 
        Decimal('10000000'), 
        Decimal('2000000'), 
        Decimal('8000000')
    )
    print(f"    Total Net Worth: ${wealth['total_net_worth']:,.2f} (Alt Exposure: {wealth['alternative_exposure_pct']}%)")

    # 4. FX Converter
    print("\n[*] Testing FXService...")
    fx = get_fx_service()
    val = fx.get_supported_currencies()
    print(f"    Supported Currencies: {val}")

    # 5. Completion Audit
    print("\n[*] Testing Epoch IX Audit Script...")
    from scripts.audits.epoch_ix_audit import EpochIXAuditor
    auditor = EpochIXAuditor()
    audit_res = auditor.run_full_audit()
    print(f"    Audit Result: {audit_res['status']} ({audit_res['readiness_pct']}%)")

    print("\n" + "="*60)
    print("               PHASE 180 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_180()
