"""
Unit tests for Institutional Logic primitives.
"""
import pytest
from services.analysis.order_blocks import OrderBlockDetector
from services.analysis.supply_demand_zones import SupplyDemandDetector
from services.options.gex_calculator import GEXCalculator

@pytest.fixture
def mock_candles():
    """Simulate a clear bullish expansion after a base."""
    return [
        {'symbol': 'EUR/USD', 'timestamp': 'T1', 'open': 1.0800, 'high': 1.0805, 'low': 1.0795, 'close': 1.0800}, # Doji
        {'symbol': 'EUR/USD', 'timestamp': 'T2', 'open': 1.0800, 'high': 1.0805, 'low': 1.0795, 'close': 1.0800}, # Doji
        # T3: The OB Base (Bearish)
        {'symbol': 'EUR/USD', 'timestamp': 'T3', 'open': 1.0800, 'high': 1.0805, 'low': 1.0790, 'close': 1.0795}, 
        # T4: Strong Bullish expansion (Rally)
        {'symbol': 'EUR/USD', 'timestamp': 'T4', 'open': 1.0795, 'high': 1.0900, 'low': 1.0790, 'close': 1.0880},
        {'symbol': 'EUR/USD', 'timestamp': 'T5', 'open': 1.0880, 'high': 1.0910, 'low': 1.0870, 'close': 1.0900},
    ]

def test_order_block_detection(mock_candles):
    obs = OrderBlockDetector.find_order_blocks(mock_candles)
    assert len(obs) >= 1
    assert obs[0]['type'] == 'BULLISH_OB'
    assert obs[0]['price_low'] == 1.0790

def test_supply_demand_detection(mock_candles):
    zones = SupplyDemandDetector.identify_zones(mock_candles)
    assert len(zones) >= 1
    assert zones[0]['type'] == 'DEMAND'
    assert zones[0]['price_high'] == 1.0805

def test_gex_calculation():
    # Spot = 5000 (e.g. SPX)
    chain = [
        {'strike': 5000, 'gamma': 0.1, 'open_interest': 1000, 'type': 'CALL'},
        {'strike': 5000, 'gamma': 0.1, 'open_interest': 1200, 'type': 'PUT'},
        {'strike': 5100, 'gamma': 0.05, 'open_interest': 500, 'type': 'CALL'}
    ]
    # Call GEX at 5000: 0.1 * 1000 * 100 = 10,000
    # Put GEX at 5000: 0.1 * 1200 * 100 = 12,000
    # Total GEX at 5000 strike: 10,000 - 12,000 = -2,000
    
    # Call GEX at 5100: 0.05 * 500 * 100 = 2,500
    
    result = GEXCalculator.calculate_gex(5000, chain)
    assert result['total_gex'] == 500 # (10,000 - 12,000) + 2,500 = 500
    assert result['market_regime'] == 'LONG_GAMMA'
