import logging
import random
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class FundamentalScanner:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FundamentalScanner, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.metrics = [
            {"id": "pe_ratio", "name": "P/E Ratio", "category": "Valuation", "format": "number"},
            {"id": "peg_ratio", "name": "PEG Ratio", "category": "Valuation", "format": "number"},
            {"id": "ps_ratio", "name": "P/S Ratio", "category": "Valuation", "format": "number"},
            {"id": "pb_ratio", "name": "P/B Ratio", "category": "Valuation", "format": "number"},
            {"id": "roe", "name": "Return on Equity", "category": "Profitability", "format": "percent"},
            {"id": "roa", "name": "Return on Assets", "category": "Profitability", "format": "percent"},
            {"id": "gross_margin", "name": "Gross Margin", "category": "Profitability", "format": "percent"},
            {"id": "operating_margin", "name": "Operating Margin", "category": "Profitability", "format": "percent"},
            {"id": "net_margin", "name": "Net Margin", "category": "Profitability", "format": "percent"},
            {"id": "revenue_growth", "name": "Revenue Growth (YoY)", "category": "Growth", "format": "percent"},
            {"id": "earnings_growth", "name": "Earnings Growth (YoY)", "category": "Growth", "format": "percent"},
            {"id": "debt_to_equity", "name": "Debt/Equity", "category": "Health", "format": "number"},
            {"id": "current_ratio", "name": "Current Ratio", "category": "Health", "format": "number"},
            {"id": "dividend_yield", "name": "Dividend Yield", "category": "Income", "format": "percent"},
        ]
        
        self._seed_mock_db()
        self._initialized = True

    def _seed_mock_db(self):
        self.companies = []
        sectors = ["Technology", "Healthcare", "Finance", "Energy", "Consumer", "Industrial"]
        tickers_base = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK.B", "LLY", "V", "JPM", "XOM", "WMT", "MA", "PG", "JNJ", "AVGO", "HD", "CVX", "MRK", "ABBV", "KO", "PEP", "COST", "ORCL"]
        
        for t in tickers_base:
            seed = sum(ord(c) for c in t)
            random.seed(seed)
            
            company = {
                "ticker": t,
                "name": f"{t} Corp",
                "sector": random.choice(sectors),
                "metrics": {}
            }
            
            for m in self.metrics:
                val = 0
                if m["id"] == "pe_ratio": val = random.uniform(10, 100)
                elif m["id"] == "peg_ratio": val = random.uniform(0.5, 3.0)
                elif m["id"] == "dividend_yield": val = random.uniform(0, 0.05) if random.random() > 0.3 else 0
                else: val = random.uniform(-0.1, 0.5)
                
                company["metrics"][m["id"]] = round(val, 2) if m["format"] == "number" else round(val, 4)
            
            self.companies.append(company)

    async def list_metrics(self) -> List[Dict]:
        return self.metrics

    async def run_scan(self, criteria: List[Dict]) -> List[Dict]:
        """
        Criteria: [{"metric": "pe_ratio", "operator": "<", "value": 20}, ...]
        """
        results = []
        for company in self.companies:
            match = True
            for c in criteria:
                metric_id = c['metric']
                op = c['operator']
                val = float(c['value'])
                
                comp_val = company['metrics'].get(metric_id)
                if comp_val is None:
                    match = False
                    break
                    
                # Handle percentage conversion check if needed, but for now assuming direct compare
                
                if op == "<" and not (comp_val < val): match = False
                elif op == ">" and not (comp_val > val): match = False
                elif op == "=" and not (comp_val == val): match = False
                elif op == ">=" and not (comp_val >= val): match = False
                elif op == "<=" and not (comp_val <= val): match = False
                
            if match:
                results.append(company)
                
        return results

    async def get_company_details(self, ticker: str) -> Optional[Dict]:
        for c in self.companies:
            if c['ticker'] == ticker:
                return c
        return None
