import logging
from typing import List, Dict, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class LoanTapeService:
    """
    Phase 171.1: Loan Tape Ingestion Engine.
    Processes institutional loan tapes for private credit portfolios.
    """
    
    def ingest_tape(self, tape_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ingests a list of loans and calculates total portfolio committed.
        """
        total_committed = sum(Decimal(str(loan["principal"])) for loan in tape_data)
        count = len(tape_data)
        
        logger.info(f"CREDIT_LOG: Ingested tape with {count} loans. Total Principal: ${total_committed:,.2f}")
        
        return {
            "loan_count": count,
            "total_committed": float(round(total_committed, 2)),
            "status": "LOADED"
        }
