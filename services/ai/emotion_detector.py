"""
Emotion Detection via NLP - Phase 34.
Analyzes user input for emotional trading patterns.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EmotionDetector:
    """Detects emotional trading signals in user input."""
    
    DANGER_WORDS = ["revenge", "make it back", "all in", "yolo", "double down"]
    
    @staticmethod
    def analyze_text(text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        danger_count = sum(1 for word in EmotionDetector.DANGER_WORDS if word in text_lower)
        return {
            "danger_words_found": danger_count,
            "risk_level": "HIGH" if danger_count >= 2 else "LOW",
            "recommendation": "SUGGEST_BREAK" if danger_count >= 2 else "CONTINUE"
        }
