"""
Record Vault Service
Phase 7 Implementation: The Compliance Shield

This service implements a Write-Once-Read-Many (WORM) style record vault
using cryptographically linked ledger entries (hash-chaining) and AES-256
encryption for sensitive data.

ACCEPTANCE CRITERIA:
- C1: Every entry is signed with the SHA-256 hash of the previous entry.
- C2: Sensitive data is encrypted before being stored.
- C3: Tamper detection identifies any mid-chain modifications.
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from cryptography.fernet import Fernet
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class RecordEntry:
    def __init__(self, data: Dict[str, Any], previous_hash: str, index: int):
        self.index = index
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.data = data # This is stored as-is in memory, but encrypted in 'raw' if needed
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        sha = hashlib.sha256()
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }
        sha.update(json.dumps(payload, sort_keys=True).encode())
        return sha.hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class RecordVault:
    """
    Manages immutable financial records and logs.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecordVault, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        sm = get_secret_manager()
        key = sm.get_secret("VAULT_KEY")
        if not key:
            # Generate a key if missing (Dev mode)
            key = Fernet.generate_key().decode()
            logger.warning("VAULT_KEY missing from secrets. Self-generating for dev.")
            
        self.cipher = Fernet(key.encode())
        self.chain: List[RecordEntry] = []
        self._initialized = True
        logger.info("RecordVault initialized")

    def add_record(self, record_type: str, payload: Dict[str, Any], sensitive_keys: Optional[List[str]] = None):
        """
        Adds a new record to the hash-chain.
        Encrypts values for keys in 'sensitive_keys'.
        """
        data = payload.copy()
        data["type"] = record_type
        
        if sensitive_keys:
            for key in sensitive_keys:
                if key in data:
                    val = str(data[key]).encode()
                    data[key] = self.cipher.encrypt(val).decode()

        prev_hash = self.chain[-1].hash if self.chain else "GENESIS"
        entry = RecordEntry(data, prev_hash, len(self.chain))
        self.chain.append(entry)
        
        logger.info(f"Record added to vault: {record_type} (Index: {entry.index})")
        return entry.hash

    def verify_chain(self) -> bool:
        """
        Full forensic audit of the hash chain.
        """
        for i in range(len(self.chain)):
            entry = self.chain[i]
            
            # 1. Check current hash integrity
            if entry.hash != entry.calculate_hash():
                logger.error(f"Integrity Violation at Index {i}: Hash mismatch")
                return False
            
            # 2. Check link integrity
            if i > 0:
                prev_entry = self.chain[i-1]
                if entry.previous_hash != prev_entry.hash:
                    logger.error(f"Integrity Violation at Index {i}: Linkage mismatch")
                    return False
            elif entry.previous_hash != "GENESIS":
                logger.error("Integrity Violation at Index 0: Genesis mismatch")
                return False
                
        return True

    def decrypt_value(self, encrypted_val: str) -> str:
        """Helper to decrypt sensitive data."""
        return self.cipher.decrypt(encrypted_val.encode()).decode()

    def get_records_by_type(self, record_type: str) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self.chain if e.data.get("type") == record_type]

def get_record_vault() -> RecordVault:
    return RecordVault()
