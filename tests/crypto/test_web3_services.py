import pytest
from services.crypto.lp_tracker_service import LPTrackerService, LPPosition
from services.crypto.gas_service import GasService

class TestWeb3Services:
    
    @pytest.mark.asyncio
    async def test_impermanent_loss_calculation(self):
        service = LPTrackerService()
        
        # Scenario: ETH goes from 1000 to 2000 (2x), USDC stays 1.0
        # Entry Ratio: 1000/1 = 1000
        # Current Ratio: 2000/1 = 2000
        # Price Change = 2.0
        # IL Formula: 2 * sqrt(2) / (1 + 2) - 1 = 2 * 1.414 / 3 - 1 = 2.828 / 3 - 1 = 0.942 - 1 = -0.057 (-5.7%)
        
        pos = LPPosition(
            pool_address="test", token0="ETH", token1="USDC",
            token0_amount=1, token1_amount=1000,
            entry_price_ratio=1000.0, current_price_ratio=2000.0,
            pool_share=0.01
        )
        
        result = await service.calculate_impermanent_loss(pos)
        
        # Check IL percent is roughly -5.7%
        assert -6.0 < result.impermanent_loss_percent < -5.0
        
        # Check LP value is less than HODL value
        assert result.lp_value_usd < result.hodl_value_usd

    @pytest.mark.asyncio
    async def test_gas_spike_detection(self):
        service = GasService()
        
        # Override history to force a stable mean
        # Mean = 20, StdDev = 0
        service._price_history["ethereum"] = [20.0] * 20
        
        # Test normal
        is_spike = await service.detect_spike("ethereum")
        assert not is_spike
        
        # Inject massive spike
        # Current = 100
        # New history: [20...20, 100]
        # Mean approx 24, StdDev approx high. 
        # Z-score of 100 vs (20) should be > 3
        
        # Actually, let's just append to the internal history directly to simulate
        service._price_history["ethereum"].append(100.0)
        
        is_spike = await service.detect_spike("ethereum")
        # With enough stable data, one outlier should trigger
        assert is_spike

    @pytest.mark.asyncio
    async def test_transaction_queue(self):
        service = GasService()
        
        tx = await service.queue_transaction("ethereum", 15.0, 24)
        
        queue = await service.get_queued_transactions()
        assert len(queue) == 1
        assert queue[0].id == tx.id
        assert queue[0].status == "pending"
        assert queue[0].target_gas_gwei == 15.0
