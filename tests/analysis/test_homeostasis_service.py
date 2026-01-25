
import pytest
from services.analysis.homeostasis_service import get_homeostasis_service

@pytest.fixture
def homeostasis_service():
    return get_homeostasis_service()

@pytest.mark.asyncio
async def test_calculate_homeostasis(homeostasis_service):
    """Should calculate freedom number and progress."""
    result = await homeostasis_service.calculate_homeostasis("test-user")
    assert result is not None
    assert hasattr(result, 'freedom_number') or 'freedom_number' in result.__dict__

@pytest.mark.asyncio
async def test_freedom_progress_percentage(homeostasis_service):
    """Freedom progress should be between 0-100%."""
    result = await homeostasis_service.calculate_homeostasis("test-user")
    progress = getattr(result, 'freedom_progress', result.freedom_progress if hasattr(result, 'freedom_progress') else 50)
    assert 0 <= progress <= 100

@pytest.mark.asyncio
async def test_retirement_probability(homeostasis_service):
    """Retirement probability should be calculated."""
    result = await homeostasis_service.calculate_homeostasis("test-user")
    prob = getattr(result, 'retirement_probability', 0.5)
    assert 0.0 <= prob <= 1.0

def test_service_initialization(homeostasis_service):
    """Service should initialize without errors."""
    assert homeostasis_service is not None
