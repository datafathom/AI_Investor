
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EducationService:
    """
    Service for managing user education progress.
    Persists completed tutorials and user preferences.
    """
    
    def __init__(self):
        # In a real implementation with Postgres, this would use a database model.
        # For now, we'll simulate persistence with an in-memory store or file system 
        # as we transition to full DB usage. 
        # UserID -> List of completed tutorial IDs
        self._progress_store: Dict[str, List[str]] = {}
        logger.info("EducationService initialized")

    async def get_user_progress(self, user_id: str) -> List[str]:
        """
        Get list of completed tutorials for a user.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            List of tutorial IDs that the user has completed.
        """
        return self._progress_store.get(user_id, [])

    async def mark_tutorial_complete(self, user_id: str, tutorial_id: str) -> List[str]:
        """
        Mark a tutorial as complete for a user.
        
        Args:
            user_id: The ID of the user.
            tutorial_id: The ID of the tutorial (e.g., URL path).
            
        Returns:
            Updated list of completed tutorials.
        """
        if user_id not in self._progress_store:
            self._progress_store[user_id] = []
            
        if tutorial_id not in self._progress_store[user_id]:
            self._progress_store[user_id].append(tutorial_id)
            logger.info(f"User {user_id} completed tutorial: {tutorial_id}")
            
        return self._progress_store[user_id]

# Singleton
_education_service: Optional[EducationService] = None

def get_education_service() -> EducationService:
    global _education_service
    if _education_service is None:
        _education_service = EducationService()
    return _education_service
