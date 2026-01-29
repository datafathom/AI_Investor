"""
MFA Service.
Multi-factor authentication for critical override actions.
"""
import logging
import pyotp
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MFAService:
    """Handles multi-factor authentication."""
    
    def __init__(self, secret: str = None):
        self.secret = secret if secret else pyotp.random_base32()
        self.totp = pyotp.TOTP(self.secret)
    
    def verify_token(self, token: str) -> bool:
        """Verify the provided 6-digit MFA token."""
        return self.totp.verify(token)
    
    def get_provisioning_uri(self, name: str, issuer_name: str) -> str:
        """Get the URI for QR code generation."""
        return self.totp.provisioning_uri(name=name, issuer_name=issuer_name)
