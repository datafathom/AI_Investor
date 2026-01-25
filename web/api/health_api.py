"""
Enhanced Health Check API
Production-ready health checks for load balancers and monitoring
"""

from flask import Blueprint, jsonify
from datetime import datetime
import logging

from services.system.health_check_service import get_health_check_service
from services.security.system_health_service import get_system_health_service

logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
@health_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Basic health check endpoint.
    Returns 200 if service is up, used by load balancers.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'ai-investor-backend',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@health_bp.route('/health/readiness', methods=['GET'])
def readiness_check():
    """
    Readiness check - verifies service can accept traffic.
    Checks database connectivity.
    """
    try:
        health_service = get_health_check_service()
        postgres_status = health_service.check_postgres()
        redis_status = health_service.check_redis()
        
        if postgres_status.get('status') == 'UP' and redis_status.get('status') == 'UP':
            return jsonify({
                'status': 'ready',
                'checks': {
                    'postgres': postgres_status,
                    'redis': redis_status
                },
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'not_ready',
                'checks': {
                    'postgres': postgres_status,
                    'redis': redis_status
                },
                'timestamp': datetime.utcnow().isoformat()
            }), 503
            
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return jsonify({
            'status': 'not_ready',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503


@health_bp.route('/health/liveness', methods=['GET'])
def liveness_check():
    """
    Liveness check - verifies service is alive.
    Should be fast and not check dependencies.
    """
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health():
    """
    Detailed health check with full system status.
    Used for monitoring dashboards.
    """
    try:
        health_service = get_health_check_service()
        system_health_service = get_system_health_service()
        
        import asyncio
        system_status = asyncio.run(system_health_service.get_health_status())
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'postgres': health_service.check_postgres(),
                'redis': health_service.check_redis(),
                'system': system_status
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503
