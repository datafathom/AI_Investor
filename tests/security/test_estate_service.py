import pytest
from datetime import datetime, timedelta
from services.security.estate_service import (
    EstateService, 
    Beneficiary, 
    HeartbeatStatus, 
    SuccessionResult,
    get_estate_service
)

@pytest.fixture
def estate_service():
    service = EstateService()
    return service

@pytest.mark.asyncio
async def test_check_heartbeat(estate_service):
    status = await estate_service.check_heartbeat("user123")
    assert status.is_alive is True
    assert status.days_until_trigger == 30
    assert "2026" in status.trigger_date

@pytest.mark.asyncio
async def test_confirm_alive(estate_service):
    # Simulate some time passed
    estate_service._last_heartbeat = datetime.now() - timedelta(days=5)
    status_before = await estate_service.check_heartbeat("user123")
    assert status_before.days_until_trigger == 25
    
    await estate_service.confirm_alive("user123")
    status_after = await estate_service.check_heartbeat("user123")
    assert status_after.days_until_trigger == 30

@pytest.mark.asyncio
async def test_trigger_succession(estate_service):
    result = await estate_service.trigger_succession("user123")
    assert result.triggered is True
    assert result.assets_transferred == 25000000.0
    assert result.beneficiaries_notified == 3

@pytest.mark.asyncio
async def test_beneficiary_management(estate_service):
    beneficiaries = await estate_service.get_beneficiaries("user123")
    assert len(beneficiaries) == 3
    
    new_b = Beneficiary("b4", "Charity B", "Charity", 5.0, "b@example.com")
    await estate_service.add_beneficiary("user123", new_b)
    
    beneficiaries_updated = await estate_service.get_beneficiaries("user123")
    assert len(beneficiaries_updated) == 4
    assert beneficiaries_updated[-1].name == "Charity B"

@pytest.mark.asyncio
async def test_update_allocation(estate_service):
    # Valid update
    success = await estate_service.update_allocation("user123", "b1", 60.0)
    assert success is True
    bens = await estate_service.get_beneficiaries("user123")
    assert bens[0].allocation_percent == 60.0
    
    # Invalid update
    fail = await estate_service.update_allocation("user123", "non-existent", 10.0)
    assert fail is False

@pytest.mark.asyncio
async def test_get_entity_graph(estate_service):
    graph = await estate_service.get_entity_graph("user123")
    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) == 4
    assert len(graph["edges"]) == 3
    assert graph["nodes"][0]["label"] == "Master Family Trust"

@pytest.mark.asyncio
async def test_calculate_estate_tax(estate_service):
    # Under exemption
    tax1 = await estate_service.calculate_estate_tax(10000000.0)
    assert tax1 == 0.0
    
    # Over exemption ($20M)
    tax2 = await estate_service.calculate_estate_tax(20000000.0)
    # (20M - 12.92M) * 0.4 = 7.08M * 0.4 = 2.832M
    assert tax2 == (20000000.0 - 12920000.0) * 0.4

def test_get_estate_service():
    s1 = get_estate_service()
    s2 = get_estate_service()
    assert s1 is s2
    assert isinstance(s1, EstateService)
