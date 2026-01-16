
import pytest
from services.risk.circuit_breaker import CircuitBreaker

class TestCircuitBreaker:
    
    def test_portfolio_freeze(self):
        cb = CircuitBreaker()
        
        # Normal PnL (-1%) -> No Freeze
        assert cb.check_portfolio_freeze(-0.01) is False
        assert cb.portfolio_frozen is False
        
        # Crash PnL (-4%) -> Freeze!
        assert cb.check_portfolio_freeze(-0.04) is True
        assert cb.portfolio_frozen is True
        assert "exceeded limit" in cb.freeze_reason
        
        # Reset
        cb.reset()
        assert cb.portfolio_frozen is False

    def test_asset_kill_switch(self):
        cb = CircuitBreaker()
        
        # Prices: 100 -> 95 -> 92 (Max drop 8%) -> OK
        prices_ok = [100.0, 95.0, 92.0]
        assert cb.check_asset_kill_switch('AAPL', prices_ok) is False
        
        # Prices: 100 -> 95 -> 85 (Max drop 15%) -> KILL
        prices_crash = [100.0, 95.0, 85.0]
        assert cb.check_asset_kill_switch('TSLA', prices_crash) is True
        assert 'TSLA' in cb.frozen_assets
