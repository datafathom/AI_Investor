import pytest
from decimal import Decimal
from services.portfolio.endowment_engine import EndowmentEngine
from services.reporting.global_risk_aggregator import GlobalRiskAggregator

@pytest.fixture
def endowment_engine():
    return EndowmentEngine()

@pytest.fixture
def risk_aggregator():
    return GlobalRiskAggregator()

def test_endowment_allocation_mix(endowment_engine):
    result = endowment_engine.generate_generational_allocation()
    assert result['model_name'] == "YALE_STYLE_ENDOWMENT"
    # Ensure combined private/equities is high
    pcts = result['allocation_pcts']
    assert pcts['private_equity'] == 0.25
    assert pcts['public_equities'] == 0.35

def test_geo_risk_aggregation(risk_aggregator):
    positions = [
        {"country_code": "US", "market_value": Decimal('1000000')},
        {"country_code": "CH", "market_value": Decimal('500000')},
        {"country_code": "US", "market_value": Decimal('500000')}
    ]
    result = risk_aggregator.aggregate_geo_exposure(positions)
    assert result['sovereign_exposure']['US'] == Decimal('1500000.00')
    assert result['sovereign_exposure']['CH'] == Decimal('500000.00')
