"""
==============================================================================
Unit Tests - ProtectorAgent
==============================================================================
Tests the Protector Agent's safety mechanisms including kill switch,
VIX monitoring, and max drawdown halt.
==============================================================================
"""
import pytest
import os
from unittest.mock import patch

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.protector_agent import ProtectorAgent


class TestProtectorAgent:
    """Test suite for ProtectorAgent safety mechanisms."""
    
    def test_initialization(self) -> None:
        """Test ProtectorAgent initializes with correct defaults."""
        agent = ProtectorAgent()
        
        assert agent.name == 'ProtectorAgent'
        assert agent.max_drawdown_threshold == 0.02
        assert agent.bunker_mode is False
    
    def test_kill_switch_halts_all(self) -> None:
        """Test that STOP_ALL_TRADING env var triggers halt."""
        agent = ProtectorAgent()
        
        with patch.dict(os.environ, {'STOP_ALL_TRADING': 'TRUE'}):
            result = agent.process_event({'type': 'VIX_UPDATE', 'vix_level': 15})
        
        assert result['action'] == 'HALT_ALL'
        assert 'Kill switch' in result['reason']
    
    def test_vix_spike_triggers_bunker_mode(self) -> None:
        """Test that high VIX triggers bunker mode."""
        agent = ProtectorAgent()
        
        with patch.dict(os.environ, {'STOP_ALL_TRADING': 'FALSE'}):
            result = agent.process_event({'type': 'VIX_UPDATE', 'vix_level': 35})
        
        assert result['action'] == 'ENTER_BUNKER_MODE'
        assert agent.bunker_mode is True
    
    def test_normal_vix_no_action(self) -> None:
        """Test that normal VIX levels don't trigger any action."""
        agent = ProtectorAgent()
        
        with patch.dict(os.environ, {'STOP_ALL_TRADING': 'FALSE'}):
            result = agent.process_event({'type': 'VIX_UPDATE', 'vix_level': 15})
        
        assert result is None
        assert agent.bunker_mode is False
    
    def test_max_drawdown_halt(self) -> None:
        """Test that exceeding max drawdown triggers halt."""
        agent = ProtectorAgent()
        
        with patch.dict(os.environ, {'STOP_ALL_TRADING': 'FALSE'}):
            result = agent.process_event({
                'type': 'PORTFOLIO_UPDATE',
                'current_value': 97000,
                'set_point': 100000
            })
        
        assert result['action'] == 'MAX_DRAWDOWN_HALT'
        assert result['drawdown'] == 0.03  # 3% drawdown
    
    def test_within_drawdown_threshold(self) -> None:
        """Test that drawdown within threshold doesn't trigger halt."""
        agent = ProtectorAgent()
        
        with patch.dict(os.environ, {'STOP_ALL_TRADING': 'FALSE'}):
            result = agent.process_event({
                'type': 'PORTFOLIO_UPDATE',
                'current_value': 99000,
                'set_point': 100000
            })
        
        # 1% drawdown is within 2% threshold
        assert result is None
    
    def test_health_check(self) -> None:
        """Test that health check returns correct status."""
        agent = ProtectorAgent()
        agent.start()
        
        health = agent.health_check()
        
        assert health['agent'] == 'ProtectorAgent'
        assert health['active'] is True
