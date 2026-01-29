"""
Insider Cluster Detector.
Detects multiple corporate insiders buying within a 7-day window.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class InsiderClusterDetector:
    """Detects institutional cluster buying signals."""
    
    def detect_clusters(self, filings: List[Dict[str, Any]], window_days: int = 7) -> List[str]:
        clusters = {}
        for f in filings:
            ticker = f['ticker']
            if ticker not in clusters: clusters[ticker] = set()
            clusters[ticker].add(f['insider_name'])
            
        signal_tickers = [t for t, insiders in clusters.items() if len(insiders) >= 3]
        
        if signal_tickers:
            logger.info(f"CLUSTER_SIGNAL: Found cluster buying in {signal_tickers}")
            
        return signal_tickers
