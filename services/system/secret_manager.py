import os
import logging
from typing import Optional, Dict

# Try to import production secret manager
try:
    from services.system.vault_secret_manager import get_production_secret_manager
    PRODUCTION_MANAGER_AVAILABLE = True
except ImportError:
    PRODUCTION_MANAGER_AVAILABLE = False

logger = logging.getLogger(__name__)

class SecretManager:
    """
    Unified interface for accessing sensitive environment variables.
    Provides masking for logs and prepares for HashiCorp Vault.
    Follows Singleton pattern.
    """
    _instance = None
    _mask_cache: Dict[str, str] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecretManager, cls).__new__(cls)
            cls._instance._init_manager()
        return cls._instance

    def _init_manager(self) -> None:
        self.logger = logging.getLogger(__name__)
        
        # Try to use production secret manager if available
        if PRODUCTION_MANAGER_AVAILABLE:
            try:
                self._production_manager = get_production_secret_manager()
                if self._production_manager._manager:
                    self.is_connected = True
                    self.engine_type = self._production_manager._manager.__class__.__name__
                    self.logger.info(f"SecretManager initialized with {self.engine_type}")
                    return
            except Exception as e:
                self.logger.warning(f"Failed to initialize production secret manager: {e}")
        
        # Fallback to environment variables
        self._production_manager = None
        self.is_connected = True
        self.engine_type = "Environment Variables"
        self.logger.info("SecretManager initialized with environment variables.")

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieves a secret from vault or environment variables."""
        # Try production manager first
        if self._production_manager:
            try:
                value = self._production_manager.get_secret(key, default)
                if value and value != default:
                    self.logger.debug(f"Accessed secret from {self.engine_type}: {key}")
                    return value
            except Exception as e:
                self.logger.warning(f"Failed to get secret from {self.engine_type}: {e}")
        
        # Fallback to environment variables
        value = os.getenv(key, default)
        if value and value != default:
            self.logger.debug(f"Accessed secret from environment: {key}")
        return value

    def get_masked_secret(self, key: str, default: Optional[str] = "N/A") -> str:
        """Retrieves a secret and returns a masked version (e.g., ****)."""
        value = self.get_secret(key)
        if not value:
            return default
        
        # Simple masking: keep first and last 2 chars
        if len(value) <= 4:
            return "****"
        return f"{value[:2]}****{value[-2:]}"

    def get_db_credentials(self) -> Dict[str, str]:
        """Structured DB credential access."""
        return {
            "url": self.get_secret("DATABASE_URL", "postgresql://investor_user:investor_password@localhost:5432/investor_db"),
            "masked_url": self.get_masked_secret("DATABASE_URL")
        }

    def get_status(self) -> Dict[str, str]:
        """Health check for the secret engine."""
        return {
            "status": "Active" if self.is_connected else "Inactive",
            "engine": self.engine_type,
            "vars_loaded": str(len(os.environ))
        }

# Global singleton accessor
def get_secret_manager() -> SecretManager:
    return SecretManager()
