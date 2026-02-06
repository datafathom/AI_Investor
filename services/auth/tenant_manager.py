"""
==============================================================================
FILE: services/auth/tenant_manager.py
ROLE: The Landlord
PURPOSE:
    Manage multi-tenant isolation and role-based access control.
    Ensures data belonging to 'Family A' is never seen by 'Family B'.
==============================================================================
"""

import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Tenant(BaseModel):
    id: str
    name: str
    schema_name: str
    status: str = "active"

class TenantManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TenantManager, cls).__new__(cls)
            cls._instance.tenants = {}
            cls._instance._load_tenants()
        return cls._instance

    def _load_tenants(self):
        # Mocking tenant load from master DB
        self.tenants = {
            "default": Tenant(id="default", name="Primary Portfolio", schema_name="public"),
            "family_alpha": Tenant(id="family_alpha", name="Alpha Family Office", schema_name="tenant_alpha")
        }
        logger.info(f"Loaded {len(self.tenants)} tenants.")

    def get_tenant_by_id(self, tenant_id: str) -> Optional[Tenant]:
        return self.tenants.get(tenant_id)

    def authorize_action(self, user_role: str, action: str) -> bool:
        """
        Simple RBAC check.
        Roles: viewer, trader, admin
        """
        permissions = {
            "admin": ["*"],
            "trader": ["view", "trade", "hedge"],
            "viewer": ["view"]
        }
        
        allowed = permissions.get(user_role, [])
        return "*" in allowed or action in allowed

    def get_current_tenant_schema(self) -> str:
        """Retrieve current tenant schema from Flask global context."""
        from flask import g
        try:
            return getattr(g, 'tenant_schema', 'public')
        except (RuntimeError, AttributeError):
            return "public"

tenant_manager = TenantManager()

