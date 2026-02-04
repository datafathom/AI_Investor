"""
Tests for Enterprise Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.enterprise import (
    TeamRole,
    Organization,
    Team,
    SharedResource
)


class TestTeamRoleEnum:
    """Tests for TeamRole enum."""
    
    def test_team_role_enum(self):
        """Test team role enum values."""
        assert TeamRole.ADMIN == "admin"
        assert TeamRole.MANAGER == "manager"
        assert TeamRole.ANALYST == "analyst"
        assert TeamRole.VIEWER == "viewer"


class TestOrganization:
    """Tests for Organization model."""
    
    def test_valid_organization(self):
        """Test valid organization creation."""
        org = Organization(
            organization_id='org_1',
            name='Test Organization',
            parent_organization_id=None,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert org.organization_id == 'org_1'
        assert org.name == 'Test Organization'
        assert org.parent_organization_id is None
    
    def test_organization_with_parent(self):
        """Test organization with parent."""
        org = Organization(
            organization_id='org_2',
            name='Sub Organization',
            parent_organization_id='org_1',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert org.parent_organization_id == 'org_1'


class TestTeam:
    """Tests for Team model."""
    
    def test_valid_team(self):
        """Test valid team creation."""
        team = Team(
            team_id='team_1',
            organization_id='org_1',
            team_name='Development Team',
            members=[
                {'user_id': 'user_1', 'role': 'admin'},
                {'user_id': 'user_2', 'role': 'analyst'}
            ],
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert team.team_id == 'team_1'
        assert len(team.members) == 2
    
    def test_team_defaults(self):
        """Test team with default values."""
        team = Team(
            team_id='team_1',
            organization_id='org_1',
            team_name='Test Team',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert len(team.members) == 0


class TestSharedResource:
    """Tests for SharedResource model."""
    
    def test_valid_shared_resource(self):
        """Test valid shared resource creation."""
        resource = SharedResource(
            resource_id='resource_1',
            resource_type='portfolio',
            team_id='team_1',
            permissions={'user_1': 'read_write', 'user_2': 'read'},
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert resource.resource_id == 'resource_1'
        assert resource.resource_type == 'portfolio'
        assert len(resource.permissions) == 2
