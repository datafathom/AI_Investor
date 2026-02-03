import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from services.pe.lbo_engine import LBOEngine
from services.pe.efficiency_engine import EfficiencyEngine
from services.neo4j.pe_graph import PEGraphService
from services.kafka.pe_event_producer import PEEventProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_164")

def verify_164():
    print("\n" + "="*60)
    print("       PHASE 164: PE LBO ARCHITECTURE VERIFICATION")
    print("="*60 + "\n")

    # 1. LBO Engine
    print("[*] Testing LBOEngine...")
    lbo = LBOEngine()
    results = lbo.project_deal_returns(
        entry_ebitda=Decimal('50000000'),
        entry_multiple=Decimal('10.0'),
        equity_contribution_pct=Decimal('0.3'),
        exit_multiple=Decimal('10.0'),
        years=5,
        revenue_growth_pct=Decimal('0.05')
    )
    print(f"    MOIC: {results['moic']}x (Expected: ~3.0-4.0x)")
    print(f"    IRR:  {results['irr_pct']}%")

    # 2. Efficiency Engine (Vintage Stats)
    print("\n[*] Testing EfficiencyEngine (Vintage)...")
    eff = EfficiencyEngine()
    vintage = eff.get_vintage_performance(2008)
    print(f"    2008 Cycle: {vintage['market_cycle']} (Expected: TROUGH)")

    # 3. PE Graph
    print("\n[*] Testing PEGraphService...")
    graph = PEGraphService()
    graph.map_lbo_deal("FUND-X", "SaaS-Co", "MegaBank")
    sectors = graph.track_portfolio_concentration("FUND-X")
    print(f"    Mapped Sectors: {sectors}")

    # 4. PE Events (Kafka)
    print("\n[*] Testing PEEventProducer...")
    producer = PEEventProducer()
    producer.publish_liquidity_event("SaaS-Co", "IPO", 1500000000)

    print("\n" + "="*60)
    print("               PHASE 164 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_164()
