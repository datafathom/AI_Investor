
import pytest
from unittest.mock import MagicMock, patch
from services.analysis.scenario_service import get_scenario_service, MacroShock

@pytest.fixture
def scenario_service():
    return get_scenario_service()

@pytest.mark.asyncio
async def test_apply_shock(scenario_service):
    """Should simulate macro shock impact on portfolio."""
    shock = MacroShock(
        id="recession",
        name="Recession",
        equity_drop=-30.0,
        bond_drop=-5.0,
        gold_change=10.0
    )
    result = await scenario_service.apply_shock("default", shock)
    assert result is not None
    assert hasattr(result, 'portfolio_impact') or hasattr(result, 'new_portfolio_value')

@pytest.mark.asyncio
async def test_hedge_sufficiency(scenario_service):
    """Should calculate hedge sufficiency ratio."""
    shock = MacroShock(
        id="crash",
        name="Market Crash",
        equity_drop=-40.0,
        bond_drop=-10.0,
        gold_change=15.0
    )
    sufficiency = await scenario_service.calculate_hedge_sufficiency("default", shock)
    assert 0.0 <= sufficiency <= 1.0

def test_service_initialization(scenario_service):
    """Service should initialize correctly."""
    assert scenario_service is not None
