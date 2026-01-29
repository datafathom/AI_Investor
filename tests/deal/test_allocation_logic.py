import pytest
from decimal import Decimal
from services.deal.deal_allocation_srv import DealAllocationService

@pytest.fixture
def deal_srv():
    return DealAllocationService()

def test_deal_allocation_oversubscribed(deal_srv):
    capacity = Decimal('5000000')
    commitments = [
        {"client_id": "SFO_1", "amount": Decimal('4000000'), "tier": "SFO"},
        {"client_id": "UHNW_1", "amount": Decimal('2000000'), "tier": "UHNW"}
    ]
    # SFO gets 4M. UHNW gets remaining 1M (of 2M requested).
    results = deal_srv.allocate_oversubscribed_deal(capacity, commitments)
    
    # Sort results by allocated amount to check
    results = sorted(results, key=lambda x: x['allocated'], reverse=True)
    assert results[0]['allocated'] == Decimal('4000000.00')
    assert results[1]['allocated'] == Decimal('1000000.00')
    assert results[1]['status'] == "CONFIRMED" # Partially confirmed
