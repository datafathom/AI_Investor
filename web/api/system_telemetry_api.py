from flask import Blueprint, jsonify, request
import random
import time

system_telemetry_bp = Blueprint('system_telemetry', __name__, url_prefix='/api/v1/system')

@system_telemetry_bp.route('/quota', methods=['GET'])
def get_quota():
    """Returns API quota usage metrics."""
    return jsonify({
        "success": True,
        "data": {
            "used": random.randint(400, 950),
            "total": 1000,
            "percentage": None # Calculated by frontend or here
        }
    })

@system_telemetry_bp.route('/health', methods=['GET'])
def get_health():
    """Returns system health and provider latency."""
    return jsonify({
        "success": True,
        "data": {
            "status": "nominal",
            "latency": {
                "us-east": random.randint(20, 50),
                "us-west": random.randint(40, 80),
                "eu-central": random.randint(100, 150),
                "ap-southeast": random.randint(200, 300)
            }
        }
    })

@system_telemetry_bp.route('/load', methods=['GET'])
def get_load():
    """Returns historical system load for sparklines."""
    return jsonify({
        "success": True,
        "data": [random.randint(20, 90) for _ in range(20)]
    })
