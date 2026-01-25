import pytest
from services.analysis.fixed_income_service import FixedIncomeService, Bond

class TestFixedIncomeService:
    @pytest.mark.asyncio
    async def test_wal_calculation(self):
        service = FixedIncomeService()
        
        # Bond 1: $100k, 2 years
        # Bond 2: $100k, 4 years
        # WAL should be ( (100k*2) + (100k*4) ) / 200k = (200k + 400k) / 200k = 600k / 200k = 3.0 years
        ladder = [
            Bond(id="b1", name="B1", par_value=100000, coupon_rate=0.05, maturity_years=2),
            Bond(id="b2", name="B2", par_value=100000, coupon_rate=0.05, maturity_years=4)
        ]
        
        wal = await service.calculate_weighted_average_life(ladder)
        assert wal == 3.0

    @pytest.mark.asyncio
    async def test_liquidity_gaps(self):
        service = FixedIncomeService()
        
        # Bond maturing in Year 1 and Year 3
        # Gap should be Year 2 (and others up to 30)
        ladder = [
            Bond(id="b1", name="B1", par_value=100, coupon_rate=0, maturity_years=1),
            Bond(id="b2", name="B2", par_value=100, coupon_rate=0, maturity_years=3)
        ]
        
        gaps = await service.detect_liquidity_gaps(ladder)
        assert 2 in gaps
        assert 1 not in gaps
        assert 3 not in gaps

    @pytest.mark.asyncio
    async def test_rate_shock_impact(self):
        service = FixedIncomeService()
        
        # We use a mock portfolio inside the service for rate shock test simplicity
        # or we could mock `_get_mock_portfolio` if we wanted specific bonds.
        # But let's trust the internal mock for a generic sanity check that shock != 0.
        
        impact = await service.get_rate_shock_impact("default", 100)
        
        assert impact.shock_basis_points == 100
        # Price should drop when rates rise
        assert impact.percentage_change < 0 
        assert impact.dollar_change < 0
        assert impact.portfolio_value_after < impact.portfolio_value_before
