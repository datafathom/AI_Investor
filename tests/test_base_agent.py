"""
==============================================================================
Unit Tests - BaseAgent
==============================================================================
Tests the abstract BaseAgent class functionality.
==============================================================================
"""
import pytest
from typing import Any, Dict, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent


class ConcreteAgent(BaseAgent):
    """Concrete implementation for testing abstract BaseAgent."""
    
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {'processed': True, 'event': event}


class TestBaseAgent:
    """Test suite for BaseAgent abstract class."""
    
    def test_agent_initialization(self) -> None:
        """Test that agent initializes with correct name and inactive state."""
        agent = ConcreteAgent(name='TestAgent')
        
        assert agent.name == 'TestAgent'
        assert agent.is_active is False
    
    def test_agent_start(self) -> None:
        """Test that start() activates the agent."""
        agent = ConcreteAgent(name='TestAgent')
        agent.start()
        
        assert agent.is_active is True
    
    def test_agent_stop(self) -> None:
        """Test that stop() deactivates the agent."""
        agent = ConcreteAgent(name='TestAgent')
        agent.start()
        agent.stop()
        
        assert agent.is_active is False
    
    def test_health_check_inactive(self) -> None:
        """Test health check returns inactive status when agent is stopped."""
        agent = ConcreteAgent(name='TestAgent')
        health = agent.health_check()
        
        assert health['agent'] == 'TestAgent'
        assert health['active'] is False
        assert health['status'] == 'inactive'
    
    def test_health_check_active(self) -> None:
        """Test health check returns healthy status when agent is active."""
        agent = ConcreteAgent(name='TestAgent')
        agent.start()
        health = agent.health_check()
        
        assert health['agent'] == 'TestAgent'
        assert health['active'] is True
        assert health['status'] == 'healthy'
    
    def test_process_event(self) -> None:
        """Test that concrete implementation processes events."""
        agent = ConcreteAgent(name='TestAgent')
        result = agent.process_event({'type': 'TEST'})
        
        assert result['processed'] is True
        assert result['event']['type'] == 'TEST'
