import logging
from uuid import uuid4
from services.mfo.concierge_srv import ConciergeService
from services.compliance.fee_tier_check import FeeTierValidator

logger = logging.getLogger(__name__)

def create_request(text: str):
    """
    CLI Handler for creating concierge tickets.
    """
    service = ConciergeService()
    family_id = uuid4()
    res = service.create_lifestyle_request(family_id, "LIFESTYLE", text)
    
    print("\n" + "="*50)
    print("          MFO CONCIERGE TICKET CREATED")
    print("="*50)
    print(f"Ticket ID:      {res['ticket_id']}")
    print(f"Priority:       {res['priority']}")
    print(f"Assigned To:    {res['assigned_team']}")
    print("-" * 50)
    print(f"Request:        {text}")
    print("="*50 + "\n")

def check_pricing():
    """
    CLI Handler for institutional fee tier verification.
    """
    validator = FeeTierValidator()
    # Mock portfolios
    funds = [
        {"id": "VTSAX", "current": 4, "retail": 14, "inst": 4},
        {"id": "SPY", "current": 9, "retail": 9, "inst": 3},
    ]
    
    print("\n" + "="*50)
    print("          INSTITUTIONAL PRICING AUDIT")
    print("="*50)
    for f in funds:
        res = validator.audit_fee_tier(f['id'], f['current'], f['retail'], f['inst'])
        status = " [x]" if res['status'] == "VALID_INSTITUTIONAL" else " [!]"
        print(f"{status} {res['fund_id']}: {res['status']} (Leakage: {res['leakage_bps']} bps)")
    print("="*50 + "\n")
