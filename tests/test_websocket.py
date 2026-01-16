"""
==============================================================================
Unit Tests - WebSocket Service
==============================================================================
Tests the WebSocket broadcaster without requiring a live SocketIO server.
==============================================================================
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.websocket import (
    WebSocketBroadcaster,
    _get_timestamp
)


class TestWebSocketBroadcaster:
    """Test suite for WebSocketBroadcaster."""
    
    def test_initialization_without_socketio(self) -> None:
        """Test broadcaster initializes without SocketIO."""
        broadcaster = WebSocketBroadcaster()
        
        assert broadcaster._sio is None
        assert broadcaster.sio is None  # No global socketio
    
    def test_initialization_with_socketio(self) -> None:
        """Test broadcaster initializes with provided SocketIO."""
        mock_sio = Mock()
        broadcaster = WebSocketBroadcaster(sio=mock_sio)
        
        assert broadcaster._sio is mock_sio
        assert broadcaster.sio is mock_sio
    
    def test_emit_without_socketio_returns_false(self) -> None:
        """Test _emit returns False when SocketIO unavailable."""
        broadcaster = WebSocketBroadcaster()
        
        result = broadcaster._emit('test_event', {'data': 'value'})
        
        assert result is False
    
    def test_broadcast_agent_status_with_socketio(self) -> None:
        """Test agent status broadcast calls emit correctly."""
        mock_sio = Mock()
        broadcaster = WebSocketBroadcaster(sio=mock_sio)
        
        result = broadcaster.broadcast_agent_status(
            agent_name='ProtectorAgent',
            status='healthy',
            is_active=True,
            details={'vix_level': 15.5}
        )
        
        assert result is True
        mock_sio.emit.assert_called_once()
        call_args = mock_sio.emit.call_args
        assert call_args[0][0] == 'agent_status'
        assert call_args[0][1]['agent'] == 'ProtectorAgent'
        assert call_args[0][1]['status'] == 'healthy'
        assert call_args[0][1]['active'] is True
    
    def test_broadcast_portfolio_update(self) -> None:
        """Test portfolio update broadcast."""
        mock_sio = Mock()
        broadcaster = WebSocketBroadcaster(sio=mock_sio)
        
        result = broadcaster.broadcast_portfolio_update(
            current_value=102500,
            set_point=100000,
            pnl_percent=2.5
        )
        
        assert result is True
        call_args = mock_sio.emit.call_args[0][1]
        assert call_args['value'] == 102500
        assert call_args['set_point'] == 100000
        assert call_args['gap'] == 2500
        assert call_args['gap_percent'] == 2.5
    
    def test_broadcast_alert(self) -> None:
        """Test alert broadcast."""
        mock_sio = Mock()
        broadcaster = WebSocketBroadcaster(sio=mock_sio)
        
        result = broadcaster.broadcast_alert(
            alert_type='VIX_SPIKE',
            severity='critical',
            message='VIX above 30 - entering bunker mode'
        )
        
        assert result is True
        call_args = mock_sio.emit.call_args[0][1]
        assert call_args['type'] == 'VIX_SPIKE'
        assert call_args['severity'] == 'critical'
        assert 'VIX above 30' in call_args['message']
    
    def test_broadcast_signal(self) -> None:
        """Test trading signal broadcast."""
        mock_sio = Mock()
        broadcaster = WebSocketBroadcaster(sio=mock_sio)
        
        result = broadcaster.broadcast_signal(
            signal_type='BUY',
            symbol='SPY',
            confidence=0.85,
            source_agent='SearcherAgent'
        )
        
        assert result is True
        call_args = mock_sio.emit.call_args[0][1]
        assert call_args['signal'] == 'BUY'
        assert call_args['symbol'] == 'SPY'
        assert call_args['confidence'] == 0.85
        assert call_args['source'] == 'SearcherAgent'
    
    def test_broadcast_uses_room(self) -> None:
        """Test broadcasts target correct rooms."""
        mock_sio = Mock()
        broadcaster = WebSocketBroadcaster(sio=mock_sio)
        
        broadcaster.broadcast_agent_status('TestAgent', 'ok', True)
        
        call_kwargs = mock_sio.emit.call_args[1]
        assert call_kwargs.get('room') == 'agents'
    
    def test_timestamp_format(self) -> None:
        """Test timestamp is ISO format with Z suffix."""
        timestamp = _get_timestamp()
        
        assert isinstance(timestamp, str)
        assert timestamp.endswith('Z')
        assert 'T' in timestamp  # ISO format has T separator


class TestGetTimestamp:
    """Test timestamp utility function."""
    
    def test_returns_string(self) -> None:
        """Test _get_timestamp returns string."""
        result = _get_timestamp()
        assert isinstance(result, str)
    
    def test_iso_format(self) -> None:
        """Test timestamp is in ISO format."""
        result = _get_timestamp()
        # Should be parseable as ISO format
        from datetime import datetime
        # Remove Z suffix for parsing
        datetime.fromisoformat(result[:-1])
