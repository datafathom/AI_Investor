import pytest
from services.compliance.role_conflict_validator import RoleConflictValidator
from models.professional_role import ProfessionalRole
from uuid import uuid4

def test_exclusive_role_clash():
    validator = RoleConflictValidator()
    
    wealth_mgr = ProfessionalRole(
        role_code="WEALTH_MANAGER",
        role_name="Wealth Manager",
        role_category="FIDUCIARY",
        fiduciary_standard=True,
        exclusive_with=["BROKER_DEALER"]
    )
    
    broker_dealer = ProfessionalRole(
        role_code="BROKER_DEALER",
        role_name="Broker Dealer",
        role_category="NON_FIDUCIARY",
        fiduciary_standard=False,
        exclusive_with=["WEALTH_MANAGER"]
    )
    
    # User has wealth_mgr, try to add broker_dealer
    assert validator.validate_assignment([wealth_mgr], broker_dealer) == False

def test_valid_role_addition():
    validator = RoleConflictValidator()
    planner = ProfessionalRole(
        role_code="FINANCIAL_PLANNER",
        role_name="Planner",
        role_category="FIDUCIARY",
        fiduciary_standard=True,
        exclusive_with=[]
    )
    wealth_mgr = ProfessionalRole(
        role_code="WEALTH_MANAGER",
        role_name="Wealth Manager",
        role_category="FIDUCIARY",
        fiduciary_standard=True,
        exclusive_with=["BROKER_DEALER"]
    )
    # Planner doesn't clash with Wealth Manager
    assert validator.validate_assignment([planner], wealth_mgr) == True
