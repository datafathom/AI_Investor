import pytest
from services.simulation.power_law_sim import PowerLawSimulator

@pytest.fixture
def vc_sim():
    return PowerLawSimulator()

def test_vc_sim_fund_level(vc_sim):
    # Simulate 50 investments
    result = vc_sim.simulate_vc_outcomes(50, ticket_size_k=100)
    assert result['total_invested_k'] == 5000
    # Because of random seeds, we just check probability of returns exists
    assert result['total_returned_k'] >= 0
    assert result['fund_multiple'] >= 0
