import pytest
from decimal import Decimal
from services.pe.lbo_engine import LBOEngine

@pytest.fixture
def lbo_engine():
    return LBOEngine()

def test_lbo_deal_projection(lbo_engine):
    # Entry: 10M EBITDA at 8x multiple = 80M EV.
    # 40% equity = 32M equity, 48M debt.
    # Exit: 5 years, 10% growth. Exit EBITDA ~ 16.1M.
    # Exit at 9x multiple = 144.9M EV.
    # Debt paydown to 24M. Exit equity = 120.9M.
    # MOIC ~ 3.77x. IRR ~ 30.4%.
    result = lbo_engine.project_deal_returns(
        entry_ebitda=Decimal('10000000'),
        entry_multiple=Decimal('8'),
        equity_contribution_pct=Decimal('0.4'),
        exit_multiple=Decimal('9'),
        years=5,
        revenue_growth_pct=Decimal('0.10')
    )
    assert result['moic'] > Decimal('3.0')
    assert result['irr_pct'] > Decimal('25.0')
