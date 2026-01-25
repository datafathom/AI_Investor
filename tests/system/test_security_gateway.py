import pytest
from flask import Flask
from services.system.security_gateway import limiter

def test_rate_limiting_enforcement():
    """
    Simulates rate limiting on a mock Flask app.
    NOTE: Using a custom limit for testing to avoid 1000 hits.
    """
    app = Flask(__name__)
    limiter.init_app(app)

    @app.route("/test-limit")
    @limiter.limit("2 per minute")
    def test_limit():
        return "OK"

    client = app.test_client()

    # Hit 1
    assert client.get("/test-limit").status_code == 200
    # Hit 2
    assert client.get("/test-limit").status_code == 200
    # Hit 3 (Should be rate limited)
    assert client.get("/test-limit").status_code == 429

def test_gateway_status():
    from services.system.security_gateway import get_security_gateway
    gw = get_security_gateway()
    status = gw.get_status()
    assert status["status"] == "Active"
    assert "rate_limiter" in status
    assert "waf_rules" in status
