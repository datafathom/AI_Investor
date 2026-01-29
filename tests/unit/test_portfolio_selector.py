import pytest
from services.portfolio.model_vs_custom import PortfolioSelector

def test_strategy_model():
    selector = PortfolioSelector()
    # 200k -> Model
    assert selector.determine_strategy(200000, "MODERATE") == "MODEL_PORTFOLIO"

def test_strategy_custom():
    selector = PortfolioSelector()
    # 1M -> Custom
    assert selector.determine_strategy(1000000, "AGGRESSIVE") == "CUSTOMIZED"
