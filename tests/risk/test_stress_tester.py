
import pytest
from services.risk.stress_tester import StressTester

class TestStressTester:
    
    def test_black_swan_simulation(self):
        tester = StressTester()
        
        # Portfolio: 100% Tech
        portfolio = {"NVDA": 1.0}
        
        # Scenario: 2008 Crisis (Tech -50%)
        result = tester.simulate_black_swan(portfolio, "2008_CRISIS")
        
        assert abs(result['pnl_pct'] - (-0.50)) < 0.01
        assert "NVDA" in result['details']

    def test_monte_carlo(self):
        tester = StressTester()
        
        # Run small simulation
        stats = tester.run_monte_carlo(iterations=100)
        
        assert "mean_return" in stats
        assert "worst_case_5pct" in stats
        assert "prob_loss" in stats
        
        # Prob loss should be between 0 and 1
        assert 0.0 <= stats['prob_loss'] <= 1.0
