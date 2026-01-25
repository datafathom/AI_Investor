import pytest
from services.analysis.attribution_service import AttributionService, DateRange

class TestAttributionService:
    @pytest.mark.asyncio
    async def test_brinson_calculation(self):
        service = AttributionService()
        
        # Override mock data for predictable testing
        service._benchmarks = {
            "test_bm": {
                "name": "Test Benchmark",
                "sectors": {
                    "Information Technology": {"weight": 0.50, "return": 0.10},  # 50% weight, 10% return
                    "Energy": {"weight": 0.50, "return": 0.05} # 50% weight, 5% return
                }
            }
        }
        # Benchmark Total Return = (0.5*0.10) + (0.5*0.05) = 0.05 + 0.025 = 0.075 (7.5%)
        
        # Mock Portfolio:
        # Information Technology: 60% weight (Overweight), 12% return (Outperformed)
        # Energy: 40% weight (Underweight), 4% return (Underperformed)
        service._get_mock_portfolio_data = lambda pid: {
            "Information Technology": {"weight": 0.60, "return": 0.12},
            "Energy": {"weight": 0.40, "return": 0.04}
        }
        
        result = await service.calculate_brinson_attribution(
            "test_port", 
            "test_bm", 
            DateRange("2025-01-01", "2025-01-31")
        )
        
        # 1. Information Technology Sector Analysis
        # Allocation = (wp - wb) * (rb - R_b)
        #            = (0.6 - 0.5) * (0.10 - 0.075) = 0.1 * 0.025 = 0.0025 = 25bps
        # Selection  = wb * (rp - rb)
        #            = 0.5 * (0.12 - 0.10) = 0.5 * 0.02 = 0.01 = 100bps
        # Interaction = (wp - wb) * (rp - rb)
        #             = (0.6 - 0.5) * (0.12 - 0.10) = 0.1 * 0.02 = 0.002 = 20bps
        
        tech = next(s for s in result.sector_attributions if s.sector == "Information Technology")
        
        # Floating point tolerance
        assert abs(tech.allocation_effect - 25.0) < 0.1
        assert abs(tech.selection_effect - 100.0) < 0.1
        assert abs(tech.interaction_effect - 20.0) < 0.1
        
        # 2. Total Analysis
        # Active Return = Portfolio Return - Benchmark Return
        # Portfolio Return = (0.6*0.12) + (0.4*0.04) = 0.072 + 0.016 = 0.088 (8.8%)
        # Benchmark Return = 7.5%
        # Active = 1.3% = 130bps
        
        assert abs(result.total_active_return - 130.0) < 0.5

    @pytest.mark.asyncio
    async def test_get_available_benchmarks(self):
        service = AttributionService()
        bms = service.get_available_benchmarks()
        ids = [b['id'] for b in bms]
        assert "sp500" in ids
        assert "nasdaq" in ids
