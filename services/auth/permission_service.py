import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class PermissionService:
    """Checks role-based permissions for system actions."""
    
    def __init__(self):
        # Mock permission map
        self.role_permissions = {
            "WEALTH_MANAGER": ["VIEW_PORTFOLIO", "CREATE_ESTATE_PLAN", "EDIT_TAX_STRATEGY"],
            "ASSET_MANAGER": ["PLACE_TRADE", "VIEW_PORTFOLIO", "REBALANCE_CARGO"],
            "FINANCIAL_PLANNER": ["VIEW_BUDGET", "SIMULATE_RETIREMENT"]
        }

    def has_permission(self, role_codes: List[str], permission: str) -> bool:
        for code in role_codes:
            if permission in self.role_permissions.get(code, []):
                return True
        return False

    def list_effective_permissions(self, role_codes: List[str]) -> List[str]:
        perms = set()
        for code in role_codes:
            perms.update(self.role_permissions.get(code, []))
        return list(perms)
