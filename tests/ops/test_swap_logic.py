
import pytest
from unittest.mock import MagicMock, patch
from scripts.ops.swap_deploy import DeploymentSwapper

@pytest.fixture
def swapper():
    return DeploymentSwapper()

@patch('requests.get')
def test_health_check_up(mock_get, swapper):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"overall": "UP"}
    
    assert swapper.check_health(5050) is True

@patch('requests.get')
def test_health_check_down(mock_get, swapper):
    mock_get.return_value.status_code = 503
    assert swapper.check_health(5050) is False

@patch('scripts.ops.swap_deploy.DeploymentSwapper.check_health')
def test_swap_to_blue_success(mock_health, swapper):
    mock_health.return_value = True
    
    # This should not raise SystemExit
    swapper.swap_to("blue")

@patch('scripts.ops.swap_deploy.DeploymentSwapper.check_health')
def test_swap_to_green_unhealthy_aborts(mock_health, swapper):
    mock_health.return_value = False
    
    with pytest.raises(SystemExit):
        swapper.swap_to("green")
