
import pytest
from services.risk.risk_monitor import RiskMonitor

class TestRiskMonitor:
    
    def test_calculate_var(self):
        monitor = RiskMonitor()
        
        # Portfolio: $100,000
        # Volatility (Daily): 2% (0.02)
        # Z-Score (95%): 1.645
        # VaR = 100k * 0.02 * 1.645 = $3,290
        
        var = monitor.calculate_parametric_var(100000, 0.02)
        assert abs(var - 3290) < 1.0 # Within $1 tolerance
        
    def test_concentration_limits(self):
        monitor = RiskMonitor()
        
        # Scenario: Tech overload
        holdings = [
            {'symbol': 'AAPL', 'sector': 'Tech', 'weight': 0.25}, # > 20% Asset Warning
            {'symbol': 'MSFT', 'sector': 'Tech', 'weight': 0.10}, 
            # Total Tech: 35% > 30% Sector Warning
            {'symbol': 'XOM', 'sector': 'Energy', 'weight': 0.10}
        ]
        
        warnings = monitor.check_concentration_limits(holdings)
        
        assert any("ASSET WARNING: AAPL" in w for w in warnings)
        assert any("SECTOR WARNING: Tech" in w for w in warnings)
        assert not any("XOM" in w for w in warnings)
