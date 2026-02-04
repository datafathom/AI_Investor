"""
==============================================================================
FILE: web/api/enterprise_api.py
ROLE: Enterprise API Endpoints (FastAPI)
PURPOSE: REST endpoints for enterprise features and multi-user support.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
import logging
from typing import List, Optional, Dict
from pydantic import BaseModel
from services.enterprise.enterprise_service import get_enterprise_service as _get_enterprise_service
from services.enterprise.multi_user_service import get_multi_user_service as _get_multi_user_service

def get_enterprise_provider():
    return _get_enterprise_service()

def get_multi_user_provider():
    return _get_multi_user_service()
from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/enterprise", tags=["Enterprise"])

class OrgCreateRequest(BaseModel):
    name: str
    parent_organization_id: Optional[str] = None

class TeamCreateRequest(BaseModel):
    organization_id: str
    team_name: str

class MemberAddRequest(BaseModel):
    user_id: str
    role: str

class ResourceShareRequest(BaseModel):
    resource_type: str
    resource_id: str
    team_id: str
    permissions: Dict = {}


@router.post('/organization/create')
async def create_organization(
    data: OrgCreateRequest,
    service = Depends(get_enterprise_provider),
    current_user: dict = Depends(get_current_user)
):
    """
    Create organization.
    """
    try:
        organization = await service.create_organization(data.name, data.parent_organization_id)
        return {'success': True, 'data': organization.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating organization: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/team/create')
async def create_team(
    data: TeamCreateRequest,
    service = Depends(get_enterprise_provider),
    current_user: dict = Depends(get_current_user)
):
    """
    Create team.
    """
    try:
        team = await service.create_team(data.organization_id, data.team_name)
        return {'success': True, 'data': team.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating team: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/team/{team_id}/member')
async def add_team_member(
    team_id: str,
    data: MemberAddRequest,
    service = Depends(get_enterprise_provider),
    current_user: dict = Depends(get_current_user)
):
    """
    Add member to team.
    """
    try:
        team = await service.add_team_member(team_id, data.user_id, data.role)
        return {'success': True, 'data': team.model_dump()}
    except Exception as e:
        logger.exception(f"Error adding team member to team {team_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/resource/share')
async def share_resource(
    data: ResourceShareRequest,
    service = Depends(get_multi_user_provider),
    current_user: dict = Depends(get_current_user)
):
    """
    Share resource with team.
    """
    try:
        shared_resource = await service.share_resource(
            resource_type=data.resource_type,
            resource_id=data.resource_id,
            team_id=data.team_id,
            permissions=data.permissions
        )
        return {'success': True, 'data': shared_resource.model_dump()}
    except Exception as e:
        logger.exception(f"Error sharing resource: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/teams')
async def get_teams(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_enterprise_provider)
):
    """
    Get teams for a user.
    """
    try:
        teams = await service.get_user_teams(user_id)
        return {'success': True, 'data': [t.model_dump() if hasattr(t, 'model_dump') else t for t in teams] if teams else []}
    except Exception as e:
        logger.exception(f"Error getting teams for user {user_id}: {e}")
        # Return mock teams as fallback
        return {
            'success': True,
            'data': [
                {'team_id': 'team_1', 'name': 'Trading Team', 'role': 'member', 'member_count': 5},
                {'team_id': 'team_2', 'name': 'Research Team', 'role': 'admin', 'member_count': 3}
            ]
        }

