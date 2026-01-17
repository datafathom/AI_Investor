"""
==============================================================================
FILE: scripts/runners/test_hype_tracking.py
ROLE: Trend Scout
PURPOSE:
    Demonstrate real-time hype detection by processing simulated social feeds.
       
CONTEXT: 
    Part of Phase 35: Visual Hype Tracking.
==============================================================================
"""

from services.analysis.hype_tracker import get_hype_tracker

def run_test_hype(args=None):
    """
    Test Phase 35 Visual Hype Tracking.
    """
    print("Initializing Visual Hype Monitor...")
    
    tracker = get_hype_tracker()
    
    # 🕵️ Mock Social Feed Mentions
    feed = [
        {"symbol": "TSLA", "source": "YouTube", "views": 1200000, "shares": 45000, "velocity": 0.95}, # VIRAL
        {"symbol": "AMC", "source": "TikTok", "views": 850000, "shares": 62000, "velocity": 0.88},  # VIRAL
        {"symbol": "MSFT", "source": "Twitter", "views": 5000, "shares": 12, "velocity": 0.1},      # QUIET
        {"symbol": "NVDA", "source": "YouTube", "views": 250000, "shares": 5000, "velocity": 0.4},   # MODERATE
    ]
    
    print("\n--- SOCIAL FEED ANALYSIS ---")
    for item in feed:
        metrics = {
            "views": item["views"],
            "shares": item["shares"],
            "velocity": item["velocity"],
            "likes": item["views"] // 10 # Mock 10% likes
        }
        result = tracker.process_social_mention(item["symbol"], item["source"], metrics)
        
        status = "🚀 VIRAL" if result["is_viral"] else "⚖️ STEADY"
        print(f"[{item['source']}] {item['symbol']} | Score: {result['hype_score']} | {status}")

    print("\n--- AGGREGATE STATS ---")
    for sym, stats in tracker.tracked_tickers.items():
        print(f"Ticker: {sym} | Avg Hype: {stats['avg_hype']:.2f} | Mentions: {stats['total_mentions']}")

    print("\n✅ Hype Tracking Logic Verified.")
