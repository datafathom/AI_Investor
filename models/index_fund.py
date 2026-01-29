from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID, uuid4

class IndexFundBase(BaseModel):
    ticker: str
    name: str
    fund_type: str = "ETF" # ETF, MUTUAL_FUND, INDEX
    benchmark_index: Optional[str] = None
    expense_ratio: float
    aum: Optional[float] = 0.0
    inception_date: Optional[date] = None
    issuer: Optional[str] = None
    asset_class: Optional[str] = "EQUITY"
    sector_focus: Optional[str] = "BROAD_MARKET"
    market_cap_focus: Optional[str] = "LARGE_CAP" # LARGE_CAP, MID_CAP, SMALL_CAP
    geography: Optional[str] = "US"
    tradability: Optional[str] = "HIGHLY_LIQUID"

class IndexFundCreate(IndexFundBase):
    pass

class IndexFund(IndexFundBase):
    id: UUID = Field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
