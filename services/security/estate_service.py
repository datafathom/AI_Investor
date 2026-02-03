"""
Estate Service - Succession & Dead Man's Switch
Phase 58: Manages beneficiary allocations, heartbeat monitoring, and inheritance.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class Beneficiary:
    id: str
    name: str
    relationship: str
    allocation_percent: float
    contact_email: str

@dataclass
class HeartbeatStatus:
    last_check: Optional[str]
    is_alive: bool
    days_until_trigger: int
    trigger_date: Optional[str]

@dataclass
class SuccessionResult:
    triggered: bool
    beneficiaries_notified: int
    assets_transferred: float
    timestamp: str

@dataclass
class EntityNode:
    id: str
    label: str
    type: str  # TRUST, LLC, INDIVIDUAL, CHARITY
    jurisdiction: Optional[str] = None
    tax_id: Optional[str] = None

@dataclass
class EntityEdge:
    source: str
    target: str
    type: str  # OWNS, BENEFICIARY_OF, TRUSTEE_OF

class EstateService:
    def __init__(self) -> None:
        self._beneficiaries: List[Beneficiary] = [
            Beneficiary("b1", "Spouse (Primary)", "Spouse", 50.0, "spouse@example.com"),
            Beneficiary("b2", "Children's Trust", "Trust", 40.0, "trust@example.com"),
            Beneficiary("b3", "Charitable Foundation", "Charity", 10.0, "charity@example.com")
        ]
        self._last_heartbeat: datetime = datetime.now()
        self._trigger_days: int = 30
        self._nodes = [
            EntityNode("n1", "Master Family Trust", "TRUST", "Wyoming", "***-**-9482"),
            EntityNode("n2", "HoldCo LLC", "LLC", "Delaware", "***-**-1122"),
            EntityNode("n3", "Real Estate LP", "LLC", "Nevada", "***-**-3344"),
            EntityNode("n4", "John Doe", "INDIVIDUAL", None, None)
        ]
        self._edges = [
            EntityEdge("n1", "n2", "OWNS"),
            EntityEdge("n1", "n3", "OWNS"),
            EntityEdge("n4", "n1", "BENEFICIARY_OF")
        ]
        logger.info("EstateService initialized")
    
    def check_heartbeat(self, user_id: str) -> HeartbeatStatus:
        days_since = (datetime.now() - self._last_heartbeat).days
        days_until = max(0, self._trigger_days - days_since)
        trigger_date = (self._last_heartbeat + timedelta(days=self._trigger_days)).isoformat()
        return HeartbeatStatus(
            last_check=self._last_heartbeat.isoformat(),
            is_alive=days_until > 0,
            days_until_trigger=days_until,
            trigger_date=trigger_date
        )
    
    def confirm_alive(self, user_id: str) -> bool:
        self._last_heartbeat = datetime.now()
        logger.info(f"Heartbeat confirmed for {user_id}")
        return True
    
    def trigger_succession(self, user_id: str) -> SuccessionResult:
        logger.warning(f"Succession triggered for {user_id}")
        return SuccessionResult(
            triggered=True,
            beneficiaries_notified=len(self._beneficiaries),
            assets_transferred=25000000.0,  # Mocked total
            timestamp=datetime.now().isoformat()
        )
    
    def get_beneficiaries(self, user_id: str) -> List[Beneficiary]:
        return self._beneficiaries
    
    def add_beneficiary(self, user_id: str, beneficiary: Beneficiary) -> Beneficiary:
        self._beneficiaries.append(beneficiary)
        return beneficiary

    def update_allocation(self, user_id: str, beneficiary_id: str, percent: float) -> bool:
        for b in self._beneficiaries:
            if b.id == beneficiary_id:
                b.allocation_percent = percent
                return True
        return False
    
    def get_entity_graph(self, user_id: str) -> Dict:
        return {
            "nodes": [n.__dict__ for n in self._nodes],
            "edges": [e.__dict__ for e in self._edges]
        }
    
    def calculate_estate_tax(self, total_value: float) -> float:
        # 2023 exemption is $12.92M per individual
        exemption = 12920000.0
        if total_value > exemption:
            return (total_value - exemption) * 0.40
        return 0.0

_estate_service: Optional[EstateService] = None
def get_estate_service() -> EstateService:
    global _estate_service
    if _estate_service is None:
        _estate_service = EstateService()
    return _estate_service
