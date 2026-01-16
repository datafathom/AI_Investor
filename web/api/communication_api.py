"""
==============================================================================
FILE: web/api/communication_api.py
ROLE: Communication Gateway
PURPOSE:
    Expose Notification and Personalization services to the frontend.
    Allows the Dashboard to fetch the "Morning Coffee" briefing and 
    user to update alert preferences.
    
    Endpoints:
    - GET /api/v1/communication/briefing: Get daily Morning Briefing.
    - POST /api/v1/communication/test-alert: Trigger a test alert.
       
ROADMAP: Phase 29 - User Personalization
==============================================================================
"""

from flask import Blueprint, jsonify, request
from services.analysis.morning_briefing import get_briefing_service
from services.communication.notification_manager import get_notification_manager, AlertPriority

communication_bp = Blueprint('communication', __name__, url_prefix='/api/v1/communication')

@communication_bp.route('/briefing', methods=['GET'])
def get_morning_briefing():
    """
    Get the personalized morning briefing.
    In a real app, we'd fetch the user's name and portfolio status from the DB.
    """
    briefing_service = get_briefing_service()
    
    # Mock context - in reality, get this from Portfolio/Risk services
    # We use query params for testing, but default to safe fallbacks
    name = request.args.get('name', 'Commander')
    value = float(request.args.get('value', 100000.0))
    fear = float(request.args.get('fear', 50.0))
    sentiment = request.args.get('sentiment', 'NEUTRAL')
    
    report = briefing_service.generate_briefing(name, value, fear, sentiment)
    
    return jsonify({
        "briefing_text": report,
        "meta": {
            "fear_used": fear,
            "sentiment_used": sentiment
        }
    })

@communication_bp.route('/test-alert', methods=['POST'])
def trigger_test_alert():
    """
    Trigger a test alert to verify notification channels.
    Payload: {"message": "Test", "priority": "INFO|CRITICAL"}
    """
    data = request.json or {}
    message = data.get('message', 'Test Alert from Dashboard')
    priority_str = data.get('priority', 'INFO').upper()
    
    try:
        priority = AlertPriority[priority_str]
    except KeyError:
        priority = AlertPriority.INFO
        
    manager = get_notification_manager()
    manager.send_alert(message, priority)
    
    return jsonify({
        "status": "sent",
        "channel_count": len(manager.history[-1]['channels']),
        "channels": manager.history[-1]['channels']
    })
