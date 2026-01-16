
import pytest
from services.execution.smart_sor import SmartOrderRouter

class TestSmartOrderRouter:
    
    def test_iceberg_splitting(self):
        sor = SmartOrderRouter()
        
        # Order of 1000 shares (Threshold 500)
        # Should split into ten 100-share batches
        qty = 1000
        strategy = sor.determine_order_strategy("AAPL", qty, 0.01)
        
        assert strategy["execution_style"] == "ICEBERG"
        assert len(strategy["batches"]) == 10
        assert sum(strategy["batches"]) == 1000
        
    def test_small_order_immediate(self):
        sor = SmartOrderRouter()
        
        qty = 50
        strategy = sor.determine_order_strategy("MSFT", qty, 0.01)
        
        assert strategy["execution_style"] == "IMMEDIATE"
        assert len(strategy["batches"]) == 1
        assert strategy["batches"][0] == 50
        
    def test_high_volatility_limit_order(self):
        sor = SmartOrderRouter()
        
        # High Vol (5%) -> Limit Order
        qty = 100
        strategy = sor.determine_order_strategy("TSLA", qty, 0.05)
        
        assert strategy["order_type"] == "LIMIT"
        assert "High Volatility" in strategy["reason"]
