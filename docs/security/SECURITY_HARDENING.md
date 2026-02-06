# Security Hardening Guide

This guide covers security best practices and hardening measures for the AI Investor platform.

## Security Headers

### Content Security Policy (CSP)
- Prevents XSS attacks
- Restricts resource loading
- Configured in `security_middleware.py`

### Other Security Headers
- `X-Content-Type-Options: nosniff` - Prevents MIME sniffing
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `Strict-Transport-Security` - Forces HTTPS
- `Referrer-Policy` - Controls referrer information

## Input Validation

### Validation Schema
Use `@validate_input` decorator:

```python
from web.middleware.security_middleware import validate_input

@validate_input({
    'email': {
        'required': True,
        'type': str,
        'pattern': r'^[^@]+@[^@]+\.[^@]+$'
    },
    'amount': {
        'required': True,
        'type': float,
        'min': 0,
        'max': 1000000
    }
})
def create_order():
    # Handler code
    pass
```

### Input Sanitization
- Remove dangerous characters
- Limit input length
- Use parameterized queries

## Rate Limiting

### IP-Based Rate Limiting
```python
from web.middleware.security_middleware import rate_limit_by_ip

@rate_limit_by_ip(max_requests=100, window=60)
def api_endpoint():
    # Handler code
    pass
```

### User-Based Rate Limiting
- Implemented via FastAPI-Limiter
- Different limits for authenticated users
- Configurable per endpoint

## SQL Injection Prevention

### Parameterized Queries
Always use parameterized queries:

```python
# ✅ Good
db.execute("SELECT * FROM users WHERE id = ?", user_id)

# ❌ Bad
db.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### Input Validation
- Validate all user input
- Use whitelist approach
- Check for dangerous patterns

## Authentication & Authorization

### JWT Tokens
- Short expiration (15 minutes)
- Refresh tokens for long sessions
- Secure token storage

### Password Security
- Bcrypt hashing (cost factor 12)
- Minimum 8 characters
- Require complexity

### Multi-Factor Authentication
- TOTP support
- SMS backup
- Recovery codes

## HTTPS Enforcement

### Production
- Force HTTPS redirects
- HSTS header enabled
- Valid SSL certificates

### Development
- HTTPS optional
- Self-signed certificates OK

## CSRF Protection

### Token-Based Protection
- Generate CSRF tokens
- Validate on state-changing requests
- Exempt API endpoints with token auth

## Secrets Management

### Environment Variables
- Never commit secrets
- Use `.env` files (gitignored)
- Rotate secrets regularly

### Vault Integration
- Use HashiCorp Vault or AWS Secrets Manager
- Encrypt secrets at rest
- Audit secret access

## Security Monitoring

### Logging
- Log all authentication attempts
- Log security events
- Monitor for suspicious activity

### Alerts
- Failed login attempts
- Rate limit violations
- Unusual access patterns

## Security Checklist

- [ ] All endpoints require authentication
- [ ] Input validation on all user inputs
- [ ] SQL injection prevention
- [ ] XSS protection (CSP headers)
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] HTTPS enforced in production
- [ ] Security headers set
- [ ] Secrets properly managed
- [ ] Regular security audits
- [ ] Dependency vulnerability scanning
- [ ] Penetration testing

## Incident Response

### Security Incident Procedure
1. Identify and contain threat
2. Assess damage
3. Notify security team
4. Remediate vulnerabilities
5. Document incident
6. Post-mortem review

### Contact
- **Security Team**: security@aiinvestor.com
- **Emergency**: Use PagerDuty escalation
