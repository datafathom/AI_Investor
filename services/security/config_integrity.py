"""
Configuration Integrity Service.
Generates and verifies SHA-256 hashes of the active risk state.
Serves as a tripwire against unauthorized DB manipulation.
"""
import hashlib
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ConfigIntegrity:
    """
    Validates that the risk state matches its signed hash.
    """

    @staticmethod
    def generate_state_hash(config_data: Dict[str, Any]) -> str:
        """
        Create a deterministic SHA-256 hash of the configuration dict.
        """
        # Sort keys for consistent hashing
        encoded_data = json.dumps(config_data, sort_keys=True).encode('utf-8')
        return hashlib.sha256(encoded_data).hexdigest()

    @staticmethod
    def verify_integrity(active_config: Dict[str, Any], stored_hash: str) -> bool:
        """
        Check if the current config has been tampered with.
        """
        # Remove metadata/audit fields before hashing for comparison if necessary
        # For this implementation, we assume the hash covers the entire signed payload
        current_hash = ConfigIntegrity.generate_state_hash(active_config)
        
        if current_hash != stored_hash:
            logger.critical(f"INTEGRITY_VIOLATION: Config hash mismatch! Expected {stored_hash[:8]}, Got {current_hash[:8]}")
            return False
            
        return True
