"""
==============================================================================
FILE: services/ai_assistant/learning_service.py
ROLE: Learning System
PURPOSE: Tracks user preferences, conversation history, and recommendation
         engine.

INTEGRATION POINTS:
    - AssistantService: Conversation context
    - UserService: User data
    - LearningService: Preference learning
    - LearningAPI: Learning endpoints

FEATURES:
    - Preference learning
    - Conversation history
    - Recommendation engine
    - Learning improvements

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.ai_assistant import UserPreference, Recommendation
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class LearningService:
    """
    Service for learning user preferences.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
    async def update_user_preferences(
        self,
        user_id: str,
        preferences: Dict[str, str]
    ) -> List[UserPreference]:
        """
        Update user preferences.
        
        Args:
            user_id: User identifier
            preferences: Dict of category to value
            
        Returns:
            List of updated UserPreference objects
        """
        logger.info(f"Updating preferences for user {user_id}")
        
        updated_prefs = []
        for category, value in preferences.items():
            pref = UserPreference(
                preference_id=f"pref_{user_id}_{category}",
                user_id=user_id,
                category=category,
                value=value,
                confidence=1.0,
                learned_date=datetime.utcnow(),
                updated_date=datetime.utcnow()
            )
            updated_prefs.append(pref)
            await self._save_preferences(pref)
            
        return updated_prefs
    
    async def get_user_preferences(
        self,
        user_id: str
    ) -> List[Dict]:
        """
        Get user preferences.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of preference dictionaries
        """
        # In production, would fetch from database
        # For now, return mock preferences
        return [
            {"category": "risk_tolerance", "value": "moderate", "confidence": 0.8},
            {"category": "investment_style", "value": "growth", "confidence": 0.7}
        ]
        
    async def get_recommendations(self, user_id: str) -> List[Recommendation]:
        """Alias for generate_recommendations to match test suite."""
        return await self.generate_recommendations(user_id)
    
    async def learn_from_interaction(
        self,
        user_id: str,
        user_message: str,
        assistant_response: str
    ):
        """
        Learn from user interaction.
        
        Args:
            user_id: User identifier
            user_message: User message
            assistant_response: Assistant response
        """
        logger.info(f"Learning from interaction for user {user_id}")
        
        # In production, would analyze interaction and update preferences
        # For now, just log
        pass
    
    async def generate_recommendations(
        self,
        user_id: str
    ) -> List[Recommendation]:
        """
        Generate personalized recommendations.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of Recommendation objects
        """
        logger.info(f"Generating recommendations for user {user_id}")
        
        recommendations = []
        
        # Generate investment recommendation
        rec1 = Recommendation(
            recommendation_id=f"rec_{user_id}_{datetime.utcnow().timestamp()}",
            user_id=user_id,
            recommendation_type="investment",
            title="Diversify Portfolio",
            description="Consider adding international stocks to diversify your portfolio",
            confidence=0.75,
            reasoning="Based on your current portfolio allocation",
            created_date=datetime.utcnow()
        )
        recommendations.append(rec1)
        
        # Save recommendations
        for rec in recommendations:
            await self._save_recommendation(rec)
        
        return recommendations
    
    async def _save_recommendation(self, recommendation: Recommendation):
        """Save recommendation to cache."""
        cache_key = f"recommendation:{recommendation.recommendation_id}"
        self.cache_service.set(cache_key, recommendation.dict(), ttl=86400 * 30)
        
    async def _save_preferences(self, preference: UserPreference):
        """Save preference to cache."""
        cache_key = f"preference:{preference.user_id}:{preference.category}"
        self.cache_service.set(cache_key, preference.dict(), ttl=86400 * 365)


# Singleton instance
_learning_service: Optional[LearningService] = None


def get_learning_service() -> LearningService:
    """Get singleton learning service instance."""
    global _learning_service
    if _learning_service is None:
        _learning_service = LearningService()
    return _learning_service
