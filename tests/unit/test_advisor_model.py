import pytest
from models.advisor import Advisor, AdvisorCreate
from uuid import UUID

def test_advisor_creation():
    data = {
        "name": "Jane Fiduciary",
        "email": "jane@fiduciary.com",
        "fiduciary_status": True,
        "fiduciary_type": "RIA",
        "registration_type": "SEC",
        "firm_name": "Fiduciary Wealth",
        "fee_structure": "FEE_ONLY"
    }
    advisor = Advisor(**data)
    assert advisor.name == "Jane Fiduciary"
    assert advisor.fiduciary_status == True
    assert isinstance(advisor.id, UUID)
    assert advisor.fee_structure == "FEE_ONLY"

def test_advisor_defaults():
    data = {
        "name": "Bob Broker",
        "email": "bob@broker.com",
        "registration_type": "STATE"
    }
    advisor = Advisor(**data)
    assert advisor.fiduciary_status == False
    assert advisor.aum_under_management == 0.0
