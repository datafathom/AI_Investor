import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CountryRiskService:
    """Evaluates country-level investment risk (sanctions, capital controls)."""
    
    # Mock Risk DB
    RISK_MAP = {
        "CN": {"repatriation_risk": "MEDIUM", "sanction_risk": "HIGH", "cap_controls": True},
        "RU": {"repatriation_risk": "CRITICAL", "sanction_risk": "CRITICAL", "cap_controls": True},
        "TW": {"repatriation_risk": "LOW", "sanction_risk": "MEDIUM", "cap_controls": False},
        "CH": {"repatriation_risk": "LOW", "sanction_risk": "LOW", "cap_controls": False},
        "SG": {"repatriation_risk": "LOW", "sanction_risk": "LOW", "cap_controls": False}
    }

    def evaluate_country(self, country_code: str) -> Dict[str, Any]:
        risk = self.RISK_MAP.get(country_code.upper(), {"repatriation_risk": "UNKNOWN", "sanction_risk": "UNKNOWN"})
        logger.info(f"RISK_LOG: Evaluated risk for {country_code}: {risk['sanction_risk']} sanctions.")
        return risk
