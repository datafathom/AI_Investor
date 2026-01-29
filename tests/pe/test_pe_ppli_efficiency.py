import pytest
from decimal import Decimal
from services.pe.efficiency_engine import EfficiencyEngine
from services.insurance.ppli_efficiency_svc import PPLIEfficiencyService

@pytest.fixture
def pe_engine():
    return EfficiencyEngine()

@pytest.fixture
def ppli_svc():
    return PPLIEfficiencyService()

def test_lbo_value_creation_sim(pe_engine):
    # 10M EBITDA, 20M OpEx, 10% headcount cut, 5% efficiency
    # Savings = 2M + 1M = 3M. New EBITDA = 13M.
    result = pe_engine.simulate_value_creation(
        Decimal('10000000'), Decimal('20000000'), Decimal('0.10'), Decimal('0.05')
    )
    assert result['revised_ebitda'] == Decimal('13000000.00')
    assert result['status'] == "IMPROVED"

def test_ppli_tax_drag_ranking(ppli_svc):
    assets = [
        {"symbol": "HY_DEBT", "yield": Decimal('0.10'), "st_gains_pct": Decimal('0.05')},
        {"symbol": "SPY", "yield": Decimal('0.02'), "st_gains_pct": Decimal('0.01')}
    ]
    # HY_DEBT should have higher drag and be #1
    ranked = ppli_svc.rank_assets_by_tax_drag(assets)
    assert ranked[0]['symbol'] == "HY_DEBT"
    assert ranked[0]['tax_drag'] > ranked[1]['tax_drag']
