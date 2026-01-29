import pytest
from services.simulation.freeloader_sim import FreeloaderSimulator

def test_efficiency_degradation_low():
    sim = FreeloaderSimulator()
    # 20% passive -> 0.98 efficiency
    eff = sim.simulate_efficiency_degradation(0.2)
    assert eff == 0.98

def test_efficiency_degradation_high():
    sim = FreeloaderSimulator()
    # 90% passive -> (0.93 - (0.2)^2 * 10) = 0.93 - 0.4 = 0.53
    eff = sim.simulate_efficiency_degradation(0.9)
    assert eff == 0.53
    assert sim.suggest_active_pivot(eff) == True
