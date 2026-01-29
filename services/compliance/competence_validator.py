import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CompetenceValidator:
    """Validates that professionals hold required credentials for their roles."""
    
    REQUIRED_CREDENTIALS = {
        "WEALTH_MANAGER": ["CFP", "SERIES_65"],
        "FINANCIAL_PLANNER": ["CFP"],
        "ASSET_MANAGER": ["CFA", "SERIES_7"]
    }

    def validate_competence(self, role_code: str, user_credentials: list) -> Dict[str, Any]:
        required = self.REQUIRED_CREDENTIALS.get(role_code, [])
        missing = [c for c in required if c not in user_credentials]
        
        is_competent = len(missing) == 0
        
        if not is_competent:
            logger.error(f"COMPLIANCE_ERROR: Role {role_code} requires {missing} which user lacks.")
            
        return {
            "is_competent": is_competent,
            "missing_credentials": missing,
            "required_credentials": required
        }
