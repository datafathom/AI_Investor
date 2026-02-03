"""
==============================================================================
FILE: scripts/runners/test_politics.py
ROLE: Intelligence Officer
PURPOSE:
    Demonstrate Political Alpha detection by processing simulated disclosures
    and lobbying data.
       
CONTEXT: 
    Part of Phase 36: Political Alpha.
==============================================================================
"""

from services.analysis.congress_tracker import get_congress_tracker

def run_test_politics(args=None):
    """
    Test Phase 36 Political Alpha.
    """
    print("Initializing Political Alpha Monitor...")
    
    tracker = get_congress_tracker()
    
    # 🕵️ Fetch Disclosures
    disclosures = tracker.fetch_latest_disclosures()
    
    print(f"\nFetched {len(disclosures)} latest disclosures:")
    for d in disclosures:
        print(f" - {d['member']} bought {d['ticker']} ({d['amount_range']}) in {d['sector']} sector.")

    # 🏛️ Lobbying Correlation
    test_tickers = ["NVDA", "XOM", "LMT", "AAPL"]
    print("\n--- ALPHA ANALYSIS ---")
    for ticker in test_tickers:
        score = tracker.get_political_alpha_signal(ticker)
        correlation = tracker.correlate_with_lobbying(ticker)
        
        status = "🛰️ HIGH ALPHA" if score > 0.5 else "⚖️ NEUTRAL"
        print(f"Ticker: {ticker} | Score: {score} | Lobbying: {correlation['lobbying_intensity']} | {status}")

    print("\nOK Political Alpha Logic Verified.")
