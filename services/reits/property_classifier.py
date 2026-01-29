import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PropertyClassifier:
    """Categorizes REITs into specific property sectors based on business profile."""
    
    SECTOR_MAP = {
        "O": "RETAIL",
        "WPC": "INDUSTRIAL",
        "DLR": "DATA_CENTER",
        "EQR": "RESIDENTIAL",
        "FPI": "AGRICULTURE",
        "AMT": "INFRASTRUCTURE",
        "PLD": "INDUSTRIAL"
    }

    def classify_ticker(self, ticker: str) -> str:
        sector = self.SECTOR_MAP.get(ticker.upper(), "DIVERSIFIED")
        logger.info(f"REIT_LOG: Classified {ticker} as {sector}")
        return sector

    def evaluate_inflation_hedge(self, sector: str) -> float:
        """
        Score: 0.0 to 1.0. High for Agriculture/Industrial, Low for Office.
        """
        scores = {
            "AGRICULTURE": 0.95,
            "INDUSTRIAL": 0.85,
            "RESIDENTIAL": 0.75,
            "RETAIL": 0.50,
            "OFFICE": 0.30
        }
        return scores.get(sector, 0.5)
