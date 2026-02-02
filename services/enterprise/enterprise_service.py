"""
==============================================================================
FILE: services/enterprise/enterprise_service.py
ROLE: Enterprise Service
PURPOSE: Provides enterprise features including team management,
         organizational hierarchies, and role-based access.

INTEGRATION POINTS:
    - UserService: User and team management
    - RBACService: Role-based access control
    - BillingService: Enterprise billing
    - EnterpriseAPI: Enterprise endpoints

FEATURES:
    - Team management
    - Organizational hierarchies
    - Role assignments
    - Shared resources

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from models.enterprise import Organization, Team, TeamRole
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class EnterpriseService:
    """
    Service for enterprise features.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
    async def create_organization(
        self,
        name: str,
        parent_organization_id: Optional[str] = None
    ) -> Organization:
        """
        Create organization.
        
        Args:
            name: Organization name
            parent_organization_id: Optional parent organization
            
        Returns:
            Organization object
        """
        logger.info(f"Creating organization: {name}")
        
        organization = Organization(
            organization_id=f"org_{datetime.now(timezone.utc).timestamp()}",
            name=name,
            parent_organization_id=parent_organization_id,
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
        
        # Save organization
        await self._save_organization(organization)
        
        return organization
    
    async def create_team(
        self,
        organization_id: str,
        team_name: str
    ) -> Team:
        """
        Create team.
        
        Args:
            organization_id: Organization identifier
            team_name: Team name
            
        Returns:
            Team object
        """
        logger.info(f"Creating team {team_name} in organization {organization_id}")
        
        team = Team(
            team_id=f"team_{organization_id}_{datetime.now(timezone.utc).timestamp()}",
            organization_id=organization_id,
            team_name=team_name,
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
        
        # Save team
        await self._save_team(team)
        
        return team
    
    async def add_team_member(
        self,
        team_id: str,
        user_id: str,
        role: str
    ) -> Team:
        """
        Add member to team.
        
        Args:
            team_id: Team identifier
            user_id: User identifier
            role: Team role
            
        Returns:
            Updated Team
        """
        team = await self._get_team(team_id)
        if not team:
            raise ValueError(f"Team {team_id} not found")
        
        # Add member if not already in team
        member_exists = any(m.get('user_id') == user_id for m in team.members)
        if not member_exists:
            team.members.append({
                "user_id": user_id,
                "role": role,
                "joined_date": datetime.now(timezone.utc).isoformat()
            })
            team.updated_date = datetime.now(timezone.utc)
            await self._save_team(team)
        
        return team
    
    async def _get_organization(self, organization_id: str) -> Optional[Organization]:
        """Get organization from cache."""
        cache_key = f"organization:{organization_id}"
        org_data = self.cache_service.get(cache_key)
        if org_data:
            return Organization(**org_data)
        return None
    
    async def _save_organization(self, organization: Organization):
        """Save organization to cache."""
        cache_key = f"organization:{organization.organization_id}"
        self.cache_service.set(cache_key, organization.dict(), ttl=86400 * 365)
    
    async def _get_team(self, team_id: str) -> Optional[Team]:
        """Get team from cache."""
        cache_key = f"team:{team_id}"
        team_data = self.cache_service.get(cache_key)
        if team_data:
            return Team(**team_data)
        return None
    
    async def _save_team(self, team: Team):
        """Save team to cache."""
        cache_key = f"team:{team.team_id}"
        self.cache_service.set(cache_key, team.dict(), ttl=86400 * 365)


# Singleton instance
_enterprise_service: Optional[EnterpriseService] = None


def get_enterprise_service() -> EnterpriseService:
    """Get singleton enterprise service instance."""
    global _enterprise_service
    if _enterprise_service is None:
        _enterprise_service = EnterpriseService()
    return _enterprise_service
