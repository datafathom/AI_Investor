import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class EnvoyService:
    """
    Handles external communication Simulation.
    Ingests 'signals' (mock emails/messages) and routes them to departments.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvoyService, cls).__new__(cls)
        return cls._instance

    def ingest_signal(self, source: str, content: str) -> Dict[str, Any]:
        """
        Classifies and routes an incoming message.
        """
        classification = self._classify_content(content)
        
        route_map = {
            "INVESTOR_UPDATE": "Dept 15 (Historian)",
            "SECURITY_ALERT": "Dept 8 (Sentry)",
            "OPPORTUNITY": "Dept 7 (Hunter)",
            "SPAM": "Trash"
        }
        
        target = route_map.get(classification, "Inbox")
        logger.info(f"Envoy: Routed signal from {source} [{classification}] -> {target}")
        
        return {
            "source": source,
            "classification": classification,
            "routed_to": target,
            "timestamp": "Now"
        }

    def _classify_content(self, content: str) -> str:
        content_upper = content.upper()
        
        if "LOGIN DETECTED" in content_upper or "VERIFY" in content_upper:
            return "SECURITY_ALERT"
        if "Q1 RESULTS" in content_upper or "UPDATE" in content_upper:
            return "INVESTOR_UPDATE"
        if "DEAL" in content_upper or "EXCLUSIVE" in content_upper:
            return "OPPORTUNITY"
        if "UNSUBSCRIBE" in content_upper or "FREE TOAST" in content_upper:
            return "SPAM"
            
        return "UNKNOWN"

# Singleton
envoy_service = EnvoyService()
def get_envoy_service() -> EnvoyService:
    return envoy_service
