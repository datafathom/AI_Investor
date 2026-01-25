"""
==============================================================================
FILE: services/estate/estate_planning_service.py
ROLE: Estate Planning Service
PURPOSE: Manages estate planning with beneficiary management, asset allocation
         by beneficiary, and tax implications analysis.

INTEGRATION POINTS:
    - PortfolioService: Current portfolio value
    - TaxService: Estate tax calculations
    - UserService: Beneficiary information
    - EstateAPI: Estate planning endpoints
    - FrontendEstate: Estate dashboard

FEATURES:
    - Beneficiary management
    - Asset allocation by beneficiary
    - Estate tax calculations
    - Trust account support

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.estate import (
    EstatePlan, Beneficiary, BeneficiaryType
)
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class EstatePlanningService:
    """
    Service for estate planning and beneficiary management.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.cache_service = get_cache_service()
        self.estate_tax_exemption = 12000000.0  # 2024 federal exemption
        self.estate_tax_rate = 0.40  # Top estate tax rate
        
    async def create_estate_plan(
        self,
        user_id: str,
        beneficiaries: List[Dict],
        trust_accounts: Optional[List[Dict]] = None
    ) -> EstatePlan:
        """
        Create estate plan with beneficiaries.
        
        Args:
            user_id: User identifier
            beneficiaries: List of beneficiary dictionaries
            trust_accounts: Optional trust account information
            
        Returns:
            EstatePlan with allocations and tax calculations
        """
        logger.info(f"Creating estate plan for user {user_id}")
        
        # Get total estate value
        total_estate_value = await self._get_estate_value(user_id)
        
        # Convert beneficiaries to Beneficiary objects
        beneficiary_objects = []
        for ben_data in beneficiaries:
            beneficiary = Beneficiary(
                beneficiary_id=f"ben_{user_id}_{datetime.utcnow().timestamp()}",
                user_id=user_id,
                created_date=datetime.utcnow(),
                updated_date=datetime.utcnow(),
                **ben_data
            )
            beneficiary_objects.append(beneficiary)
        
        # Validate allocations sum to 100%
        total_allocation = sum(b.allocation_percentage for b in beneficiary_objects)
        if abs(total_allocation - 100.0) > 0.01:
            raise ValueError(f"Beneficiary allocations must sum to 100%, got {total_allocation}%")
        
        # Calculate allocations in dollars
        for beneficiary in beneficiary_objects:
            beneficiary.allocation_amount = total_estate_value * (beneficiary.allocation_percentage / 100.0)
        
        # Calculate estate tax
        estimated_estate_tax = await self._calculate_estate_tax(total_estate_value)
        
        plan = EstatePlan(
            plan_id=f"estate_{user_id}_{datetime.utcnow().timestamp()}",
            user_id=user_id,
            total_estate_value=total_estate_value,
            beneficiaries=beneficiary_objects,
            trust_accounts=trust_accounts or [],
            estimated_estate_tax=estimated_estate_tax,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        
        # Cache plan
        cache_key = f"estate_plan:{user_id}"
        self.cache_service.set(cache_key, plan.dict(), ttl=86400)
        
        return plan
    
    async def update_beneficiary(
        self,
        plan_id: str,
        beneficiary_id: str,
        updates: Dict
    ) -> Beneficiary:
        """
        Update beneficiary in estate plan.
        
        Args:
            plan_id: Estate plan identifier
            beneficiary_id: Beneficiary identifier
            updates: Dictionary of updates
            
        Returns:
            Updated Beneficiary
        """
        # Get plan
        plan = await self._get_estate_plan(plan_id)
        if not plan:
            raise ValueError(f"Estate plan {plan_id} not found")
        
        # Find and update beneficiary
        beneficiary = next((b for b in plan.beneficiaries if b.beneficiary_id == beneficiary_id), None)
        if not beneficiary:
            raise ValueError(f"Beneficiary {beneficiary_id} not found")
        
        # Update fields
        for key, value in updates.items():
            if hasattr(beneficiary, key):
                setattr(beneficiary, key, value)
        
        beneficiary.updated_date = datetime.utcnow()
        
        # Recalculate allocations
        total_allocation = sum(b.allocation_percentage for b in plan.beneficiaries)
        if abs(total_allocation - 100.0) > 0.01:
            raise ValueError(f"Beneficiary allocations must sum to 100%, got {total_allocation}%")
        
        # Update allocation amounts
        for b in plan.beneficiaries:
            b.allocation_amount = plan.total_estate_value * (b.allocation_percentage / 100.0)
        
        # Save updated plan
        await self._save_estate_plan(plan)
        
        return beneficiary
    
    async def calculate_estate_tax(
        self,
        estate_value: float,
        exemptions: Optional[float] = None
    ) -> Dict:
        """
        Calculate estate tax liability.
        
        Args:
            estate_value: Total estate value
            exemptions: Optional exemption amount (default: federal exemption)
            
        Returns:
            Tax calculation breakdown
        """
        exemption = exemptions or self.estate_tax_exemption
        taxable_estate = max(0, estate_value - exemption)
        
        # Progressive estate tax brackets (simplified)
        if taxable_estate <= 0:
            tax = 0.0
        elif taxable_estate <= 1000000:
            tax = taxable_estate * 0.18
        elif taxable_estate <= 3000000:
            tax = 180000 + (taxable_estate - 1000000) * 0.28
        elif taxable_estate <= 5000000:
            tax = 740000 + (taxable_estate - 3000000) * 0.32
        else:
            tax = 1380000 + (taxable_estate - 5000000) * self.estate_tax_rate
        
        effective_rate = (tax / estate_value * 100) if estate_value > 0 else 0.0
        
        return {
            'estate_value': estate_value,
            'exemption': exemption,
            'taxable_estate': taxable_estate,
            'estate_tax': tax,
            'effective_rate': effective_rate,
            'after_tax_value': estate_value - tax
        }
    
    async def _get_estate_value(self, user_id: str) -> float:
        """Get total estate value for user."""
        # In production, aggregate from portfolio, real estate, etc.
        return 2000000.0  # Mock value
    
    async def _calculate_estate_tax(self, estate_value: float) -> float:
        """Calculate estimated estate tax."""
        tax_calc = await self.calculate_estate_tax(estate_value)
        return tax_calc['estate_tax']
    
    async def _get_estate_plan(self, plan_id: str) -> Optional[EstatePlan]:
        """Get estate plan from cache."""
        # Extract user_id from plan_id or search all plans
        # Simplified: search cache
        return None  # Would implement proper lookup
    
    async def _save_estate_plan(self, plan: EstatePlan):
        """Save estate plan to cache."""
        cache_key = f"estate_plan:{plan.user_id}"
        self.cache_service.set(cache_key, plan.dict(), ttl=86400)


# Singleton instance
_estate_planning_service: Optional[EstatePlanningService] = None


def get_estate_planning_service() -> EstatePlanningService:
    """Get singleton estate planning service instance."""
    global _estate_planning_service
    if _estate_planning_service is None:
        _estate_planning_service = EstatePlanningService()
    return _estate_planning_service
