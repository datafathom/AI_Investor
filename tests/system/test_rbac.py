import pytest
from flask import Flask, g
from web.auth_utils import login_required, requires_role, generate_token

def test_rbac_access_granted():
    app = Flask(__name__)
    
    @app.route("/admin-only")
    @login_required
    @requires_role("admin")
    def admin_only():
        return "OK"

    client = app.test_client()
    
    # 1. Generate Admin Token
    token = generate_token(user_id=1, role="admin")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/admin-only", headers=headers)
    assert response.status_code == 200

def test_rbac_access_denied():
    app = Flask(__name__)
    
    @app.route("/admin-only")
    @login_required
    @requires_role("admin")
    def admin_only():
        return "OK"

    client = app.test_client()
    
    # 1. Generate Trader Token (Should be denied)
    token = generate_token(user_id=2, role="trader")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/admin-only", headers=headers)
    assert response.status_code == 403
    assert b"Forbidden" in response.data

def test_role_hierarchy():
    app = Flask(__name__)
    
    @app.route("/trader-plus")
    @login_required
    @requires_role("trader")
    def trader_plus():
        return "OK"

    client = app.test_client()
    
    # Admin should have access to trader endpoints (Hierarchy)
    token = generate_token(user_id=1, role="admin")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/trader-plus", headers=headers)
    assert response.status_code == 200
    
    # Analyst should NOT have access to trader endpoints
    token = generate_token(user_id=3, role="analyst")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/trader-plus", headers=headers)
    assert response.status_code == 403
