"""
Unit tests for Liquidity Monitoring components.
"""
import pytest
from services.market.level2_parser import Level2Parser
from services.market.depth_aggregator import DepthAggregator
from services.risk.liquidity_validator import LiquidityValidator
from services.trading.slippage_estimator import SlippageEstimator

@pytest.fixture
def mock_eur_book():
    """Mock a healthy EUR/USD book."""
    return {
        'symbol': 'EUR/USD',
        'timestamp': '2026-01-25T21:30:00Z',
        'bids': [
            {'price': 1.08500, 'size': 5_000_000},
            {'price': 1.08490, 'size': 3_000_000}
        ],
        'asks': [
            {'price': 1.08502, 'size': 4_000_000},
            {'price': 1.08510, 'size': 2_500_000}
        ]
    }

def test_level2_parsing(mock_eur_book):
    parsed = Level2Parser.parse_depth_event(mock_eur_book)
    assert parsed['symbol'] == 'EUR/USD'
    assert parsed['spread'] == pytest.approx(0.00002)
    assert parsed['mid'] == pytest.approx(1.08501)
    assert len(parsed['bids']) == 2

def test_liquidity_aggregator(mock_eur_book):
    parsed = Level2Parser.parse_depth_event(mock_eur_book)
    metrics = DepthAggregator.get_total_volume_at_depth(parsed, pip_range=0.0005)
    assert metrics['bid_volume'] == 8_000_000
    assert metrics['ask_volume'] == 6_500_000

def test_liquidity_gate_pass(mock_eur_book):
    parsed = Level2Parser.parse_depth_event(mock_eur_book)
    check = LiquidityValidator.is_safe_to_execute(parsed)
    assert check['safe'] is True

def test_liquidity_gate_fail_spread():
    bad_book = {
        'symbol': 'EUR/USD',
        'timestamp': '2026-01-25T21:30:00Z',
        'bids': [{'price': 1.08000, 'size': 5_000_000}],
        'asks': [{'price': 1.08500, 'size': 4_000_000}] # 50 pip spread
    }
    parsed = Level2Parser.parse_depth_event(bad_book)
    check = LiquidityValidator.is_safe_to_execute(parsed)
    assert check['safe'] is False
    assert "High Spread" in check['reason']

def test_slippage_estimation(mock_eur_book):
    parsed = Level2Parser.parse_depth_event(mock_eur_book)
    # Mid = 1.08501
    # Ask Level 1: 1.08502 (4M size)
    # Buy 2M -> Should get 1.08502
    estimation = SlippageEstimator.estimate_slippage(parsed, 2_000_000, 'BUY')
    assert estimation['estimated_vwap'] == 1.08502
    # Slippage = (1.08502 - 1.08501) = 0.00001 = 0.1 pips
    assert pytest.approx(estimation['slippage_pips']) == 0.1
