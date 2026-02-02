import logging
from uuid import uuid4
from services.hr.heir_governance_svc import HeirGovernanceService

logger = logging.getLogger(__name__)

def list_heirs():
    """
    CLI Handler for listing employed family members and their roles.
    """
    # Mock data
    heirs = [
        {"id": str(uuid4()), "name": "James III", "role": "Junior Analyst", "nepotism_flag": True},
        {"id": str(uuid4()), "name": "Sara", "role": "VP Social Impact", "nepotism_flag": True}
    ]
    
    print("\n" + "="*50)
    print("          EMPLOYED DESCENDANTS AUDIT")
    print("="*50)
    for h in heirs:
        status = " [!] CUSHY_JOB" if h['nepotism_flag'] else ""
        print(f"- {h['name']} ({h['role']}){status}")
    print("="*50 + "\n")

def audit_kpi(staff_id: str, hard_score: float, discretion: float):
    """
    CLI Handler for auditing discretionary KPI overrides.
    """
    service = HeirGovernanceService()
    final = service.apply_discretionary_kpi_override(staff_id, hard_score, discretion)
    
    print("\n" + "="*50)
    print(f"          KPI AUDIT: {staff_id}")
    print("="*50)
    print(f"Hard KPI Score:    {hard_score}")
    print(f"Family Discretion: {discretion}")
    print("-" * 50)
    print(f"FINAL OVERRIDE:    {final}")
    print(f"Adjustment:        +{round(final - hard_score, 2)}")
    print("="*50 + "\n")
