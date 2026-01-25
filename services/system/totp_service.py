import pyotp
import logging
from typing import Optional
from services.system.secret_manager import get_secret_manager

class TOTPService:
    """
    Service for generating and verifying TOTP (Time-based One-Time Password) codes.
    Uses pyotp library for standard-compliant MFA.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TOTPService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.sm = get_secret_manager()
        self.logger.info("TOTPService initialized.")

    def generate_new_secret(self) -> str:
        """Generates a new base32 secret for MFA setup."""
        return pyotp.random_base32()

    def get_provisioning_uri(self, secret: str, username: str, issuer_name: str = "AI Investor") -> str:
        """Returns the URI for QR code generation (otpauth://)."""
        return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer_name)

    def verify_code(self, secret: str, code: str) -> bool:
        """
        Verifies a 6-digit TOTP code against the secret.
        Includes support for a 'Hardware Mock' code (999999) if enabled.
        """
        if not secret or not code:
            return False

        # Mock Hardware Token Support (Phase 06 requirement)
        if self.sm.get_secret("YUBIKEY_MOCK") == "1" and code == "999999":
            self.logger.info("MFA Verified via Mock Hardware Token.")
            return True

        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(code)
        
        if is_valid:
            self.logger.debug("TOTP Code verified successfully.")
        else:
            self.logger.warning("Invalid TOTP Code attempt.")
            
        return is_valid

# Global accessor
def get_totp_service() -> TOTPService:
    return TOTPService()
