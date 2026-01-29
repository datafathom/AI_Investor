from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from decimal import Decimal

class QOZInvestment(BaseModel):
    investment_id: str
    amount: Decimal
    investment_date: datetime
    zone_id: str
    description: Optional[str] = None

class QOZService:
    def __init__(self):
        self.investments: Dict[str, QOZInvestment] = {}
        self.CLIFF_DATE_2026 = datetime(2026, 12, 31)

    def add_investment(self, investment: QOZInvestment):
        self.investments[investment.investment_id] = investment
        return investment

    def get_adjusted_basis(self, investment_id: str, current_date: datetime = None) -> Decimal:
        if investment_id not in self.investments:
            raise ValueError(f"Investment {investment_id} not found")
        
        if current_date is None:
            current_date = datetime.now()
            
        inv = self.investments[investment_id]
        years_held = (current_date - inv.investment_date).days / 365.25
        
        basis = Decimal("0.0") # Initial basis in deferred gain is 0
        
        # 5-year step up: 10%
        if years_held >= 5:
            basis += inv.amount * Decimal("0.10")
            
        # 7-year step up: +5% (total 15%)
        # NOTE: Investment must have been made by certain dates to hit these before 2026
        if years_held >= 7:
            basis += inv.amount * Decimal("0.05")
            
        return basis

    def calculate_taxable_gain_2026(self, investment_id: str) -> Decimal:
        """
        Calculates the gain that must be recognized on Dec 31, 2026.
        """
        if investment_id not in self.investments:
            raise ValueError(f"Investment {investment_id} not found")
            
        inv = self.investments[investment_id]
        basis_at_cliff = self.get_adjusted_basis(investment_id, self.CLIFF_DATE_2026)
        
        taxable_gain = inv.amount - basis_at_cliff
        return max(Decimal("0.0"), taxable_gain)

    def is_eligible_for_full_exclusion(self, investment_id: str, current_date: datetime = None) -> bool:
        """
        Check if 10-year holding period met for full basis step-up to FMV.
        """
        if investment_id not in self.investments:
            raise ValueError(f"Investment {investment_id} not found")
            
        if current_date is None:
            current_date = datetime.now()
            
        inv = self.investments[investment_id]
        years_held = (current_date - inv.investment_date).days / 365.25
        return years_held >= 10
