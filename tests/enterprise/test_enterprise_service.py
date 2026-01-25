"""
Tests for Enterprise Service
Comprehensive test coverage for organization and team management
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.enterprise.enterprise_service import EnterpriseService
from models.enterprise import Organization, Team, TeamRole


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.enterprise.enterprise_service.get_cache_service'):
        return EnterpriseService()


@pytest.mark.asyncio
async def test_create_organization(service):
    """Test organization creation."""
    service._save_organization = AsyncMock()
    
    result = await service.create_organization(
        name="Acme Corp"
    )
    
    assert result is not None
    assert isinstance(result, Organization)
    assert result.name == "Acme Corp"


@pytest.mark.asyncio
async def test_create_team(service):
    """Test team creation."""
    service._save_team = AsyncMock()
    
    result = await service.create_team(
        organization_id="org_123",
        team_name="Investment Team"
    )
    
    assert result is not None
    assert isinstance(result, Team)
    assert result.organization_id == "org_123"
    assert result.team_name == "Investment Team"


@pytest.mark.asyncio
async def test_add_team_member(service):
    """Test adding team member."""
    team = Team(
        team_id="team_123",
        organization_id="org_123",
        team_name="Test Team",
        members=[],
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_team = AsyncMock(return_value=team)
    service._save_team = AsyncMock()
    
    result = await service.add_team_member(
        team_id="team_123",
        user_id="user_456",
        role=TeamRole.MEMBER
    )
    
    assert result is not None
    assert len(result.members) == 1
    assert result.members[0]['user_id'] == "user_456"
