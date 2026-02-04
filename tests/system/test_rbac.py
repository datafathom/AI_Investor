"""
RBAC (Role-Based Access Control) Tests
Tests role-based access using FastAPI dependencies.
"""
import pytest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from web.auth_utils import get_current_user, generate_token, decode_token
from typing import Dict, Any


def create_test_app_with_rbac() -> FastAPI:
    """Create a FastAPI app with RBAC-protected routes for testing."""
    app = FastAPI()
    
    # Role hierarchy: admin > trader > analyst > viewer
    ROLE_HIERARCHY = {
        'admin': 4,
        'trader': 3,
        'analyst': 2,
        'viewer': 1
    }
    
    def get_role_level(role: str) -> int:
        return ROLE_HIERARCHY.get(role, 0)
    
    async def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)):
        if get_role_level(current_user.get('role', '')) < get_role_level('admin'):
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    
    async def require_trader(current_user: Dict[str, Any] = Depends(get_current_user)):
        if get_role_level(current_user.get('role', '')) < get_role_level('trader'):
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    
    @app.get("/admin-only")
    async def admin_only(user: Dict[str, Any] = Depends(require_admin)):
        return {"status": "OK", "user": user}
    
    @app.get("/trader-plus")
    async def trader_plus(user: Dict[str, Any] = Depends(require_trader)):
        return {"status": "OK", "user": user}
    
    return app


def test_rbac_access_granted() -> None:
    """Test that admin users can access admin-only routes."""
    app = create_test_app_with_rbac()
    client = TestClient(app)
    
    # Generate Admin Token
    token = generate_token(user_id=1, role="admin")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/admin-only", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "OK"


def test_rbac_access_denied() -> None:
    """Test that non-admin users cannot access admin-only routes."""
    app = create_test_app_with_rbac()
    client = TestClient(app)
    
    # Generate Trader Token (Should be denied for admin-only)
    token = generate_token(user_id=2, role="trader")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/admin-only", headers=headers)
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]


def test_role_hierarchy() -> None:
    """Test that role hierarchy is respected."""
    app = create_test_app_with_rbac()
    client = TestClient(app)
    
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
