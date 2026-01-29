import pytest
from uuid import UUID
from services.estate.residue_sweeper import ResidueSweeper

@pytest.fixture
def sweeper():
    return ResidueSweeper()

def test_residue_sweeper_batch(sweeper):
    deceased_id = UUID('12345678-1234-5678-1234-567812345678')
    trust_id = UUID('87654321-4321-8765-4321-876543210987')
    assets = [
        {"id": UUID('00000000-0000-0000-0000-000000000001'), "type": "WATCH"},
        {"id": UUID('00000000-0000-0000-0000-000000000002'), "type": "CASH_ACCOUNT"}
    ]
    # Sweeping miscellaneous assets
    assert sweeper.sweep_to_trust(deceased_id, trust_id, assets) is True
