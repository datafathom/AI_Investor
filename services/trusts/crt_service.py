from typing import Dict, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class CRTConfig(BaseModel):
    trust_id: str
    trust_type: Literal["CRAT", "CRUT"] # Annuity vs Unitrust
    initial_value: Decimal
    payout_rate: Decimal # e.g., 0.05 for 5%
    start_date: datetime = Field(default_factory=datetime.now)
    term_years: Optional[int] = None
    charity_name: str

    @validator("payout_rate")
    def validate_payout_rate(cls, v):
        if v < Decimal("0.05") or v > Decimal("0.50"):
            raise ValueError("Payout rate must be between 5% and 50% (IRC 664)")
        return v

class CRTService:
    def __init__(self):
        self.trusts: Dict[str, CRTConfig] = {}

    def create_crt(self, config: CRTConfig) -> CRTConfig:
        # IRC 664: 10% Remainder Rule (Simplified check)
        # In practice, this requires actuarial tables (IRS Pub 1457/1458)
        # We'll implement a placeholder check
        if not self._check_10_percent_remainder(config):
             raise ValueError("Trust fails the 10% remainder rule (IRC 664)")
             
        self.trusts[config.trust_id] = config
        return config

    def _check_10_percent_remainder(self, config: CRTConfig) -> bool:
        # Placeholder for complex actuarial calculation
        # Rule of thumb: payout_rate * term_years < threshold
        # For now, we assume it passes if payout rate is reasonable for the term
        if config.term_years and config.payout_rate * config.term_years > Decimal("0.8"):
            return False
        return True

    def calculate_distribution(self, trust_id: str, current_value: Decimal) -> Decimal:
        if trust_id not in self.trusts:
            raise ValueError(f"Trust {trust_id} not found")
        
        config = self.trusts[trust_id]
        if config.trust_type == "CRAT":
            # Fixed annuity based on initial value
            return config.initial_value * config.payout_rate
        else:
            # Variable unitrust based on current value
            return current_value * config.payout_rate
