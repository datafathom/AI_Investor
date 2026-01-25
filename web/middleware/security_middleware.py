"""
Security Middleware
Enhanced security headers and protections
"""

import logging
from flask import request, g, jsonify, abort
from functools import wraps
import re

logger = logging.getLogger(__name__)


def security_headers(app):
    """Add security headers to all responses."""
    
    @app.after_request
    def add_security_headers(response):
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://api.sentry.io wss://localhost:*; "
            "frame-ancestors 'none';"
        )
        response.headers['Content-Security-Policy'] = csp
        
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response


def rate_limit_by_ip(max_requests: int = 100, window: int = 60):
    """Rate limiting by IP address (uses advanced rate limiter if available)."""
    try:
        from web.middleware.rate_limiter import rate_limit_by_ip as advanced_rate_limit
        return advanced_rate_limit(max_requests=max_requests, window=window)
    except ImportError:
        # Fallback to simple in-memory rate limiting
        from collections import defaultdict
        from time import time
        
        request_counts = defaultdict(list)
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                ip = request.remote_addr
                now = time()
                
                # Clean old requests
                request_counts[ip] = [
                    req_time for req_time in request_counts[ip]
                    if now - req_time < window
                ]
                
                # Check rate limit
                if len(request_counts[ip]) >= max_requests:
                    logger.warning(f"Rate limit exceeded for IP: {ip}")
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'retry_after': window
                    }), 429
                
                # Record request
                request_counts[ip].append(now)
                
                return func(*args, **kwargs)
            return wrapper
        return decorator


def validate_input(schema: dict):
    """Validate request input against schema."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json() or {}
            errors = []
            
            for field, rules in schema.items():
                value = data.get(field)
                
                # Required check
                if rules.get('required') and not value:
                    errors.append(f"{field} is required")
                    continue
                
                if value is None:
                    continue
                
                # Type check
                expected_type = rules.get('type')
                if expected_type and not isinstance(value, expected_type):
                    errors.append(f"{field} must be {expected_type.__name__}")
                    continue
                
                # Pattern check
                pattern = rules.get('pattern')
                if pattern and isinstance(value, str):
                    if not re.match(pattern, value):
                        errors.append(f"{field} format is invalid")
                        continue
                
                # Min/Max check
                if isinstance(value, (int, float)):
                    if 'min' in rules and value < rules['min']:
                        errors.append(f"{field} must be >= {rules['min']}")
                    if 'max' in rules and value > rules['max']:
                        errors.append(f"{field} must be <= {rules['max']}")
            
            if errors:
                return jsonify({
                    'error': 'Validation failed',
                    'errors': errors
                }), 400
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def sanitize_input(data: dict) -> dict:
    """Sanitize user input to prevent injection attacks."""
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove potentially dangerous characters
            value = re.sub(r'[<>"\']', '', value)
            # Limit length
            value = value[:1000]
        sanitized[key] = value
    
    return sanitized


def require_https(app):
    """Require HTTPS in production."""
    @app.before_request
    def force_https():
        if app.config.get('ENV') == 'production':
            if not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
                if request.url.startswith('http://'):
                    url = request.url.replace('http://', 'https://', 1)
                    from flask import redirect
                    return redirect(url, code=301)


def csrf_protection(app):
    """CSRF protection."""
    from flask import session
    
    @app.before_request
    def csrf_check():
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            # Skip CSRF for API endpoints with token auth
            if request.path.startswith('/api/') and request.headers.get('Authorization'):
                return
            
            token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
            session_token = session.get('csrf_token')
            
            if not token or token != session_token:
                logger.warning(f"CSRF token validation failed for {request.path}")
                abort(403)


def sql_injection_protection(query: str) -> bool:
    """Check for potential SQL injection."""
    dangerous_patterns = [
        r"(\bOR\b|\bAND\b)\s*\d+\s*=\s*\d+",
        r"(\bUNION\b|\bSELECT\b).*(\bFROM\b|\bWHERE\b)",
        r"(\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b).*(\bTABLE\b|\bDATABASE\b)",
        r"(--|#|\/\*|\*\/)",
        r"(\bEXEC\b|\bEXECUTE\b)",
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            logger.warning(f"Potential SQL injection detected: {query[:100]}")
            return False
    
    return True
