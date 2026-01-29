"""
'Guru' ETF Basket Generator.
Creates portfolios based on multi-manager consensus.
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GuruBasketGen:
    """Generates 'Consensus' baskets from smart money filings."""
    
    def generate_billionaire_basket(self, filings_db: List[Dict[str, Any]]) -> List[str]:
        # Count occurrences of tickers across top funds
        counts = {}
        for f in filings_db:
            ticker = f['ticker']
            counts[ticker] = counts.get(ticker, 0) + 1
            
        # Top 10 consensus picks
        sorted_consensus = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return [t[0] for t in sorted_consensus[:10]]
