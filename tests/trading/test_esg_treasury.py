import pytest
from decimal import Decimal
from services.quantitative.esg_displacement_svc import ESGDisplacementService
from services.trading.bank_sweep_executor import BankSweepExecutor

@pytest.fixture
def esg_svc():
    return ESGDisplacementService()

@pytest.fixture
def sweep_svc():
    return BankSweepExecutor()

def test_sin_stock_alpha_scanner(esg_svc):
    assets = [
        {"symbol": "XOM", "sector": "ENERGY", "pe_ratio": Decimal('8'), "fcf_yield": Decimal('0.12')},
        {"symbol": "TSLA", "sector": "TECH", "pe_ratio": Decimal('50'), "fcf_yield": Decimal('0.02')}
    ]
    result = esg_svc.scan_for_sin_stock_alpha(assets)
    assert len(result) == 1
    assert result[0]['symbol'] == "XOM"
    assert result[0]['esg_discount_alpha_score'] == 0.2 # 1 - (8/10)

def test_bank_sweep_order_generation(sweep_svc):
    # $10k cash, $5k buffer -> $5k sweep.
    result = sweep_svc.generate_sweep_orders(Decimal('10000'), reserve_buffer=Decimal('5000'))
    assert len(result) == 1
    assert result[0]['symbol'] == "SGOV"
    assert result[0]['amount'] == Decimal('5000.00')
