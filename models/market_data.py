
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

class Quote(BaseModel):
    """Real-time stock quote data model."""
    symbol: str
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    price: float = 0.0
    volume: int = 0
    latest_trading_day: Optional[str] = None
    previous_close: float = 0.0
    change: float = 0.0
    change_percent: str = "0.00%"
    timestamp: datetime = Field(default_factory=datetime.now)
    source: str = "alpha_vantage"

class OHLCV(BaseModel):
    """OHLCV bar data model."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    adjusted_close: Optional[float] = None
    volume: int
    dividend: Optional[float] = None
    split_coefficient: Optional[float] = None

class Earnings(BaseModel):
    """Earnings calendar entry."""
    symbol: str
    name: Optional[str] = None
    report_date: str
    fiscal_date_ending: Optional[str] = None
    estimate: Optional[float] = None
    currency: str = "USD"

class MarketDataHealth(BaseModel):
    """Health status of market data sources."""
    source_name: str
    status: str
    requests_remaining: dict
    overall_status: str
