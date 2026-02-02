import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch
from services.tax.harvest_service import TaxHarvestService, HarvestCandidate


class TestTaxHarvestService:
    @pytest.mark.asyncio
    async def test_wash_sale_violation_check(self):
        service = TaxHarvestService()
        ticker = "TEST_WASH"
        user_id = "u1"
        
        # Mock trade history: Buy 10 days ago
        ten_days_ago = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
        
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
        
        # Mock _get_portfolio_positions to return test data
        mock_positions = [
            {
                "id": "pos_1",
                "ticker": "TSLA",
                "cost_basis": 8000.0,
                "current_value": 5500.0,
                "unrealized_pl": -2500.0,
                "holding_days": 90
            },
            {
                "id": "pos_2",
                "ticker": "AAPL",
                "cost_basis": 15000.0,
                "current_value": 14200.0,
                "unrealized_pl": -800.0,
                "holding_days": 180
            },
            {
                "id": "pos_3",
                "ticker": "MSFT",
                "cost_basis": 33600.0,
                "current_value": 35100.0,
                "unrealized_pl": 1500.0,  # Gain - won't be harvested
                "holding_days": 400
            }
        ]
        
        service._get_db_positions = AsyncMock(return_value=mock_positions)
        
        candidates = await service.identify_harvest_candidates("default", min_loss=100)
        
        assert len(candidates) > 0
        tsla = next((c for c in candidates if c.ticker == "TSLA"), None)
        assert tsla is not None
        assert abs(tsla.unrealized_loss) >= 2500
        assert tsla.tax_savings_estimate > 0

    @pytest.mark.asyncio
    async def test_capital_gains_projection(self):
        service = TaxHarvestService()
        
        # Mock _get_portfolio_positions to return test data
        mock_positions = [
            {
                "id": "pos_1",
                "ticker": "TSLA",
                "cost_basis": 8000.0,
                "current_value": 5500.0,
                "unrealized_pl": -2500.0,
                "holding_days": 90
            },
            {
                "id": "pos_2",
                "ticker": "AAPL",
                "cost_basis": 15000.0,
                "current_value": 14200.0,
                "unrealized_pl": -800.0,
                "holding_days": 180
            },
        ]
        
        service._get_db_positions = AsyncMock(return_value=mock_positions)
        
        # Hold scenario
        hold_proj = await service.project_capital_gains("default", "hold")
        # Harvest All scenario
        harvest_proj = await service.project_capital_gains("default", "harvest_all")
        
        # Harvest All should result in lower net gains (higher losses offset)
        assert harvest_proj.total_tax_liability <= hold_proj.total_tax_liability
        assert harvest_proj.net_short_term <= hold_proj.net_short_term
