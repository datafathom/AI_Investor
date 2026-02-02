import logging
import yfinance as yf
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SECScraper:
    """
    Service to fetch financial data and filings.
    Currently uses yfinance for financials.
    Future: Integrate sec-api or similar for robust 10-K text.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SECScraper, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("SECScraper initialized (Powered by yfinance)")

    def get_latest_filing_text(self, ticker: str, doc_type: str = '10-K') -> str:
        """
        Retrieves the text content of a latest filing.
        """
        logger.info(f"SEC Scraper: Retrieving latest {doc_type} for {ticker}...")
        
        # TODO: Implement real EDGAR scraping or use a paid API like 'sec-api'
        # yfinance does not provide full 10-K text.
        # Returning a placeholder that clearly indicates source limitation.
        
        return f"""
        [REAL DATA LIMITATION]
        Full {doc_type} text not available via free public APIs without rate limits/parsing complex XBRL.
        
        However, financial data for {ticker} is being pulled LIVE from market data feeds.
        
        (In a production environment, integrated with 'sec-api.io' or EDGAR RSS feed here).
        """

    def get_financials(self, ticker: str) -> Dict[str, Any]:
        """
        Extracts structured financial data using yfinance.
        """
        logger.info(f"SEC Scraper: Fetching LIVE financials for {ticker} via yfinance...")
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Map yfinance keys to our internal schema with safe defaults
            return {
                "free_cash_flow": info.get("freeCashflow", 0),
                "revenue": info.get("totalRevenue", 0),
                "net_income": info.get("netIncomeToCommon", 0),
                "gross_margin": info.get("grossMargins", 0),
                "roic": info.get("returnOnEquity", 0), # ROE as proxy if ROIC missing
                "growth_rate_5y": info.get("earningsGrowth", 0.05),
                "wacc": 0.09, # Hard to calc live without extensive data, default 9%
                "shares_outstanding": info.get("sharesOutstanding", 0),
                "current_price": info.get("currentPrice", 0),
                "market_cap": info.get("marketCap", 0),
                "average_volume": info.get("averageVolume", 0)
            }
        except Exception as e:
            logger.error(f"Failed to fetch financials for {ticker}: {e}")
            raise

