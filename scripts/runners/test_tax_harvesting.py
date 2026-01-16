
from services.strategy.tax_harvester import get_tax_harvester
from datetime import datetime, timedelta

def run_test_harvesting(args=None):
    """
    Test Phase 19 Tax Harvesting.
    """
    print("Testing Tax Harvester & Wash Sale Logic...")
    harvester = get_tax_harvester()
    
    # 1. Test Harvesting Logic
    print("\n--- Harvesting Scan ---")
    positions = [
        {'symbol': 'AAPL', 'quantity': 10, 'cost_basis_per_share': 150.0}, # Val $1500
        {'symbol': 'MSFT', 'quantity': 10, 'cost_basis_per_share': 300.0}, # Val $3000
        {'symbol': 'TSLA', 'quantity': 10, 'cost_basis_per_share': 200.0}  # Val $2000
    ]
    
    prices = {
        'AAPL': 160.0, # Gain +$100
        'MSFT': 270.0, # Loss -$300 (-10%) -> SHOULD HARVEST (Threshold -5%)
        'TSLA': 198.0  # Loss -$20 (-1%)   -> NO HARVEST
    }
    
    recs = harvester.scan_harvestable_losses(positions, prices)
    for rec in recs:
        print(f"RECOMMENDATION: Sell {rec['symbol']} ({rec['reason']})")
        
    if any(r['symbol'] == 'MSFT' for r in recs) and not any(r['symbol'] == 'TSLA' for r in recs):
        print("✅ Harvesting Logic Verified: Identifies significant losses only.")
    else:
        print("❌ Harvesting Logic Failed.")

    # 2. Test Wash Sale Logic
    print("\n--- Wash Sale Check ---")
    today = datetime.now()
    history = [
        {'symbol': 'GOOG', 'action': 'SELL', 'pnl': -100.0, 'date': (today - timedelta(days=15)).isoformat()}
    ]
    
    is_restricted = harvester.check_wash_sale_restriction('GOOG', history)
    if is_restricted:
        print(f"✅ Wash Sale Verified: GOOG is restricted (Sold 15 days ago for loss).")
    else:
        print(f"❌ Wash Sale Failed: GOOG should be restricted.")
        
    is_safe = harvester.check_wash_sale_restriction('AMZN', history)
    if not is_safe:
        print(f"✅ Wash Sale Verified: AMZN is safe.")
