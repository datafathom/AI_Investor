import logging
import hashlib
from typing import Dict, Any, List
from models.platform_ledger import PlatformLedger

logger = logging.getLogger(__name__)

class LedgerService:
    """Manages the immutable platform ledger."""
    
    def create_entry_hash(self, data: Dict[str, Any], prev_hash: str) -> str:
        string_to_hash = f"{data.get('account_id')}|{data.get('amount')}|{data.get('transaction_type')}|{prev_hash}"
        return hashlib.sha256(string_to_hash.encode()).hexdigest()

    def verify_chain_integrity(self, entries: List[PlatformLedger]) -> bool:
        """Validates that each entry's hash matches the checksum of the data + previous hash."""
        # Simple mock logic
        for i in range(1, len(entries)):
            expected = self.create_entry_hash(entries[i].dict(), entries[i-1].entry_hash)
            if entries[i].entry_hash != expected:
                logger.error(f"LEDGER_CRITICAL: Chain break at entry {entries[i].id}")
                return False
        return True
