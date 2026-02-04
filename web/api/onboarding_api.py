"""
Onboarding API - FastAPI Router
Complete user onboarding flow with preference management
"""

import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding"])

# Models
class OnboardingStep(BaseModel):
    id: int
    name: str
    title: str
    required: bool

class StepUpdateRequest(BaseModel):
    step: int
    data: Dict[str, Any] = {}

class CompletionRequest(BaseModel):
    preferences: Dict[str, Any]

class PreferenceUpdateRequest(BaseModel):
    preferences: Dict[str, Any]

# Steps configuration
ONBOARDING_STEPS = [
    {"id": 1, "name": "welcome", "title": "Welcome to AI Investor", "required": True},
    {"id": 2, "name": "experience", "title": "Investment Experience", "required": True},
    {"id": 3, "name": "goals", "title": "Investment Goals", "required": True},
    {"id": 4, "name": "risk", "title": "Risk Tolerance", "required": True},
    {"id": 5, "name": "preferences", "title": "Preferences", "required": False},
    {"id": 6, "name": "complete", "title": "Complete", "required": False}
]

@router.get('/status')
async def get_onboarding_status(current_user: Dict[str, Any] = Depends(get_current_user)):
    user_id = current_user.get("id")
    
    # Mock response (would come from database)
    onboarding_data = {
        'user_id': user_id,
        'completed': False,
        'current_step': 1,
        'total_steps': len(ONBOARDING_STEPS),
        'steps': ONBOARDING_STEPS,
        'started_at': None,
        'completed_at': None,
        'preferences': {}
    }

    return {
        'success': True,
        'data': onboarding_data
    }

@router.post('/step')
async def update_onboarding_step(
    request_data: StepUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    user_id = current_user.get("id")
    step = request_data.step
    step_data = request_data.data

    if step < 1 or step > len(ONBOARDING_STEPS):
        return JSONResponse(status_code=400, content={"success": False, "detail": "Invalid step number"})

    logger.info("User %s updated onboarding step to %s", user_id, step)

    return {
        'success': True,
        'data': {
            'user_id': user_id,
            'current_step': step,
            'step_data': step_data,
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
    }

@router.post('/complete')
async def complete_onboarding(
    request_data: CompletionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    user_id = current_user.get("id")
    preferences = request_data.preferences

    required_fields = ['experience_level', 'risk_tolerance']
    missing_fields = [field for field in required_fields if field not in preferences]

    if missing_fields:
        return JSONResponse(status_code=400, content={"success": False, "detail": f"Missing required preferences: {missing_fields}"})

    logger.info("User %s completed onboarding with preferences: %s", user_id, preferences)

    return {
        'success': True,
        'data': {
            'user_id': user_id,
            'completed': True,
            'completed_at': datetime.now(timezone.utc).isoformat(),
            'preferences': preferences
        }
    }

@router.get('/preferences')
async def get_preferences(current_user: Dict[str, Any] = Depends(get_current_user)):
    user_id = current_user.get("id")
    return {
        'success': True,
        'data': {
            'user_id': user_id,
            'preferences': {}
        }
    }

@router.put('/preferences')
async def update_preferences(
    request_data: PreferenceUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    user_id = current_user.get("id")
    preferences = request_data.preferences

    if not preferences:
        return JSONResponse(status_code=400, content={"success": False, "detail": "No preferences provided"})

    logger.info("User %s updated preferences: %s", user_id, preferences)

    return {
        'success': True,
        'data': {
            'user_id': user_id,
            'preferences': preferences,
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
    }

@router.post('/skip')
async def skip_onboarding(current_user: Dict[str, Any] = Depends(get_current_user)):
    user_id = current_user.get("id")
    logger.info("User %s skipped onboarding", user_id)
    return {
        'success': True,
        'data': {
            'user_id': user_id,
            'skipped': True,
            'completed_at': datetime.now(timezone.utc).isoformat()
        }
    }

@router.post('/reset')
async def reset_onboarding(current_user: Dict[str, Any] = Depends(get_current_user)):
    user_id = current_user.get("id")
    logger.info("User %s reset onboarding", user_id)
    return {
        'success': True,
        'data': {
            'user_id': user_id,
            'reset': True,
            'current_step': 1,
            'reset_at': datetime.now(timezone.utc).isoformat()
        }
    }
