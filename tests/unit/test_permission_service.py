import pytest
from services.auth.permission_service import PermissionService

def test_permission_check():
    service = PermissionService()
    roles = ["WEALTH_MANAGER"]
    assert service.has_permission(roles, "VIEW_PORTFOLIO") == True
    assert service.has_permission(roles, "PLACE_TRADE") == False

def test_combined_permissions():
    service = PermissionService()
    # Wealth Manager + Asset Manager
    roles = ["WEALTH_MANAGER", "ASSET_MANAGER"]
    assert service.has_permission(roles, "PLACE_TRADE") == True
    assert service.has_permission(roles, "CREATE_ESTATE_PLAN") == True
