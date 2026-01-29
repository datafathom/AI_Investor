"""
Runner for Searcher Agent CLI commands.
"""
from agents.searcher_agent import SearcherAgent

def run_test_searcher():
    """
    Run Searcher Agent market scan and print results.
    """
    print("=== Searcher Agent: Market Scan ===")
    agent = SearcherAgent()
    result = agent.process_event({"type": "SCAN_TRIGGER"})
    
    print(f"\nFound {result['count']} opportunities:")
    print("-" * 60)
    
    for opp in result['opportunities']:
        print(f"SYMBOL: {opp['symbol']:<8} | PATTERN: {opp['pattern']:<20} | CONFIDENCE: {opp['confidence']:<4} | ACTION: {opp['action']:<4} | SCORE: {opp['score']:.1f}")
        
    print("-" * 60)
    print("✅ Scan Complete.")
