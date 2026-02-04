import logging
from typing import List, Optional
from uuid import UUID
from schemas.advisor import Advisor, AdvisorCreate

logger = logging.getLogger(__name__)

class AdvisorService:
    """Manages advisor data and fiduciary status."""
    
    def __init__(self):
        # In a real app, this would interact with a DB session
        self.mock_db = {} 

    def create_advisor(self, advisor_data: AdvisorCreate) -> Advisor:
        """Creates a new advisor record."""
        new_advisor = Advisor(**advisor_data.model_dump())
        self.mock_db[new_advisor.id] = new_advisor
        logger.info(f"ADVISOR_LOG: Created advisor {new_advisor.name} with fiduciary_status={new_advisor.fiduciary_status}")
        return new_advisor

    def get_advisor(self, advisor_id: UUID) -> Optional[Advisor]:
        """Retrieves an advisor by ID."""
        return self.mock_db.get(advisor_id)

    def list_advisors(self) -> List[Advisor]:
        """Lists all advisors."""
        return list(self.mock_db.values())

    def update_fiduciary_status(self, advisor_id: UUID, status: bool) -> Optional[Advisor]:
        """Updates the fiduciary status of an advisor."""
        advisor = self.get_advisor(advisor_id)
        if advisor:
            advisor.fiduciary_status = status
            logger.info(f"ADVISOR_LOG: Updated fiduciary status to {status} for advisor {advisor.name}")
            return advisor
        return None
