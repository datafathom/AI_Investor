"""
==============================================================================
Unit Tests - Kafka Consumer Infrastructure
==============================================================================
Tests the Kafka consumer base class and specialized consumers without
requiring a running Kafka cluster.
==============================================================================
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.kafka.consumer import (
    BaseConsumer, 
    ConsumerConfig, 
    VIXConsumer, 
    EquityConsumer,
    SignalConsumer
)


class TestConsumerConfig:
    """Test suite for ConsumerConfig dataclass."""
    
    def test_default_values(self) -> None:
        """Test ConsumerConfig has correct defaults."""
        config = ConsumerConfig(
            topics=['test.topic'],
            group_id='test-group'
        )
        
        assert config.auto_offset_reset == 'earliest'
        assert config.enable_auto_commit is True
        assert config.max_poll_interval_ms == 300000
    
    def test_custom_values(self) -> None:
        """Test ConsumerConfig with custom values."""
        config = ConsumerConfig(
            topics=['a', 'b'],
            group_id='custom',
            auto_offset_reset='latest',
            enable_auto_commit=False
        )
        
        assert config.topics == ['a', 'b']
        assert config.auto_offset_reset == 'latest'
        assert config.enable_auto_commit is False


class ConcreteConsumer(BaseConsumer):
    """Concrete implementation for testing."""
    
    def __init__(self, config, bootstrap_servers=None):
        super().__init__(config, bootstrap_servers)
        self.processed_messages = []
    
    def process_message(self, message):
        self.processed_messages.append(message)


class TestBaseConsumer:
    """Test suite for BaseConsumer abstract class."""
    
    def test_initialization(self) -> None:
        """Test BaseConsumer initializes correctly."""
        config = ConsumerConfig(topics=['test'], group_id='test-group')
        consumer = ConcreteConsumer(config)
        
        assert consumer.config == config
        assert consumer.is_running is False
        assert consumer._error_count == 0
    
    def test_default_bootstrap_servers(self) -> None:
        """Test default bootstrap servers from env or fallback."""
        config = ConsumerConfig(topics=['test'], group_id='test')
        
        with patch.dict(os.environ, {}, clear=True):
            consumer = ConcreteConsumer(config)
            assert consumer.bootstrap_servers == 'localhost:9092'
    
    def test_env_bootstrap_servers(self) -> None:
        """Test bootstrap servers from environment variable."""
        config = ConsumerConfig(topics=['test'], group_id='test')
        
        with patch.dict(os.environ, {'KAFKA_BOOTSTRAP_SERVERS': 'kafka:29092'}):
            consumer = ConcreteConsumer(config)
            assert consumer.bootstrap_servers == 'kafka:29092'
    
    def test_deserialize_valid_json(self) -> None:
        """Test deserialize with valid JSON."""
        config = ConsumerConfig(topics=['test'], group_id='test')
        consumer = ConcreteConsumer(config)
        
        result = consumer.deserialize(b'{"key": "value", "num": 42}')
        
        assert result == {'key': 'value', 'num': 42}
    
    def test_deserialize_invalid_json(self) -> None:
        """Test deserialize with invalid JSON returns None."""
        config = ConsumerConfig(topics=['test'], group_id='test')
        consumer = ConcreteConsumer(config)
        
        result = consumer.deserialize(b'not valid json')
        
        assert result is None
    
    def test_health_check_initial(self) -> None:
        """Test health check returns correct initial state."""
        config = ConsumerConfig(topics=['test.topic'], group_id='test-group')
        consumer = ConcreteConsumer(config)
        
        health = consumer.health_check()
        
        assert health['is_running'] is False
        assert health['topics'] == ['test.topic']
        assert health['group_id'] == 'test-group'
        assert health['error_count'] == 0
        assert health['healthy'] is False  # Not running
    
    def test_process_message_implementation(self) -> None:
        """Test that process_message stores messages."""
        config = ConsumerConfig(topics=['test'], group_id='test')
        consumer = ConcreteConsumer(config)
        
        consumer.process_message({'data': 'test1'})
        consumer.process_message({'data': 'test2'})
        
        assert len(consumer.processed_messages) == 2
        assert consumer.processed_messages[0] == {'data': 'test1'}


class TestVIXConsumer:
    """Test suite for VIXConsumer."""
    
    def test_initialization(self) -> None:
        """Test VIXConsumer initializes with correct topic."""
        consumer = VIXConsumer()
        
        assert consumer.config.topics == ['market.vix']
        assert consumer.config.group_id == 'ai-investor-vix-consumers'
        assert consumer.agent is None
    
    def test_initialization_with_agent(self) -> None:
        """Test VIXConsumer with agent injection."""
        mock_agent = Mock()
        consumer = VIXConsumer(agent=mock_agent)
        
        assert consumer.agent is mock_agent
    
    def test_process_message_forwards_to_agent(self) -> None:
        """Test that VIX messages are forwarded to agent."""
        mock_agent = Mock()
        mock_agent.process_event.return_value = {'action': 'NONE'}
        
        consumer = VIXConsumer(agent=mock_agent)
        consumer.process_message({'vix_level': 25.5, 'timestamp': '2024-01-01'})
        
        mock_agent.process_event.assert_called_once()
        call_args = mock_agent.process_event.call_args[0][0]
        assert call_args['type'] == 'VIX_UPDATE'
        assert call_args['vix_level'] == 25.5
    
    def test_process_message_no_agent(self) -> None:
        """Test process_message handles missing agent gracefully."""
        consumer = VIXConsumer(agent=None)
        
        # Should not raise
        consumer.process_message({'vix_level': 20.0})


class TestEquityConsumer:
    """Test suite for EquityConsumer."""
    
    def test_initialization(self) -> None:
        """Test EquityConsumer initializes with correct topic."""
        consumer = EquityConsumer()
        
        assert consumer.config.topics == ['market.equity']
        assert consumer.config.group_id == 'ai-investor-equity-consumers'
    
    def test_process_message_with_agent(self) -> None:
        """Test equity messages forwarded to agent."""
        mock_agent = Mock()
        consumer = EquityConsumer(agent=mock_agent)
        
        consumer.process_message({'symbol': 'SPY', 'price': 450.0})
        
        mock_agent.process_event.assert_called_once()
        call_args = mock_agent.process_event.call_args[0][0]
        assert call_args['type'] == 'EQUITY_UPDATE'
        assert call_args['symbol'] == 'SPY'


class TestSignalConsumer:
    """Test suite for SignalConsumer."""
    
    def test_initialization(self) -> None:
        """Test SignalConsumer initializes with correct topic."""
        consumer = SignalConsumer()
        
        assert consumer.config.topics == ['agent.signals']
        assert consumer.callback is None
    
    def test_process_message_with_callback(self) -> None:
        """Test signals trigger callback function."""
        callback = Mock()
        consumer = SignalConsumer(callback=callback)
        
        consumer.process_message({'signal_type': 'BUY', 'symbol': 'QQQ'})
        
        callback.assert_called_once_with({'signal_type': 'BUY', 'symbol': 'QQQ'})
