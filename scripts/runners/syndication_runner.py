import logging
from decimal import Decimal
from services.real_estate.syndication_service import SyndicationService

logger = logging.getLogger(__name__)

def list_syndications():
    """
    CLI Handler for listing open syndication deals.
    """
    # Mock some data for demonstration
    print("\n" + "="*50)
    print("          OPEN SYNDICATION DEALS")
    print("="*50)
    print("ID: RE-SYND-01 | Name: Austin Multi-Family | Cap Rate: 6.2%")
    print("Sponsor: XYZ Equities | Target: $5,000,000")
    print("-" * 50)
    print("ID: CO-SYND-42 | Name: Denver Data Center | Cap Rate: 7.5%")
    print("Sponsor: CloudVault | Target: $12,000,000")
    print("="*50 + "\n")

def commit_deal(deal_id: str, amount: str):
    """
    CLI Handler for soft commitments to syndications.
    """
    try:
        service = SyndicationService()
        amt = Decimal(amount.replace(',', ''))
        
        # In real, would use context.user_id
        investor_id = "USER-DEFAULT"
        
        success = service.soft_circle(deal_id, investor_id, amt)
        if success:
            status = service.get_raise_status(deal_id, Decimal('10000000')) # Assume 10M target
            print("\n" + "="*50)
            print("          SYNDICATION SOFT COMMITMENT")
            print("="*50)
            print(f"Deal ID:      {deal_id}")
            print(f"Amount:       ${amt:,.2f}")
            print(f"New Progress: {status['pct_complete']}% of target")
            print("-" * 50)
            print("STATUS: SOFT_CIRCLE_CONFIRMED")
            print("="*50 + "\n")
    except Exception as e:
        print(f"Error making commitment: {e}")
