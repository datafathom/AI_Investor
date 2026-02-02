import logging
from decimal import Decimal
from services.deal.deal_allocation_srv import DealAllocationService
from services.deal.waitlist_manager import WaitlistManager

logger = logging.getLogger(__name__)

def allocate(deal_id: str, capacity: float):
    """
    CLI Handler for running the allocation algorithm.
    """
    service = DealAllocationService()
    # Mocking commitments for the demo
    commitments = [
        {"user": "James III", "amount": Decimal('5000000'), "tier": "SFO"},
        {"user": "Sara", "amount": Decimal('3000000'), "tier": "UHNW"},
        {"user": "Retail-1", "amount": Decimal('3000000'), "tier": "HNW"},
    ]
    
    res = service.allocate_oversubscribed_deal(Decimal(str(capacity)), commitments)
    
    print("\n" + "="*50)
    print(f"          DEAL ALLOCATION: {deal_id}")
    print(f"          CAPACITY: ${capacity:,.2f}")
    print("="*50)
    for a in res:
        print(f"- {a['user']} ({a['tier']}): Requested ${a['amount']:,.0f} -> Allocated ${a['allocated']:,.0f} [{a['status']}]")
    print("="*50 + "\n")

def show_waitlist():
    """
    CLI Handler for showing the deal waitlist.
    """
    print("\n" + "="*50)
    print("          PRIVATE DEAL WAITLIST")
    print("="*50)
    print("1. Tech Unicorn Pre-IPO - 12 SFOs pending")
    print("2. Manhattan Multi-Family - 5 UHNW pending")
    print("="*50 + "\n")
