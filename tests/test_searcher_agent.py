"""
==============================================================================
Unit Tests - SearcherAgent
==============================================================================
Tests the Searcher Agent's Neo4j graph scanning and opportunity detection.
==============================================================================
"""
import pytest

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.searcher_agent import SearcherAgent


class TestSearcherAgent:
    """Test suite for SearcherAgent Neo4j scanning."""
    
    def test_initialization(self) -> None:
        """Test SearcherAgent initializes correctly."""
        agent = SearcherAgent()
        
        assert agent.name == 'SearcherAgent'
        assert agent.neo4j_driver is None
        assert agent.scan_results == []
    
    def test_scan_trigger_executes_scan(self) -> None:
        """Test that SCAN_TRIGGER event executes a scan."""
        agent = SearcherAgent()
        
        result = agent.process_event({
            'type': 'SCAN_TRIGGER',
            'sector': 'TECH',
            'min_liquidity': 5000000
        })
        
        assert result['action'] == 'SCAN_COMPLETE'
        assert 'opportunities' in result
        assert result['count'] > 0
    
    def test_scan_results_stored(self) -> None:
        """Test that scan results are stored for retrieval."""
        agent = SearcherAgent()
        
        agent.process_event({
            'type': 'SCAN_TRIGGER',
            'sector': 'ALL'
        })
        
        results = agent.get_last_scan_results()
        assert len(results) > 0
    
    def test_mock_opportunities_structure(self) -> None:
        """Test that mock opportunities have correct structure."""
        agent = SearcherAgent()
        
        result = agent.process_event({'type': 'SCAN_TRIGGER'})
        
        for opp in result['opportunities']:
            assert 'asset_a' in opp
            assert 'asset_b' in opp
            assert 'correlation' in opp
            assert 'liquidity' in opp
            assert 'opportunity_type' in opp
    
    def test_correlation_check(self) -> None:
        """Test correlation check between assets."""
        agent = SearcherAgent()
        
        result = agent.process_event({
            'type': 'CORRELATION_CHECK',
            'asset_a': 'SPY',
            'asset_b': 'QQQ'
        })
        
        assert result['action'] == 'CORRELATION_RESULT'
        assert result['asset_a'] == 'SPY'
        assert result['asset_b'] == 'QQQ'
        assert 'correlation' in result
    
    def test_unknown_event_returns_none(self) -> None:
        """Test that unknown events return None."""
        agent = SearcherAgent()
        
        result = agent.process_event({'type': 'UNKNOWN_EVENT'})
        
        assert result is None
    
    def test_health_check(self) -> None:
        """Test health check returns correct format."""
        agent = SearcherAgent()
        agent.start()
        
        health = agent.health_check()
        
        assert health['agent'] == 'SearcherAgent'
        assert health['active'] is True
