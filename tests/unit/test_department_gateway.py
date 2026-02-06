"""
==============================================================================
Unit Tests - Department WebSocket Gateway
==============================================================================
Tests the Department WebSocket broadcaster and event handlers.
==============================================================================
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timezone

from web.websocket.department_gateway import (
    broadcast_agent_status,
    broadcast_metrics,
    broadcast_event,
    _verify_jwt,
    connect,
    subscribe_department,
    unsubscribe_department,
    dept_sio
)

# Mock settings for all tests to avoid environment issues
@pytest.fixture(autouse=True)
def mock_settings():
    with patch('web.websocket.department_gateway.get_settings') as mock:
        settings = MagicMock()
        settings.JWT_SECRET = "dev_secret_key"
        settings.JWT_ALGORITHM = "HS256"
        settings.APP_ENV = "testing"
        mock.return_value = settings
        yield settings

@pytest.mark.asyncio
async def test_broadcast_agent_status() -> None:
    """Test agent status broadcast emits correct event to room."""
    with patch.object(dept_sio, 'emit', new_callable=AsyncMock) as mock_emit:
        await broadcast_agent_status(1, "agent-001", "BUSY", {"task": "analysis"})
        
        mock_emit.assert_called_once()
        args, kwargs = mock_emit.call_args
        assert args[0] == 'agent_status'
        assert args[1]['dept_id'] == 1
        assert args[1]['agent_id'] == "agent-001"
        assert args[1]['status'] == "BUSY"
        assert args[1]['details']['task'] == "analysis"
        assert kwargs['room'] == "dept_1"

@pytest.mark.asyncio
async def test_broadcast_metrics() -> None:
    """Test metrics broadcast."""
    with patch.object(dept_sio, 'emit', new_callable=AsyncMock) as mock_emit:
        await broadcast_metrics(2, {"rps": 150})
        
        mock_emit.assert_called_once()
        args, kwargs = mock_emit.call_args
        assert args[0] == 'metrics'
        assert args[1]['dept_id'] == 2
        assert args[1]['metrics']['rps'] == 150
        assert kwargs['room'] == "dept_2"

@pytest.mark.asyncio
async def test_subscribe_department() -> None:
    """Test department subscription logic."""
    sid = "test-sid"
    data = {"dept_id": 1}
    
    with patch.object(dept_sio, 'enter_room', new_callable=AsyncMock) as mock_enter_room, \
         patch.object(dept_sio, 'emit', new_callable=AsyncMock) as mock_emit:
        
        # We need to reach into the module-level _dept_connections or mock it
        # For simplicity, we just test the SIO interaction
        await subscribe_department(sid, data)
        
        mock_enter_room.assert_called_once_with(sid, "dept_1")
        mock_emit.assert_called_with('subscribed', {'dept_id': 1, 'room': 'dept_1', 'active_connections': 1}, to=sid)

@pytest.mark.asyncio
async def test_subscribe_invalid_dept() -> None:
    """Test subscription with invalid data."""
    sid = "test-sid"
    data = {"dept_id": "invalid"}  # Should be int
    
    with patch.object(dept_sio, 'emit', new_callable=AsyncMock) as mock_emit:
        await subscribe_department(sid, data)
        
        mock_emit.assert_called_once()
        args, kwargs = mock_emit.call_args
        assert args[0] == 'error'
        assert 'Invalid' in args[1]['message']

@pytest.mark.asyncio
async def test_unsubscribe_department() -> None:
    """Test department unsubscription."""
    sid = "test-sid"
    data = {"dept_id": 1}
    
    with patch.object(dept_sio, 'leave_room', new_callable=AsyncMock) as mock_leave_room, \
         patch.object(dept_sio, 'emit', new_callable=AsyncMock) as mock_emit:
        
        await unsubscribe_department(sid, data)
        
        # Note: If not subscribed, leave_room is still called but sets are handled
        mock_leave_room.assert_called_once_with(sid, "dept_1")

def test_verify_jwt_invalid_token() -> None:
    """Test JWT verification with junk data."""
    result = _verify_jwt("not-a-token")
    assert result is None

@pytest.mark.asyncio
async def test_connect_unauthenticated() -> None:
    """Test connection without token."""
    sid = "test-sid"
    environ = {'QUERY_STRING': ''}
    from unittest.mock import ANY
    
    with patch.object(dept_sio, 'save_session', new_callable=AsyncMock) as mock_save, \
         patch.object(dept_sio, 'emit', new_callable=AsyncMock) as mock_emit:
        
        # Connect returns bool (always True in our current implementation)
        result = await connect(sid, environ)
        
        assert result is True
        mock_save.assert_called_once()
        assert mock_save.call_args[0][1]['authenticated'] is False
        mock_emit.assert_any_call('connected', ANY, to=sid)
