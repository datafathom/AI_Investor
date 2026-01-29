from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal

class K1Distribution(BaseModel):
    syndication_id: str
    amount: Decimal
    date: datetime
    type: str  # Rental income, Capital gain, Return of capital
    description: Optional[str] = None

class SyndicationRecord(BaseModel):
    id: str
    name: str
    initial_investment: Decimal
    current_basis: Decimal
    cumulative_distributions: Decimal = Field(default=Decimal("0.0"))
    last_updated: datetime = Field(default_factory=datetime.now)

class SyndicationService:
    def __init__(self):
        # In a real scenario, this would connect to a database
        self.records: Dict[str, SyndicationRecord] = {}
        self.distributions: List[K1Distribution] = []

    def create_syndication(self, name: str, initial_investment: Decimal) -> SyndicationRecord:
        syndication_id = f"SYND_{name.upper().replace(' ', '_')}_{int(datetime.now().timestamp())}"
        record = SyndicationRecord(
            id=syndication_id,
            name=name,
            initial_investment=initial_investment,
            current_basis=initial_investment
        )
        self.records[syndication_id] = record
        return record

    def record_distribution(self, syndication_id: str, amount: Decimal, dist_type: str) -> K1Distribution:
        if syndication_id not in self.records:
            raise ValueError(f"Syndication {syndication_id} not found")
        
        distribution = K1Distribution(
            syndication_id=syndication_id,
            amount=amount,
            date=datetime.now(),
            type=dist_type
        )
        
        record = self.records[syndication_id]
        record.cumulative_distributions += amount
        
        # Basis adjustment: Only 'Return of capital' reduces basis
        if dist_type.lower() == "return of capital":
            record.current_basis -= amount
        
        record.last_updated = datetime.now()
        self.distributions.append(distribution)
        return distribution

    def calculate_tax_recapture(self, syndication_id: str, sale_price: Decimal) -> Dict[str, Decimal]:
        if syndication_id not in self.records:
            raise ValueError(f"Syndication {syndication_id} not found")
            
        record = self.records[syndication_id]
        gain = sale_price - record.current_basis
        recapture = Decimal("0.0")
        
        # Simplified: Recapture is the difference between initial investment and current basis (depreciation)
        if record.initial_investment > record.current_basis:
            recapture = record.initial_investment - record.current_basis
            
        capital_gain = max(Decimal("0.0"), gain - recapture)
        
        return {
            "total_gain": gain,
            "recapture_amount": recapture,
            "capital_gain_amount": capital_gain
        }
