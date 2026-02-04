from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID, uuid4

class SpendingCategoryBase(BaseModel):
    user_id: UUID
    month: date
    housing: float = 0.0
    transportation: float = 0.0
    food_groceries: float = 0.0
    food_dining: float = 0.0
    healthcare: float = 0.0
    insurance: float = 0.0
    education: float = 0.0
    childcare: float = 0.0
    entertainment: float = 0.0
    travel: float = 0.0
    subscriptions: float = 0.0
    debt_payments: float = 0.0
    savings_contributions: float = 0.0
    investments: float = 0.0

class SpendingCategory(SpendingCategoryBase):
    id: UUID = Field(default_factory=uuid4)
    total_spending: float = 0.0
    savings_rate: Optional[float] = 0.0
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class SpendingBenchmark(BaseModel):
    income_bracket: str
    category: str
    benchmark_percentage: float
    benchmark_amount: Optional[float] = 0.0
    peer_group: str = "UPPER_MIDDLE"
