"""
Estate Planning Integrator - Phase 53.
Tracks beneficiaries and estate documents.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class EstatePlanner:
    """Manages estate planning information."""
    
    def __init__(self):
        self.beneficiaries: List[Dict[str, Any]] = []
        self.documents: Dict[str, bool] = {
            "will": False,
            "trust": False,
            "power_of_attorney": False,
            "healthcare_directive": False
        }
    
    def add_beneficiary(self, name: str, relationship: str, percentage: float):
        self.beneficiaries.append({
            "name": name,
            "relationship": relationship,
            "percentage": percentage
        })
    
    def mark_document_complete(self, doc_type: str):
        if doc_type in self.documents:
            self.documents[doc_type] = True
    
    def get_completion_status(self) -> float:
        completed = sum(1 for v in self.documents.values() if v)
        return completed / len(self.documents) * 100
