"""
Onboarding API
Complete user onboarding flow with preference management
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any

from flask import Blueprint, jsonify, request, g

from web.auth_utils import login_required

logger = logging.getLogger(__name__)

onboarding_api_bp = Blueprint('onboarding', __name__)
onboarding_bp = onboarding_api_bp  # Alias for app.py

# Onboarding steps configuration
ONBOARDING_STEPS = [
    {
        'id': 1,
        'name': 'welcome',
        'title': 'Welcome to AI Investor',
        'required': True
    },
    {
        'id': 2,
        'name': 'experience',
        'title': 'Investment Experience',
        'required': True
    },
    {
        'id': 3,
        'name': 'goals',
        'title': 'Investment Goals',
        'required': True
    },
    {
        'id': 4,
        'name': 'risk',
        'title': 'Risk Tolerance',
        'required': True
    },
    {
        'id': 5,
        'name': 'preferences',
        'title': 'Preferences',
        'required': False
    },
    {
        'id': 6,
        'name': 'complete',
        'title': 'Complete',
        'required': False
    }
]


@onboarding_api_bp.route('/onboarding/status', methods=['GET'])
@login_required
def get_onboarding_status():
    """
    Get user's onboarding status.
    Requires authentication.

    Returns:
        JSON response with onboarding status
    """
    user_id = getattr(g, 'user_id', None)

    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401

    # In production, query database for user onboarding status
    # Example SQL:
    # SELECT onboarding_completed, onboarding_step, preferences
    # FROM users WHERE id = :user_id

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

    return jsonify({
        'success': True,
        'data': onboarding_data
    }), 200


@onboarding_api_bp.route('/onboarding/step', methods=['POST'])
@login_required
def update_onboarding_step():
    """
    Update user's current onboarding step.
    Requires authentication.

    Request Body:
        {
            "step": 2,
            "data": { ... }
        }

    Returns:
        JSON response with updated status
    """
    user_id = getattr(g, 'user_id', None)

    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401

    data = request.get_json()
    step = data.get('step')
    step_data = data.get('data', {})

    if not step or step < 1 or step > len(ONBOARDING_STEPS):
        return jsonify({
            'success': False,
            'error': 'Invalid step number'
        }), 400

    # In production, update database
    # Example SQL:
    # UPDATE users
    # SET onboarding_step = :step,
    #     onboarding_data = jsonb_set(
    #         COALESCE(onboarding_data, '{}'::jsonb),
    #         ARRAY[:step_name],
    #         :step_data::jsonb
    #     )
    # WHERE id = :user_id

    logger.info("User %s updated onboarding step to %s", user_id, step)

    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'current_step': step,
            'step_data': step_data,
            'updated_at': datetime.utcnow().isoformat()
        }
    }), 200


@onboarding_api_bp.route('/onboarding/complete', methods=['POST'])
@login_required
def complete_onboarding():
    """
    Complete onboarding and save user preferences.
    Requires authentication.

    Request Body:
        {
            "preferences": {
                "experience_level": "intermediate",
                "investment_goals": ["growth", "income"],
                "risk_tolerance": "moderate",
                "notifications": true,
                "theme": "dark"
            }
        }

    Returns:
        JSON response with completion status
    """
    user_id = getattr(g, 'user_id', None)

    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401

    data = request.get_json()
    preferences = data.get('preferences', {})

    # Validate preferences
    required_fields = ['experience_level', 'risk_tolerance']
    missing_fields = [field for field in required_fields if field not in preferences]

    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required preferences: {missing_fields}'
        }), 400

    # In production, save to database
    # Example SQL:
    # UPDATE users
    # SET onboarding_completed = TRUE,
    #     onboarding_completed_at = NOW(),
    #     preferences = :preferences::jsonb
    # WHERE id = :user_id

    logger.info("User %s completed onboarding with preferences: %s", user_id, preferences)

    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'completed': True,
            'completed_at': datetime.utcnow().isoformat(),
            'preferences': preferences
        }
    }), 200


@onboarding_api_bp.route('/onboarding/preferences', methods=['GET'])
@login_required
def get_preferences():
    """
    Get user's saved preferences.
    Requires authentication.

    Returns:
        JSON response with user preferences
    """
    user_id = getattr(g, 'user_id', None)

    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401

    # In production, query database
    # Example SQL:
    # SELECT preferences FROM users WHERE id = :user_id

    preferences = {}  # Would come from database

    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'preferences': preferences
        }
    }), 200


@onboarding_api_bp.route('/onboarding/preferences', methods=['PUT'])
@login_required
def update_preferences():
    """
    Update user preferences.
    Requires authentication.

    Request Body:
        {
            "preferences": {
                "notifications": false,
                "theme": "light"
            }
        }

    Returns:
        JSON response with updated preferences
    """
    user_id = getattr(g, 'user_id', None)

    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401

    data = request.get_json()
    preferences = data.get('preferences', {})

    if not preferences:
        return jsonify({
            'success': False,
            'error': 'No preferences provided'
        }), 400

    # In production, update database
    # Example SQL:
    # UPDATE users
    # SET preferences = jsonb_set(
    #     COALESCE(preferences, '{}'::jsonb),
    #     ARRAY[:key],
    #     :value::jsonb
    # )
    # WHERE id = :user_id

    logger.info("User %s updated preferences: %s", user_id, preferences)

    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'preferences': preferences,
            'updated_at': datetime.utcnow().isoformat()
        }
    }), 200


@onboarding_api_bp.route('/onboarding/skip', methods=['POST'])
@login_required
def skip_onboarding():
    """
    Skip onboarding (mark as complete without preferences).
    Requires authentication.

    Returns:
        JSON response with skip status
    """
    user_id = getattr(g, 'user_id', None)

    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401

    # In production, update database
    # Example SQL:
    # UPDATE users
    # SET onboarding_completed = TRUE,
    #     onboarding_skipped = TRUE,
    #     onboarding_completed_at = NOW()
    # WHERE id = :user_id

    logger.info("User %s skipped onboarding", user_id)

    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'skipped': True,
            'completed_at': datetime.utcnow().isoformat()
        }
    }), 200


@onboarding_api_bp.route('/onboarding/reset', methods=['POST'])
@login_required
def reset_onboarding():
    """
    Reset onboarding (for testing or re-onboarding).
    Requires authentication.

    Returns:
        JSON response with reset status
    """
    user_id = getattr(g, 'user_id', None)

    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401

    # In production, reset in database
    # Example SQL:
    # UPDATE users
    # SET onboarding_completed = FALSE,
    #     onboarding_step = 1,
    #     onboarding_data = NULL
    # WHERE id = :user_id

    logger.info("User %s reset onboarding", user_id)

    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'reset': True,
            'current_step': 1,
            'reset_at': datetime.utcnow().isoformat()
        }
    }), 200
