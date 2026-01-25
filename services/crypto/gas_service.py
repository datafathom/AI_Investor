"""
Gas Service - Network Fee Optimization

Phase 51: Monitors gas prices across networks and provides optimization
strategies for transaction timing.

Features:
- Real-time gas price monitoring
- Spike detection (> 3 std dev from mean)
- Optimal execution window recommendations
- Meta-transaction queuing support

Usage:
    service = GasService()
    gas = await service.get_current_gas("ethereum")
    should_wait = await service.detect_spike("ethereum")
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import logging
import random

logger = logging.getLogger(__name__)


class GasUrgency(Enum):
    """Gas price urgency levels."""
    LOW = "low"  # ~30min confirmation
    MEDIUM = "medium"  # ~5min confirmation
    HIGH = "high"  # ~30sec confirmation
    INSTANT = "instant"  # Next block


@dataclass
class GasMetrics:
    """Current gas price metrics for a chain."""
    chain: str
    base_fee_gwei: float
    priority_fee_gwei: float
    estimated_usd: Dict[str, float]  # Urgency -> USD cost
    trend: str  # "rising", "falling", "stable"
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TimeWindow:
    """Optimal execution time window."""
    start_time: str
    end_time: str
    expected_savings_percent: float
    confidence: float


@dataclass
class QueuedTransaction:
    """Transaction queued for optimal execution."""
    id: str
    chain: str
    target_gas_gwei: float
    expires_at: str
    status: str  # "pending", "executed", "expired"


class GasService:
    """
    Service for gas price monitoring and optimization.
    
    Provides real-time gas data, spike detection, and
    optimal execution window recommendations.
    """
    
    def __init__(self) -> None:
        """Initialize the gas service."""
        self._price_history: Dict[str, List[float]] = {
            "ethereum": self._generate_mock_history(),
            "polygon": [0.01 + random.uniform(-0.005, 0.005) for _ in range(100)],
            "arbitrum": [0.1 + random.uniform(-0.05, 0.05) for _ in range(100)],
        }
        self._queued_txs: Dict[str, QueuedTransaction] = {}
        logger.info("GasService initialized")
    
    def _generate_mock_history(self) -> List[float]:
        """Generate mock gas price history."""
        base = 25
        history = []
        for _ in range(100):
            base += random.uniform(-2, 2)
            base = max(10, min(base, 100))  # Keep in realistic range
            history.append(base)
        return history
    
    async def get_current_gas(self, chain: str) -> GasMetrics:
        """
        Get current gas prices for a chain.
        
        Args:
            chain: Blockchain network name
            
        Returns:
            GasMetrics with current prices and trends
        """
        history = self._price_history.get(chain.lower(), [25])
        current_base = history[-1] if history else 25
        
        # Generate priority fees based on urgency
        priority_fees = {
            GasUrgency.LOW: 0.5,
            GasUrgency.MEDIUM: 1.5,
            GasUrgency.HIGH: 3.0,
            GasUrgency.INSTANT: 5.0,
        }
        
        # Calculate USD costs (assuming 21000 gas for simple transfer)
        eth_price = 3250.0
        gas_units = 21000
        
        estimated_usd = {}
        for urgency, priority in priority_fees.items():
            total_gwei = current_base + priority
            eth_cost = (total_gwei * gas_units) / 1e9
            estimated_usd[urgency.value] = round(eth_cost * eth_price, 2)
        
        # Determine trend
        if len(history) >= 3:
            recent = history[-3:]
            if recent[-1] > recent[0] * 1.1:
                trend = "rising"
            elif recent[-1] < recent[0] * 0.9:
                trend = "falling"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        return GasMetrics(
            chain=chain.lower(),
            base_fee_gwei=round(current_base, 2),
            priority_fee_gwei=1.5,  # Medium default
            estimated_usd=estimated_usd,
            trend=trend
        )
    
    async def detect_spike(self, chain: str) -> bool:
        """
        Detect if current gas is > 3 std dev above 24h mean.
        
        Args:
            chain: Blockchain network
            
        Returns:
            True if spike detected
        """
        history = self._price_history.get(chain.lower(), [])
        
        if len(history) < 10:
            return False
        
        mean = sum(history) / len(history)
        variance = sum((x - mean) ** 2 for x in history) / len(history)
        std_dev = variance ** 0.5
        
        current = history[-1]
        z_score = (current - mean) / std_dev if std_dev > 0 else 0
        
        return z_score > 3.0
    
    async def get_optimal_execution_window(self) -> TimeWindow:
        """
        Get optimal time window for transaction execution.
        
        Analyzes historical patterns to find lowest gas periods.
        
        Returns:
            TimeWindow with expected savings
        """
        # Mock optimal window (typically weekends, early UTC)
        now = datetime.now()
        
        # Simulate finding optimal window
        optimal_start = now.replace(hour=4, minute=0, second=0)
        if optimal_start < now:
            optimal_start += timedelta(days=1)
        
        optimal_end = optimal_start + timedelta(hours=3)
        
        return TimeWindow(
            start_time=optimal_start.isoformat(),
            end_time=optimal_end.isoformat(),
            expected_savings_percent=25.0,
            confidence=0.72
        )
    
    async def queue_transaction(
        self,
        chain: str,
        target_gas_gwei: float,
        ttl_hours: int = 24
    ) -> QueuedTransaction:
        """
        Queue transaction for execution when gas hits target.
        
        Args:
            chain: Target blockchain
            target_gas_gwei: Maximum gas price to accept
            ttl_hours: Hours until expiration
            
        Returns:
            QueuedTransaction tracking object
        """
        tx_id = f"q-{datetime.now().timestamp()}"
        expires = datetime.now() + timedelta(hours=ttl_hours)
        
        tx = QueuedTransaction(
            id=tx_id,
            chain=chain.lower(),
            target_gas_gwei=target_gas_gwei,
            expires_at=expires.isoformat(),
            status="pending"
        )
        
        self._queued_txs[tx_id] = tx
        logger.info(f"Queued transaction {tx_id} for {target_gas_gwei} gwei")
        
        return tx
    
    async def get_queued_transactions(self) -> List[QueuedTransaction]:
        """Get all queued transactions."""
        return list(self._queued_txs.values())
    
    def get_24h_stats(self, chain: str) -> Dict[str, float]:
        """Get 24h gas statistics for a chain."""
        history = self._price_history.get(chain.lower(), [25])
        
        if not history:
            return {"min": 0, "max": 0, "mean": 0, "current": 0}
        
        return {
            "min": round(min(history), 2),
            "max": round(max(history), 2),
            "mean": round(sum(history) / len(history), 2),
            "current": round(history[-1], 2)
        }
