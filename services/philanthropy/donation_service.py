"""
Donation Service - Excess Alpha Routing
Phase 61: Manages automated charitable giving and tax optimization.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import logging
from .charity_client import GivingBlockClient

logger = logging.getLogger(__name__)

@dataclass
class DonationAllocation:
    category: str  # e.g., 'Climate', 'Education', 'Health'
    percentage: float
    amount_usd: float = 0.0

@dataclass
class DonationRecord:
    id: str
    timestamp: datetime
    total_amount: float
    allocations: List[DonationAllocation]
    tax_savings_est: float
    status: str = "COMPLETED"

class DonationService:
    def __init__(self):
        self._history: List[DonationRecord] = []
        self._enough_threshold = 3000000.0  # Default $3M
        self._gb_client = GivingBlockClient()
        logger.info("DonationService initialized with real GivingBlockClient")

    async def calculate_excess_alpha(self, current_net_worth: float, threshold: float = None) -> float:
        """Calculates available excess capital above the 'Enough' threshold."""
        target = threshold or self._enough_threshold
        return max(0.0, current_net_worth - target)

    async def route_excess_alpha(self, amount: float, allocations: List[Dict]) -> DonationRecord:
        """Executes a donation routing operation."""
        import uuid
        
        # Calculate split
        final_allocations = []
        for alloc in allocations:
            category = alloc.get('category', 'General')
            pct = alloc.get('percentage', 0)
            allocated_amt = amount * (pct / 100)
            
            # Execute via GivingBlock
            gb_tx = await self._gb_client.create_donation_transaction(allocated_amt, category)
            
            final_allocations.append(DonationAllocation(
                category=category,
                percentage=pct,
                amount_usd=allocated_amt
            ))
            
        # Estimate tax savings (assuming ~35% effective rate for high net worth)
        tax_savings = amount * 0.35
        
        record = DonationRecord(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            total_amount=amount,
            allocations=final_allocations,
            tax_savings_est=tax_savings
        )
        
        self._history.insert(0, record)
        logger.info(f"Routed ${amount:,.2f} to charity. Est. Tax Savings: ${tax_savings:,.2f}")
        return record

    async def get_donation_history(self) -> List[DonationRecord]:
        return self._history

    async def get_tax_impact_summary(self) -> Dict:
        total_donated = sum(r.total_amount for r in self._history)
        total_savings = sum(r.tax_savings_est for r in self._history)
        return {
            "total_donated_ytd": total_donated,
            "estimated_tax_savings": total_savings,
            "effective_cost": total_donated - total_savings
        }

_donation_service: Optional[DonationService] = None
def get_donation_service() -> DonationService:
    global _donation_service
    if _donation_service is None:
        _donation_service = DonationService()
    return _donation_service
