import logging
from typing import List, Optional
from uuid import UUID
from schemas.index_fund import IndexFund, IndexFundCreate

logger = logging.getLogger(__name__)

class IndexFundService:
    """Manages the index fund master database."""
    
    def __init__(self):
        self.mock_db = {}

    def add_fund(self, fund_data: IndexFundCreate) -> IndexFund:
        new_fund = IndexFund(**fund_data.model_dump())
        self.mock_db[new_fund.ticker] = new_fund
        logger.info(f"FUND_LOG: Added fund {new_fund.ticker} ({new_fund.name})")
        return new_fund

    def get_fund_by_ticker(self, ticker: str) -> Optional[IndexFund]:
        return self.mock_db.get(ticker.upper())

    def list_funds(self, fund_type: Optional[str] = None) -> List[IndexFund]:
        if fund_type:
            return [f for f in self.mock_db.values() if f.fund_type == fund_type]
        return list(self.mock_db.values())

    def update_aum(self, ticker: str, new_aum: float):
        fund = self.get_fund_by_ticker(ticker)
        if fund:
            fund.aum = new_aum
            logger.info(f"FUND_LOG: Updated AUM for {ticker} to ${new_aum:,.2f}")
            return fund
        return None
