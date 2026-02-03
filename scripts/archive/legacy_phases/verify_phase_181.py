import sys
import os
import logging
import uuid
from decimal import Decimal
from datetime import date

# Add project root to path
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))
sys.path.append(os.getcwd())

from services.risk.valuation_gap_analyzer import ValuationGapAnalyzer
from services.risk.advanced_risk_metrics_service import get_risk_metrics_service
from services.risk.risk_monitor import get_risk_monitor
from services.neo4j.perception_graph import PerceptionGraph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_181")

def verify_181():
    print("\n" + "="*60)
    print("       PHASE 181: OSTRICH IN THE SAND VERIFICATION")
    print("="*60 + "\n")

    # 1. Valuation Gap Analyzer
    print("[*] Testing ValuationGapAnalyzer...")
    vga = ValuationGapAnalyzer()
    res = vga.calculate_gap("SpaceX PE", Decimal('100000000'), date.today(), "QQQ")
    print(f"    Gap Found: {res['gap_percentage']:.1%} (Risk: {res['risk_flag']})")

    # 2. Hidden Volatility Scorer
    print("\n[*] Testing Hidden Volatility Scorer...")
    arms = get_risk_metrics_service()
    hvol = arms.calculate_hidden_volatility_score(0.12, 0.25, 5)
    print(f"    True Volatility: {hvol['true_volatility']:.1%}")
    print(f"    Risk Score:      {hvol['hidden_vol_score']}/100 ({hvol['status']})")

    # 3. Kafka Liquidity Trigger
    print("\n[*] Testing Kafka Liquidity Trigger...")
    rm = get_risk_monitor()
    trigger = rm.trigger_liquidity_markdown(str(uuid.uuid4()), 0.30)
    print(f"    Triggered: {trigger['reason']} for {trigger['asset_id']}")

    # 4. Perception Graph (Neo4j)
    print("\n[*] Testing PerceptionGraph (Neo4j)...")
    pg = PerceptionGraph()
    graph_res = pg.model_ostrich_risk(uuid.uuid4(), 0.55)
    print(f"    Graph Status: {graph_res['status']} (Is Ostrich: {graph_res['is_ostrich']})")

    print("\n" + "="*60)
    print("               PHASE 181 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_181()
