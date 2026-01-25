import pytest
import datetime
from services.tax.harvest_service import TaxHarvestService

class TestTaxHarvestService:
    @pytest.mark.asyncio
    async def test_wash_sale_violation_check(self):
        service = TaxHarvestService()
        ticker = "TEST_WASH"
        user_id = "u1"
        
        # Mock trade history: Buy 10 days ago
        now_iso = datetime.datetime.now().isoformat()
        ten_days_ago = (datetime.datetime.now() - datetime.timedelta(days=10)).isoformat()
        
        service._trade_history[f"{user_id}:{ticker}"] = [
            {"date": ten_days_ago, "action": "BUY", "amount": 10}
        ]
        
        # Check wash sale violation (should be true as we bought < 30 days ago)
        result = await service.check_wash_sale_violation(ticker, user_id)
        
        assert result.violates_wash_sale is True
        assert len(result.blocking_trades) == 1

    @pytest.mark.asyncio
    async def test_harvest_candidate_identification(self):
        service = TaxHarvestService()
        
        # Identify candidates from mock portfolio
        # Mock portfolio has AAPL, MSFT, TSLA, etc.
        # TSLA has unrealized loss of -2500
        
        candidates = await service.identify_harvest_candidates("default", min_loss=100)
        
        assert len(candidates) > 0
        tsla = next((c for c in candidates if c.ticker == "TSLA"), None)
        assert tsla is not None
        assert tsla.unrealized_loss >= 2500
        assert tsla.tax_savings_estimate > 0

    @pytest.mark.asyncio
    async def test_capital_gains_projection(self):
        service = TaxHarvestService()
        
        # Hold scenario
        hold_proj = await service.project_capital_gains("default", "hold")
        # Harvest All scenario
        harvest_proj = await service.project_capital_gains("default", "harvest_all")
        
        # Harvest All should result in lower net gains (higher losses offset)
        assert harvest_proj.total_tax_liability < hold_proj.total_tax_liability
        assert harvest_proj.net_short_term < hold_proj.net_short_term
