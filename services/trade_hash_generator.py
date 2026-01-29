"""
Trade Hash Generator Service.
Guarantees integrity of the performance audit trail using SHA-256.
"""
import hashlib
import json
from typing import Any, Dict

class TradeHashGenerator:
    """
    Service to generate cryptographic hashes for trade entries.
    """

    @staticmethod
    def generate_hash(trade_data: Dict[str, Any]) -> str:
        """
        Creates a SHA-256 hash of immutable trade fields.
        
        Args:
            trade_data: Dictionary containing trade fields.
            
        Returns:
            str: SHA-256 hex digest.
        """
        # Define fields that should be immutable for audit
        audit_fields = [
            'trade_id', 'symbol', 'direction', 'entry_price', 
            'stop_loss', 'entry_time', 'agent_id', 'trade_thesis'
        ]
        
        # Extract and canonicalize
        canonical_map = {}
        for field in audit_fields:
            val = trade_data.get(field)
            # Convert to string to ensure consistency (UUIDs, Decimals, datetimes)
            canonical_map[field] = str(val) if val is not None else ""
            
        # Serialize with sorted keys for deterministic hashing
        serialized = json.dumps(canonical_map, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()
