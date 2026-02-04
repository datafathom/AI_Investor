
"""
==============================================================================
FILE: web/middleware/tenant_middleware.py
ROLE: The Border Patrol
PURPOSE:
    Extracts X-Tenant-ID from incoming requests and sets the security context.
    Integrates with TenantManager to validate tenant status.
==============================================================================
"""

import logging
from flask import request, g
from services.auth.tenant_manager import tenant_manager

logger = logging.getLogger(__name__)

def tenant_context_processor():
    """
    Flask middleware to handle tenant isolation.
    To be registered as a before_request handler.
    """
    tenant_id = request.headers.get("X-Tenant-ID", "default")
    
    tenant = tenant_manager.get_tenant_by_id(tenant_id)
    if not tenant:
        logger.warning(f"Access attempted with invalid tenant ID: {tenant_id}")
        # Default to 'default' or block?
        # For now, we allow fallback to 'default' but log the warning.
        g.tenant_id = "default"
        g.tenant_schema = "public"
    else:
        g.tenant_id = tenant.id
        g.tenant_schema = tenant.schema_name
        
    logger.debug(f"Request bound to tenant: {g.tenant_id} (Schema: {g.tenant_schema})")

def init_tenant_middleware(app):
    """Register the middleware with the Flask app."""
    app.before_request(tenant_context_processor)
    logger.info("Multi-tenant middleware initialized.")
