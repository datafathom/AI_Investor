import pytest
from services.market.futures_service import FuturesService, FuturesCurve, FuturesContract

class TestFuturesService:
    
    @pytest.mark.asyncio
    async def test_contango_detection(self):
        service = FuturesService()
        
        # Construct Contango Curve (Future > Spot)
        spot = 100.0
        contracts = [
            FuturesContract("F1", "2026-01-01", 101.0, 100, 100),
            FuturesContract("F2", "2026-02-01", 102.0, 100, 100)
        ]
        curve = FuturesCurve("TEST", "Test", contracts, spot, "unknown")
        
        start_is_contango = await service.detect_contango(curve)
        assert start_is_contango
        
        # Construct Backwardation Curve (Future < Spot)
        spot_back = 100.0
        contracts_back = [
            FuturesContract("F1", "2026-01-01", 99.0, 100, 100),
            FuturesContract("F2", "2026-02-01", 98.0, 100, 100)
        ]
        curve_back = FuturesCurve("TEST", "Test", contracts_back, spot_back, "unknown")
        
        is_contango_back = await service.detect_contango(curve_back)
        assert not is_contango_back

    @pytest.mark.asyncio
    async def test_roll_yield_calculation(self):
        service = FuturesService()
        
        # Front = 100, Second = 102 (Contango)
        # Yield should be negative. (100 - 102) / 100 = -0.02 * 12 * 100 = -24%
        contracts = [
            FuturesContract("F1", "2026-01-01", 100.0, 100, 100),
            FuturesContract("F2", "2026-02-01", 102.0, 100, 100)
        ]
        curve = FuturesCurve("TEST", "Test", contracts, 100.0, "unknown")
        
        yield_val = await service.calculate_roll_yield(curve)
        assert yield_val < 0
        assert yield_val == -24.0

    @pytest.mark.asyncio
    async def test_crack_spread(self):
        service = FuturesService()
        
        spread = await service.calculate_crack_spread()
        assert spread.name == "3-2-1 Crack Spread"
        assert spread.value is not None
        assert "crude_oil" in spread.components
