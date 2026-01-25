"""
Performance Middleware
Monitors and optimizes request performance
"""

import time
import logging
from functools import wraps
from flask import request, g, jsonify

logger = logging.getLogger(__name__)


def performance_monitor(app):
    """Add performance monitoring to Flask app."""
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        duration = time.time() - g.start_time
        
        # Log slow requests
        if duration > 1.0:
            logger.warning(
                f"Slow request: {request.method} {request.path} "
                f"took {duration:.2f}s"
            )
        
        # Add performance headers
        response.headers['X-Response-Time'] = f"{duration:.3f}s"
        response.headers['X-Request-ID'] = getattr(g, 'request_id', 'unknown')
        
        return response


def cache_control(max_age: int = 3600, public: bool = True):
    """Add cache control headers to response."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            cache_header = f"{'public' if public else 'private'}, max-age={max_age}"
            response.headers['Cache-Control'] = cache_header
            return response
        return wrapper
    return decorator


def compress_response(app):
    """Enable response compression."""
    try:
        from flask_compress import Compress
        Compress(app)
        logger.info("Response compression enabled")
    except ImportError:
        logger.warning("flask-compress not installed. Install with: pip install flask-compress")


def enable_cors_optimization(app):
    """Optimize CORS headers."""
    @app.after_request
    def add_cors_headers(response):
        # Preflight caching
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Max-Age'] = '86400'
        return response
