import sys
import os
import logging
from decimal import Decimal
import uuid

# Add project root to path
sys.path.append(os.getcwd())

from services.mfo.expense_allocator import MFOExpenseAllocator
from services.trading.trade_aggregator import TradeAggregator
from services.neo4j.mfo_graph import MFOGraphService
from services.compliance.privacy_disclosure import PrivacyDisclosureService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_162")

def verify_162():
    print("\n" + "="*60)
    print("       PHASE 162: MFO SHARED-COST LOGIC VERIFICATION")
    print("="*60 + "\n")

    # 1. Expense Allocator
    print("[*] Testing MFOExpenseAllocator...")
    allocator = MFOExpenseAllocator()
    family_aums = {
        "FAM-1": Decimal('50000000'),
        "FAM-2": Decimal('25000000'),
        "FAM-3": Decimal('25000000')
    }
    allocs = allocator.split_monthly_overhead(Decimal('100000'), family_aums, method='PRO_RATA')
    print(f"    FAM-1 Allocation: ${allocs[0]['amount']:,.2f} (Expected: $50,000.00)")
    
    # 2. Trade Aggregator
    print("\n[*] Testing TradeAggregator...")
    aggregator = TradeAggregator()
    orders = [
        {"id": "O1", "family_id": "F1", "quantity": 1000},
        {"id": "O2", "family_id": "F2", "quantity": 2000}
    ]
    block = aggregator.aggregate_orders("AAPL", orders)
    print(f"    Block Quantity: {block['total_quantity']} (Expected: 3000)")
    
    # Partial fill allocation
    fills = aggregator.allocate_fill(block['block_id'], 1500, orders)
    print(f"    F1 Fill: {fills[0]['allocated_quantity']} (Expected: 500)")
    print(f"    F2 Fill: {fills[1]['allocated_quantity']} (Expected: 1000)")

    # 3. MFO Graph (Mock)
    print("\n[*] Testing MFOGraphService...")
    graph = MFOGraphService()
    res = graph.map_shared_professional("PROF-99", [uuid.uuid4(), uuid.uuid4()])
    print(f"    Graph Privacy Guard: {res['privacy_enforced']}")

    # 4. Privacy Disclosure
    print("\n[*] Testing PrivacyDisclosureService...")
    disc_svc = PrivacyDisclosureService()
    text = disc_svc.generate_shared_service_disclosure("Windsor Family", ["Trade Block", "Concierge"])
    print(f"    Disclosure Generated: {len(text) > 50}")
    print(f"    Risk Metric: {disc_svc.get_risk_assessment()['mfo_privacy_score']}")

    print("\n" + "="*60)
    print("               PHASE 162 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_162()
