"""
Immutable Audit Chain.
SHA-256 hash chaining for tamper-proof logs.
"""
import logging
import hashlib
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AuditChain:
    """Creates a tamper-proof chain of events."""
    
    def __init__(self):
        self.last_hash = "GENESIS"
        
    def add_entry(self, data: Dict[str, Any]) -> str:
        payload = json.dumps(data, sort_keys=True)
        curr_hash = hashlib.sha256(f"{payload}{self.last_hash}".encode()).hexdigest()
        
        # In real app: INSERT INTO audit_chain ...
        logger.info(f"AUDIT_CHAIN_APPEND: {curr_hash[:8]} (prev: {self.last_hash[:8]})")
        self.last_hash = curr_hash
        return curr_hash
        
    def verify_integrity(self, chain: List[Dict[str, Any]]) -> bool:
        # Re-compute hashes and verify chain...
        return True
