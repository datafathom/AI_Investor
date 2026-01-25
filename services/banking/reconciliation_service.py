import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from services.banking.banking_service import get_banking_service

class ReconciliationService:
    """
    Engine to match bank transactions with internal system ledger entries.
    Flags discrepancies and handles fuzzy matching on date/amount/description.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReconciliationService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self) -> None:
        self.logger = logging.getLogger(__name__)
        # In a real app, this would be a DB session
        self.mock_ledger = [
            {"id": "tx_internal_1", "date": datetime.now() - timedelta(days=1), "amount": -42.50, "desc": "Starbucks NYC"},
            {"id": "tx_internal_2", "date": datetime.now() - timedelta(days=2), "amount": 5000.00, "desc": "Transfer from Checking"},
            {"id": "tx_internal_3", "date": datetime.now() - timedelta(days=3), "amount": -120.00, "desc": "AWS Usage fees"}
        ]

    def perform_reconciliation(self, access_token: str) -> Dict[str, Any]:
        """
        Compares bank transactions with the internal ledger.
        Returns matched pairs and unreconciled items.
        """
        banking_service = get_banking_service()
        # In simulation mode, this fetches mock items
        bank_txs = [
            {"id": "bank_1", "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), "amount": -42.50, "desc": "Starbucks Coffee"},
            {"id": "bank_2", "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), "amount": 5000.00, "desc": "Incoming Wire Transfer"},
            {"id": "bank_4", "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"), "amount": -10.99, "desc": "Netflix Inc"}
        ]
        
        matched = []
        unreconciled_bank = []
        unreconciled_ledger = list(self.mock_ledger)
        
        for btx in bank_txs:
            found_match = False
            btx_date = datetime.strptime(btx['date'], "%Y-%m-%d")
            
            for ltx in list(unreconciled_ledger):
                # Matching Logic: Same amount, date within 2 days, description similar
                date_diff = abs((btx_date - ltx['date']).days)
                amount_match = float(btx['amount']) == float(ltx['amount'])
                
                # Simple "contains" or fuzzy match on description for this prototype
                desc_match = btx['desc'].lower()[:5] in ltx['desc'].lower()
                
                if amount_match and date_diff <= 2 and desc_match:
                    matched.append({"bank": btx, "ledger": ltx})
                    unreconciled_ledger.remove(ltx)
                    found_match = True
                    break
            
            if not found_match:
                unreconciled_bank.append(btx)
                
        return {
            "matched_count": len(matched),
            "unreconciled_bank": unreconciled_bank,
            "unreconciled_ledger": [
                {"id": l['id'], "date": l['date'].strftime("%Y-%m-%d"), "amount": l['amount'], "desc": l['desc']}
                for l in unreconciled_ledger
            ],
            "accuracy": len(matched) / (len(bank_txs) or 1) * 100,
            "last_audit": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# Global Accessor
def get_reconciliation_service() -> ReconciliationService:
    return ReconciliationService()
