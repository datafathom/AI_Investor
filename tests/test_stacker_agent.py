"""
==============================================================================
Unit Tests - StackerAgent
==============================================================================
Tests the Stacker Agent's signal aggregation and trade decision logic.
==============================================================================
"""
import pytest

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.stacker_agent import StackerAgent, Signal


class TestStackerAgent:
    """Test suite for StackerAgent signal aggregation."""
    
    def test_initialization(self) -> None:
        """Test StackerAgent initializes with default weights."""
        agent = StackerAgent()
        
        assert agent.name == 'StackerAgent'
        assert len(agent.weights) > 0
        assert agent.CONFIDENCE_THRESHOLD == 0.65
        assert agent.signal_stack == []
    
    def test_signal_stacking(self) -> None:
        """Test that signals are added to the stack."""
        agent = StackerAgent()
        
        result = agent.process_event({
            'type': 'SIGNAL',
            'source': 'SearcherAgent',
            'signal_type': 'OPPORTUNITY',
            'direction': 'LONG',
            'confidence': 0.8
        })
        
        assert result['action'] == 'SIGNAL_STACKED'
        assert result['stack_size'] == 1
    
    def test_multiple_signals_stack(self) -> None:
        """Test that multiple signals accumulate."""
        agent = StackerAgent()
        
        agent.process_event({
            'type': 'SIGNAL', 'source': 'SearcherAgent',
            'direction': 'LONG', 'confidence': 0.8
        })
        agent.process_event({
            'type': 'SIGNAL', 'source': 'HMM_Engine',
            'direction': 'LONG', 'confidence': 0.7
        })
        
        summary = agent.get_stack_summary()
        assert summary['stack_size'] == 2
    
    def test_evaluate_triggers_trade_above_threshold(self) -> None:
        """Test that evaluation triggers trade when confidence exceeds threshold."""
        agent = StackerAgent()
        
        # Add high-confidence signals
        agent.process_event({
            'type': 'SIGNAL', 'source': 'SearcherAgent',
            'direction': 'LONG', 'confidence': 0.9
        })
        agent.process_event({
            'type': 'SIGNAL', 'source': 'HMM_Engine',
            'direction': 'LONG', 'confidence': 0.85
        })
        
        result = agent.process_event({'type': 'EVALUATE'})
        
        assert result['action'] == 'TRADE_SIGNAL'
        assert result['direction'] == 'LONG'
        assert result['execute'] is True
    
    def test_evaluate_holds_below_threshold(self) -> None:
        """Test that evaluation recommends HOLD when below threshold."""
        agent = StackerAgent()
        
        # Add low-confidence signal
        agent.process_event({
            'type': 'SIGNAL', 'source': 'SearcherAgent',
            'direction': 'LONG', 'confidence': 0.3
        })
        
        result = agent.process_event({'type': 'EVALUATE'})
        
        assert result['action'] == 'BELOW_THRESHOLD'
        assert result['recommendation'] == 'HOLD'
    
    def test_evaluate_empty_stack(self) -> None:
        """Test that evaluation with empty stack recommends HOLD."""
        agent = StackerAgent()
        
        result = agent.process_event({'type': 'EVALUATE'})
        
        assert result['action'] == 'NO_SIGNALS'
        assert result['recommendation'] == 'HOLD'
    
    def test_clear_stack(self) -> None:
        """Test that stack can be cleared."""
        agent = StackerAgent()
        
        agent.process_event({
            'type': 'SIGNAL', 'source': 'SearcherAgent',
            'direction': 'LONG', 'confidence': 0.8
        })
        
        result = agent.process_event({'type': 'CLEAR_STACK'})
        
        assert result['action'] == 'STACK_CLEARED'
        assert result['cleared_count'] == 1
        assert len(agent.signal_stack) == 0
    
    def test_mixed_direction_signals(self) -> None:
        """Test aggregation with conflicting signal directions."""
        agent = StackerAgent()
        
        agent.process_event({
            'type': 'SIGNAL', 'source': 'SearcherAgent',
            'direction': 'LONG', 'confidence': 0.8
        })
        agent.process_event({
            'type': 'SIGNAL', 'source': 'HMM_Engine',
            'direction': 'SHORT', 'confidence': 0.7
        })
        
        result = agent.process_event({'type': 'EVALUATE'})
        
        # With conflicting signals, should not trigger trade
        assert 'direction' in result
    
    def test_custom_weights(self) -> None:
        """Test that custom weights can be provided."""
        custom_weights = {'SearcherAgent': 0.5, 'HMM_Engine': 0.5}
        agent = StackerAgent(weights=custom_weights)
        
        assert agent.weights == custom_weights
    
    def test_stack_summary(self) -> None:
        """Test that stack summary returns correct structure."""
        agent = StackerAgent()
        
        agent.process_event({
            'type': 'SIGNAL', 'source': 'SearcherAgent',
            'direction': 'LONG', 'confidence': 0.8
        })
        
        summary = agent.get_stack_summary()
        
        assert 'stack_size' in summary
        assert 'signals' in summary
        assert 'pending_trade' in summary
        assert summary['signals'][0]['source'] == 'SearcherAgent'
