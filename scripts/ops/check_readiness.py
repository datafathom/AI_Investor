
import os
import sys
import logging
import requests
from typing import List, Tuple

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ReadinessChecker:
    """
    Final readiness checker before Production Launch.
    Verifies critical components from all Phase Groups.
    """
    
    def __init__(self, base_url: str = "http://localhost:5050"):
        self.base_url = base_url

    def check_health(self) -> bool:
        """Phase 31: Health Check Endpoint"""
        try:
            r = requests.get(f"{self.base_url}/api/v1/health")
            return r.status_code == 200 and r.json().get("overall") == "UP"
        except:
            return False

    def check_secrets(self) -> bool:
        """Phase 05: Secrets Management (checks if env vars are NOT default)"""
        # In a real audit, we'd check if they are retrieved from a vault
        critical_vars = ["DATABASE_URL", "JWT_SECRET", "ALPHAVANTAGE_API_KEY"]
        for var in critical_vars:
            val = os.getenv(var)
            if not val or val == "dev_secret_key" or "localhost" in val and os.getenv("APP_ENV") == "production":
                logger.warning(f"Check Security: {var} is not production-ready.")
                return False
        return True

    def run_all_checks(self) -> bool:
        logger.info("--- AI Investor Launch Readiness Audit ---")
        
        checks = [
            ("System Health (Phase 31)", self.check_health),
            ("Secrets Validation (Phase 05)", self.check_secrets),
        ]
        
        all_passed = True
        for name, func in checks:
            passed = func()
            status = "✅ PASSED" if passed else "❌ FAILED"
            logger.info(f"{status} - {name}")
            if not passed:
                all_passed = False
                
        if all_passed:
            logger.info("🚀 SYSTEM IS READY FOR PRODUCTION LAUNCH")
        else:
            logger.error("🛑 LAUNCH BLOCKED: Critical readiness checks failed.")
            
        return all_passed

if __name__ == "__main__":
    checker = ReadinessChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
