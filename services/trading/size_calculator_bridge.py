"""
Position Size Calculator API Bridge.
Integrates external Position Size Calculator API.
"""
import logging
import aiohttp
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SizeCalculatorBridge:
    """Bridge to the Position Size Calculator API."""
    
    API_URL = "http://calculator-service:5000/calculate"
    
    async def calculate_size(self, account_id: str, symbol: str, entry: float, stop: float, risk_pct: float) -> Dict[str, Any]:
        """Call usage calculation API."""
        payload = {
            "account_id": account_id,
            "symbol": symbol,
            "entry_price": entry,
            "stop_loss": stop,
            "risk_percentage": risk_pct
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.API_URL, json=payload, timeout=2.0) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"SIZE_API_ERROR: {response.status}")
                        return {"error": "API Error", "units": 0}
        except Exception as e:
            logger.error(f"SIZE_CALC_FAILURE: {e}")
            return {"error": str(e), "units": 0}
