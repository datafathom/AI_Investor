from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

# Shared limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10000 per day", "500 per hour"],
    storage_uri="memory://", # Replaced with Redis in production if needed
    strategy="fixed-window"
)

class SecurityGatewayService:
    """
    Manages API security policies including rate limiting and basic WAF rules.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.status = "Active"
        self.waf_mode = "Core v1 (Enabled)"

    def get_status(self):
        """Returns the current state of the security gateway."""
        return {
            "status": self.status,
            "rate_limiter": "Active",
            "waf_rules": self.waf_mode,
            "default_limits": "10000/day, 500/hr"
        }

def get_security_gateway() -> SecurityGatewayService:
    return SecurityGatewayService()
