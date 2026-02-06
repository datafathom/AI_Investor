import logging
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SovereignRouter:
    """
    Routes AI tasks based on privacy and complexity.
    - HIGH PRIVACY (Keys, PII) -> Local Model (Ollama)
    - LOW PRIVACY -> Cloud Model (OpenAI)
    """
    _instance = None
    
    # Simple regex for finding sensitive patterns
    SENSITIVE_PATTERNS = [
        r"0x[a-fA-F0-9]{40}", # ETH Address
        r"-----BEGIN PRIVATE KEY-----", # RSA Key
        r"password",
        r"secret",
        r"HONEY_TEST_KEY" # Active Defense Tripwire
    ]
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SovereignRouter, cls).__new__(cls)
        return cls._instance

    def route_request(self, prompt: str) -> Dict[str, str]:
        """
        Determines the optimal model provider.
        """
        privacy_level = self._assess_privacy(prompt)
        
        if privacy_level == "HIGH":
            return {"provider": "LOCAL", "model": "llama3:8b", "reason": "PII/Key Detected"}
        else:
            return {"provider": "CLOUD", "model": "gpt-4-turbo", "reason": "Public Data"}

    def _assess_privacy(self, prompt: str) -> str:
        # 1. Honey Token Check
        if "HONEY_TEST_KEY" in prompt:
             # Trigger Security Response (Mock)
             # In real app: panic_service.trigger_panic("HONEY_TOKEN_ACCESSED")
             msg = "🚨 ACTIVE DEFENSE: Honey-Token accessed! Intruders detected."
             logger.critical(msg)
             # We return a specific signal or raise exception
             raise PermissionError("SYSTEM_LOCKDOWN_INITIATED")

        # 2. Privacy Pattern Check
        for pattern in self.SENSITIVE_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                logger.warning(f"SovereignRouter: Senstitive data detected by pattern '{pattern}'")
                return "HIGH"
        return "LOW"

# Singleton
sovereign_router = SovereignRouter()
def get_sovereign_router() -> SovereignRouter:
    return sovereign_router
