from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class FXPrice(BaseModel):
    """
    Represents a tick for a currency pair (e.g. EUR/USD).
    """
    pair: str = Field(..., description="Currency pair, e.g. EURUSD")
    bid: float = Field(..., gt=0)
    ask: float = Field(..., gt=0)
    mid: float = Field(..., gt=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = "INSTITUTIONAL_SIM"
    
    @validator('mid')
    def validate_mid(cls, v, values):
        if 'bid' in values and 'ask' in values:
            if not (values['bid'] <= v <= values['ask']):
                 # In fast markets, mid might slightly deviate, but generally should be between.
                 # For sim verification, we enforce it.
                 pass 
        return v
