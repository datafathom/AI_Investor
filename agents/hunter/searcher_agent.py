"""
==============================================================================
FILE: agents/searcher_agent.py
ROLE: Opportunity Scanner (The Scout)
PURPOSE: Traverses the Neo4j graph to find high-liquidity paths and correlations.
USAGE: Triggered by SCAN_TRIGGER events to output trading pairs.
INPUT/OUTPUT:
    - Input: Dict (Scan params: sector, min_liquidity)
    - Output: List[Dict] (Identified opportunities: symbols, correlation)
==============================================================================
"""
from typing import Any, Dict, List, Optional
import logging

from agents.base_agent import BaseAgent
from services.market_scanner import MarketScannerService
from analysis.pattern_recognition import PatternRecognition
from analysis.opportunity_scorer import OpportunityScorer

logger = logging.getLogger(__name__)


class SearcherAgent(BaseAgent):
    """
    The Searcher Agent - Scout of the Ant Colony.
    
    Traverses the market to identify trading opportunities based on 
    logic-based patterns and correlations.
    """
    
    def __init__(self, neo4j_driver: Optional[Any] = None) -> None:
        """
        Initialize the Searcher Agent.
        
        Args:
            neo4j_driver: Optional Neo4j driver for graph queries.
        """
        super().__init__(name='SearcherAgent')
        self.neo4j_driver = neo4j_driver
        self.scan_results: List[Dict[str, Any]] = []
        self.market_scanner = MarketScannerService()
    
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process scan trigger events.
        """
        event_type = event.get('type')
        
        if event_type == 'SCAN_TRIGGER':
            return self._execute_scan(event)
        
        return None
    
    def _execute_scan(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a full market scan for opportunities.
        """
        logger.info("Executing market scan...")
        
        # 1. Scan Market
        market_data = self.market_scanner.scan_major_pairs()
        
        # 2. Identify Patterns
        raw_patterns = PatternRecognition.identify_patterns(market_data)
        
        # 3. Score Opportunities
        scored_opportunities = []
        for p in raw_patterns:
            score = OpportunityScorer.score_opportunity(p)
            p['score'] = score
            if score > 50: # Filter low quality
                scored_opportunities.append(p)
                
        self.scan_results = scored_opportunities
        
        return {
            'action': 'SCAN_COMPLETE',
            'opportunities': scored_opportunities,
            'count': len(scored_opportunities)
        }
    
    def get_last_scan_results(self) -> List[Dict[str, Any]]:
        """Return the most recent scan results."""
        return self.scan_results

