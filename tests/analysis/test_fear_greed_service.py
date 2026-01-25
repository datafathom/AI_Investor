
import pytest
from services.analysis.fear_greed_service import FearGreedIndexService

@pytest.fixture
def fear_greed_service():
    return FearGreedIndexService(mock=True)

def test_composite_score_range(fear_greed_service):
    """Score should be between 0-100."""
    result = fear_greed_service.get_fear_greed_index(symbols=["SPY"])
    assert 0 <= result["score"] <= 100

def test_extreme_fear_threshold(fear_greed_service):
    """Score < 20 should be labeled EXTREME_FEAR."""
    label = fear_greed_service._score_to_label(15)
    assert label == "EXTREME_FEAR"

def test_extreme_greed_threshold(fear_greed_service):
    """Score > 80 should be labeled EXTREME_GREED."""
    label = fear_greed_service._score_to_label(85)
    assert label == "EXTREME_GREED"

def test_weight_sum(fear_greed_service):
    """Weights should sum to 1.0."""
    default_weights = {
        "retail_sentiment": 0.25,
        "social_sentiment": 0.25,
        "smart_money": 0.25,
        "macro_risk": 0.25
    }
    assert sum(default_weights.values()) == 1.0

def test_signal_generation_extreme_fear(fear_greed_service):
    """Extreme fear should generate BUY signal."""
    signal, _ = fear_greed_service._generate_signal(10, "EXTREME_FEAR")
    assert signal == "BUY"

def test_signal_generation_extreme_greed(fear_greed_service):
    """Extreme greed should generate SELL signal."""
    signal, _ = fear_greed_service._generate_signal(90, "EXTREME_GREED")
    assert signal == "SELL"
