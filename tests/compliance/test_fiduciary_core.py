import pytest
from uuid import UUID
from services.compliance.justification_service import JustificationService

@pytest.fixture
def justification_service():
    return JustificationService()

def test_record_rational(justification_service):
    client_id = UUID('12345678-1234-5678-1234-567812345678')
    rec_id = UUID('87654321-4321-8765-4321-876543210987')
    # Should successfully log the justification
    assert justification_service.record_rational(client_id, rec_id, "TAX_LOSS", "Offsetting gains", ["TickerA"]) is True

def test_verify_fiduciary_coverage(justification_service):
    rec_ids = [UUID('00000000-0000-0000-0000-000000000001')]
    result = justification_service.verify_fiduciary_coverage(rec_ids)
    assert result['status'] == "COMPLIANT"
    assert result['missing_justifications_count'] == 0
