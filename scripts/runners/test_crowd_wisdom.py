"""
scripts/runners/test_crowd_wisdom.py
Purpose: Test Google Trends Crowd Wisdom Logic.
"""

from services.data.google_trends import GoogleTrendsService

def run_test_crowd_wisdom(**kwargs):
    """
    Test the Crowd Wisdom Engine.
    Checks for Fear/Greed keywords.
    """
    print("Testing Crowd Wisdom Engine (Google Trends)...")
    
    service = GoogleTrendsService()
    
    # 1. Test Fear Queries
    fear_keywords = ["margin call", "AMZN debt"]
    print(f"\nAnalyzing Fear Keywords: {fear_keywords}")
    fear_results = service.get_trend_score(fear_keywords)
    
    for kw, stats in fear_results.items():
        print(f"Keyword: {kw}")
        print(f"  Score: {stats['current_score']}")
        print(f"  Z-Score: {stats['z_score']}")
        print(f"  Spike Detected: {stats['is_spike']}")
        
        if stats['is_spike']:
            print("  ALERT: Significant deviation in FEAR sentiment detected!")

    # 2. Test Greed Queries
    greed_keywords = ["buy NVDA", "stock prediction"]
    print(f"\nAnalyzing Greed Keywords: {greed_keywords}")
    greed_results = service.get_trend_score(greed_keywords)
    
    for kw, stats in greed_results.items():
        print(f"Keyword: {kw}")
        print(f"  Score: {stats['current_score']}")
        print(f"  Z-Score: {stats['z_score']}")
        
    return True
