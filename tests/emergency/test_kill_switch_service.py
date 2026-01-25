
import pytest
from unittest.mock import MagicMock, patch
from services.risk.kill_switch_service import KillSwitchService

@pytest.fixture
def kill_switch_service():
    # Reset singleton for testing
    KillSwitchService._instance = None
    with patch('services.risk.kill_switch_service.MessageBus'):
        service = KillSwitchService()
        service.is_frozen = False
        return service

def test_activate_kill_switch(kill_switch_service):
    """Test kill switch activation."""
    result = kill_switch_service.activate_kill_switch("test-user")
    
    assert result["status"] == "success"
    assert kill_switch_service.is_frozen is True

def test_deactivate_kill_switch_correct_passcode(kill_switch_service):
    """Test kill switch deactivation with correct passcode."""
    kill_switch_service.is_frozen = True
    result = kill_switch_service.deactivate_kill_switch("123456")
    
    assert result is True
    assert kill_switch_service.is_frozen is False

def test_deactivate_kill_switch_wrong_passcode(kill_switch_service):
    """Test kill switch deactivation with wrong passcode fails."""
    kill_switch_service.is_frozen = True
    result = kill_switch_service.deactivate_kill_switch("wrong")
    
    assert result is False
    assert kill_switch_service.is_frozen is True

def test_get_status(kill_switch_service):
    """Test get status returns correct frozen state."""
    kill_switch_service.is_frozen = False
    status = kill_switch_service.get_status()
    assert status["is_frozen"] is False
    
    kill_switch_service.is_frozen = True
    status = kill_switch_service.get_status()
    assert status["is_frozen"] is True

def test_broadcast_emergency_message(kill_switch_service):
    """Test that activation broadcasts emergency message."""
    kill_switch_service.bus.publish = MagicMock()
    
    kill_switch_service.activate_kill_switch("admin")
    
    kill_switch_service.bus.publish.assert_called_once()
    call_args = kill_switch_service.bus.publish.call_args[0]
    assert call_args[0] == "system"
    assert call_args[1] == "emergency"
    assert call_args[2]["type"] == "EMERGENCY_KILL"
