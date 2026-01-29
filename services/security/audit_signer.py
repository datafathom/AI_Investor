"""
Audit Signer.
Signs critical log entries.
"""
import logging
import hashlib
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AuditSigner:
    """Signs audit logs."""
    
    SECRET_KEY = "mock-secret-key-phase-23"
    
    @staticmethod
    def sign_entry(entry: Dict[str, Any]) -> str:
        """Generate SHA-256 signature for log entry."""
        payload = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(f"{payload}{AuditSigner.SECRET_KEY}".encode()).hexdigest()
    
    @staticmethod
    def verify_signature(entry: Dict[str, Any], signature: str) -> bool:
        return AuditSigner.sign_entry(entry) == signature
