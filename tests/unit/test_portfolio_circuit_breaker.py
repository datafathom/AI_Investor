"""
Unit tests for Portfolio Circuit Breaker Logic.
Verifies aggregation of system losses and global trade blocking (Zen Mode).
"""
import pytest
from decimal import Decimal
from services.risk.drawdown_aggregator import DrawdownAggregator
from services.risk.portfolio_circuit_breaker import PortfolioCircuitBreaker

def test_drawdown_calculation():
    agg = DrawdownAggregator(start_of_day_equity=Decimal("100000.00"))
    
    # 1% drawdown (unrealized)
    agg.update_pnl(realized=Decimal("0.00"), unrealized=Decimal("-1000.00"))
    assert agg.get_total_drawdown_pct() == 0.01
    assert agg.is_3_percent_breached() == False

    # 3% drawdown (mix)
    agg.update_pnl(realized=Decimal("-1500.00"), unrealized=Decimal("-1500.00"))
    assert agg.get_total_drawdown_pct() == 0.03
    assert agg.is_3_percent_breached() == True

    # Recovery (unrealized bounce)
    agg.update_pnl(realized=Decimal("-1500.00"), unrealized=Decimal("1000.00"))
    assert agg.get_total_drawdown_pct() == 0.005 # 100k - 1.5k + 1k = 99.5k (0.5% loss)
    assert agg.is_3_percent_breached() == False

def test_circuit_breaker_enforcement():
    agg = DrawdownAggregator(start_of_day_equity=Decimal("100000.00"))
    breaker = PortfolioCircuitBreaker(agg)
    
    # Normal State
    allowed, _ = breaker.is_trading_allowed()
    assert allowed == True

    # Breach State (4% Loss)
    agg.update_pnl(Decimal("-4000.00"), Decimal("0"))
    allowed, reason = breaker.is_trading_allowed()
    assert allowed == False
    assert "ZEN_MODE" in reason

def test_administrative_lock():
    agg = DrawdownAggregator(start_of_day_equity=Decimal("100000.00"))
    breaker = PortfolioCircuitBreaker(agg)
    
    breaker.set_administrative_lock(True)
    allowed, reason = breaker.is_trading_allowed()
    assert allowed == False
    assert "Manual administrative lock" in reason
