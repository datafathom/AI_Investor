import logging
from services.external.masterworks_adapter import MasterworksAdapter
from services.tax.k1_tracker import K1Tracker

logger = logging.getLogger(__name__)

def update_prices():
    """
    CLI Handler for fetching external valuations for alts.
    """
    adapter = MasterworksAdapter()
    res = adapter.fetch_artwork_value("Basquiat", "piece-001")
    
    print("\n" + "="*50)
    print("          ALTERNATIVE ASSET REVALUATION")
    print("="*50)
    print(f"Asset:          {res['artist']} ({res['piece_id']})")
    print(f"Source:         {res['source']}")
    print("-" * 50)
    print(f"MARKET VALUE:   ${res['market_value_usd']:,.2f}")
    print(f"Appraisal Date: {res['last_appraisal_date']}")
    print("="*50 + "\n")

def list_k1s():
    """
    CLI Handler for listing missing K-1 tax forms.
    """
    tracker = K1Tracker()
    funds = ["Sequoia Cap X", "Blackstone RE VII", "Andreessen Bio III"]
    
    print("\n" + "="*50)
    print("          K-1 TAX DOCUMENT STATUS")
    print("="*50)
    for f in funds:
        res = tracker.check_k1_status(f, 2025)
        indicator = " [!]" if res['status'] == "DELINQUENT" else " [x]"
        print(f"{indicator} {res['fund_name']}: {res['status']} (Exp: {res['expected_delivery']})")
    print("="*50 + "\n")
