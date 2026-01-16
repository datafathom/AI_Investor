"""
==============================================================================
Unit Tests - BacktestAgent
==============================================================================
Tests the Backtest Agent's historical simulation and k-factor validation.
==============================================================================
"""
import pytest

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.backtest_agent import BacktestAgent, BacktestResult


class TestBacktestAgent:
    """Test suite for BacktestAgent strategy validation."""
    
    def test_initialization(self) -> None:
        """Test BacktestAgent initializes correctly."""
        agent = BacktestAgent()
        
        assert agent.name == 'BacktestAgent'
        assert agent.db_connection is None
        assert agent.last_result is None
    
    def test_run_backtest(self) -> None:
        """Test that running a backtest returns results."""
        agent = BacktestAgent()
        
        result = agent.process_event({
            'type': 'RUN_BACKTEST',
            'strategy': 'IRON_CONDOR',
            'start_date': '2022-01-01',
            'end_date': '2023-12-31',
            'initial_capital': 100000
        })
        
        assert result['action'] == 'BACKTEST_COMPLETE'
        assert result['strategy'] == 'IRON_CONDOR'
        assert 'total_return' in result['result']
        assert 'k_factor' in result['result']
    
    def test_backtest_stores_result(self) -> None:
        """Test that backtest results are stored for retrieval."""
        agent = BacktestAgent()
        
        agent.process_event({
            'type': 'RUN_BACKTEST',
            'strategy': 'DEFAULT'
        })
        
        assert agent.last_result is not None
        assert isinstance(agent.last_result, BacktestResult)
    
    def test_get_results(self) -> None:
        """Test retrieving last backtest results."""
        agent = BacktestAgent()
        
        # First run a backtest
        agent.process_event({'type': 'RUN_BACKTEST'})
        
        # Then retrieve results
        result = agent.process_event({'type': 'GET_RESULTS'})
        
        assert result['action'] == 'RESULTS'
        assert 'sharpe_ratio' in result['result']
    
    def test_get_results_no_backtest(self) -> None:
        """Test that getting results without running backtest returns appropriate message."""
        agent = BacktestAgent()
        
        result = agent.process_event({'type': 'GET_RESULTS'})
        
        assert result['action'] == 'NO_RESULTS'
    
    def test_load_historical_data(self) -> None:
        """Test loading historical data."""
        agent = BacktestAgent()
        
        result = agent.process_event({
            'type': 'LOAD_DATA',
            'symbol': 'SPY',
            'start_date': '2024-01-01',
            'end_date': '2024-01-31'
        })
        
        assert result['action'] == 'DATA_LOADED'
        assert result['symbol'] == 'SPY'
        assert result['records'] > 0
    
    def test_k_factor_calculation(self) -> None:
        """Test k-factor is calculated correctly."""
        agent = BacktestAgent()
        
        result = agent.process_event({'type': 'RUN_BACKTEST'})
        
        k_factor = result['result']['k_factor']
        # Mock returns 15% so k = 1.15
        assert k_factor > 1.0
    
    def test_validate_k_threshold_passes(self) -> None:
        """Test k-threshold validation when k > threshold."""
        agent = BacktestAgent()
        
        agent.process_event({'type': 'RUN_BACKTEST'})
        validation = agent.validate_k_threshold(threshold=1.05)
        
        assert validation['valid'] is True
        assert validation['recommendation'] == 'DEPLOY'
    
    def test_validate_k_threshold_fails(self) -> None:
        """Test k-threshold validation when k < threshold."""
        agent = BacktestAgent()
        
        agent.process_event({'type': 'RUN_BACKTEST'})
        # Set an impossibly high threshold
        validation = agent.validate_k_threshold(threshold=2.0)
        
        assert validation['valid'] is False
        assert validation['recommendation'] == 'REJECT'
    
    def test_validate_k_no_results(self) -> None:
        """Test k-threshold validation without prior backtest."""
        agent = BacktestAgent()
        
        validation = agent.validate_k_threshold()
        
        assert validation['valid'] is False
        assert 'No backtest' in validation['reason']
    
    def test_sharpe_ratio_in_results(self) -> None:
        """Test that Sharpe ratio is included in results."""
        agent = BacktestAgent()
        
        result = agent.process_event({'type': 'RUN_BACKTEST'})
        
        assert result['result']['sharpe_ratio'] > 0
    
    def test_max_drawdown_in_results(self) -> None:
        """Test that max drawdown is included in results."""
        agent = BacktestAgent()
        
        result = agent.process_event({'type': 'RUN_BACKTEST'})
        
        assert 'max_drawdown' in result['result']
        assert 0 <= result['result']['max_drawdown'] <= 1
